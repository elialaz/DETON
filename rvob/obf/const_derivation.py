from enum import Enum, auto
from typing import Tuple, List, Optional, NamedTuple, Union
from secrets import randbits
from random import seed, choices, sample, randrange
from BitVector import BitVector

from rep.base import Instruction
from structures import Register


class Opcodes(Enum):
    pass


class OtherOps(Opcodes):
    """Opcodes of instructions that are neither arithmetic nor memory-related"""

    LI = auto()
    LUI = auto()


class ALOps(Opcodes):
    """Opcodes of arithmetic/logic instructions"""

    ADD = auto()
    ADDI = auto()
    SUB = auto()
    SUBI = auto()
    AND = auto()
    ANDI = auto()
    OR = auto()
    ORI = auto()
    XOR = auto()
    XORI = auto()
    SLLI = auto()
    SRLI = auto()
    SLL = auto()
    SRL = auto()

# TODO this enumeration isn't strictly necessary, but I think it can be useful in other places.
class Direction(Enum):
    FROM_MEM = auto()
    TO_MEM = auto()


# TODO this enumeration isn't strictly necessary, but I think it can be useful in other places.
class ObjectSize(Enum):
    """The data size on which an instruction operates"""

    BYTE = 8
    HALF = 16
    WORD = 32


class MemOps(Opcodes):
    """Memory-related instructions, with information about data direction (to memory/from memory) and data size"""

    LW = (Direction.FROM_MEM, ObjectSize.WORD)
    LH = (Direction.FROM_MEM, ObjectSize.HALF)
    LHU = (Direction.FROM_MEM, ObjectSize.HALF)
    LB = (Direction.FROM_MEM, ObjectSize.BYTE)
    LBU = (Direction.FROM_MEM, ObjectSize.BYTE)
    SW = (Direction.TO_MEM, ObjectSize.WORD)
    SH = (Direction.TO_MEM, ObjectSize.HALF)
    SB = (Direction.TO_MEM, ObjectSize.BYTE)

    def __init__(self, direction: Direction, object_size: ObjectSize):
        self.direction = direction
        self.object_size = object_size


class Promise(NamedTuple):
    """
    A placeholder for an instruction.

    Obfuscation functions don't directly produce instructions objects. Instead, they output a virtual instruction (a
    promise), that is: on object which carries the opcode of the represented instruction and a description of its
    register and immediate operands.
    A register operand description can be None, if that operand isn't needed by the instruction, a Register object, for
    a concrete register, or an integer, representing an unresolved register that should be chosen at placement time.
    An immediate operand description can only be None ore an ImmediateConstant object.
    """

    op: Opcodes
    rd: Optional[Union[int, Register]]
    rs1: Optional[Union[int, Register]]
    rs2: Optional[Union[int, Register]]
    const: Optional[Instruction.ImmediateConstant]


class Goal(NamedTuple):
    """
    A goal represents an intention of putting a certain value in a register at some point in the execution flow.

    Goals are used by the obfuscation machinery to keep track of the value that needs to be obfuscated and of the
    register in which subsequent instructions expect to find it.
    """

    reg: Union[int, Register]
    const: Instruction.ImmediateConstant


class Derivation(NamedTuple):
    """The current state of the obfuscated derivation chain for a constant."""

    chain: List[Promise]
    remainder: Goal


def _next_reg_placeholder(p: Union[int, Register]) -> int:
    return p + 1 if isinstance(p, int) else 0


def mem_primer(target: Instruction) -> Derivation:
    """Generate an equivalent instruction sequence as a memory op with no offset and an already shifted base."""

    # 0: new address base
    # 1: register from where the offset is to be loaded
    starting_sequence = [
        Promise(MemOps[target.opcode.upper()], target.r1, 0, None, Instruction.ImmediateConstant(12, None, 0)),
        Promise(ALOps.ADD, 0, target.r2, 1, None)
        ]

    # Prime the derivation with the starting sequence and the correct promise
    return Derivation(starting_sequence, Goal(1, target.immediate))


def imm_primer(target: Instruction) -> Derivation:
    """Substitute the given instruction with its R-format counterpart; initialize the goal with its immediate value."""

    return Derivation([Promise(ALOps[target.opcode[:-1].upper()], target.r1, target.r2, 0, None)],
                      Goal(0, target.immediate))


def lui_primer(target: Instruction) -> Derivation:
    """Break a load upper immediate into less revealing operations (ors and shifts); obfuscate the 12 upper bits."""

    # Shift the bits around to load 12 + 8 bits separately: insert 12b -> shift left 8 -> insert 8b -> shift left 12
    loading_sequence = [
        Promise(ALOps.SLLI, target.r1, 0, None, Instruction.ImmediateConstant(12, None, 12)),
        Promise(ALOps.ORI,
                0,
                1,
                None,
                Instruction.ImmediateConstant(12, None, target.immediate.value[-8:].int_val())),
        Promise(ALOps.SLLI, 1, 2, None, Instruction.ImmediateConstant(12, None, 8))
        ]

    # With the previous shifting and loading machinery in place, target the 12 most significant bits for obfuscation
    return Derivation(loading_sequence,
                      Goal(2, Instruction.ImmediateConstant(12, None, target.immediate.value[:-8].int_val())))


def shifter_obf(goal: Goal) -> Tuple[Promise, Goal]:
    """
    Modify a constant by bit-shifting it, producing a promise for an instruction that reverses the shift.

    The shifting direction that results in the highest number of shifts is used.
    """

    def _count_leading_zeros(constant: BitVector):
        leading_zeroes = 0
        while constant[0] == 0:
            leading_zeroes += 1
            constant <<= 1

        return leading_zeroes

    def _count_trailing_zeroes(constant: BitVector):
        trailing_zeroes = 0
        while constant[-1] == 0:
            trailing_zeroes += 1
            constant >>= 1

        return trailing_zeroes

    if goal.const.int_val != 0:
        lead = _count_leading_zeros(goal.const.value)
        trail = _count_trailing_zeroes(goal.const.value)
    else:
        lead = goal.const.size
        trail = goal.const.size

    if lead > trail:
        shift = lead
        new_val = goal.const.value << lead
        instruction = ALOps.SRLI
    else:
        shift = trail
        new_val = goal.const.value >> trail
        instruction = ALOps.SLLI

    return (Promise(instruction, goal.reg, _next_reg_placeholder(goal.reg), None,
                    Instruction.ImmediateConstant(goal.const.size, None, shift)),
            Goal(_next_reg_placeholder(goal.reg), Instruction.ImmediateConstant(new_val.size, None, new_val.int_val())))


def logic_ori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    """
    Modifies a constant by or-ing it with a random value.

    The produced promise reverts the transformation based on the identity: (A and !B) or (A and B) = A
    The value used for obfuscation is derived from high-quality entropy sources.
    """

    noise = randbits(goal.const.size)
    immediate = goal.const.int_val
    return (Promise(ALOps.ORI, goal.reg, _next_reg_placeholder(goal.reg), None,
                    Instruction.ImmediateConstant(goal.const.size, None, immediate & ~noise)),
            Goal(_next_reg_placeholder(goal.reg),
                 Instruction.ImmediateConstant(goal.const.size, None, immediate & noise)))


def logic_andi_obf(goal: Goal) -> Tuple[Promise, Goal]:
    """
    Modifies a constant by and-ing it with a random value.

    The produced promise reverts the transformation based on the identity: (A or !B) and (A or B) = A
    The value used for obfuscation is derived from high-quality entropy sources.
    """

    noise = randbits(goal.const.size)
    immediate = goal.const.int_val
    return (Promise(ALOps.ANDI, goal.reg, _next_reg_placeholder(goal.reg), None,
                    Instruction.ImmediateConstant(goal.const.size, None, immediate | ~noise)),
            Goal(_next_reg_placeholder(goal.reg),
                 Instruction.ImmediateConstant(goal.const.size, None, immediate | noise)))


def logic_xori_obf(goal: Goal) -> Tuple[Promise, Goal]:
    """
    Modifies a constant by xor-ing it with a random value.

    The produced promise reverts the transformation based on the identity: (A xor B) xor B = A
    The value used for obfuscation is derived from high-quality entropy sources.
    """

    noise = randbits(goal.const.size)
    immediate = goal.const.int_val
    return (Promise(ALOps.XORI, goal.reg, _next_reg_placeholder(goal.reg), None,
                    Instruction.ImmediateConstant(goal.const.size, None, immediate ^ noise)),
            Goal(_next_reg_placeholder(goal.reg), Instruction.ImmediateConstant(goal.const.size, None, noise)))


def terminator(goal: Goal) -> Promise:
    """
    Load the goal's value through a load immediate instruction.

    Used to terminate a derivation chain.
    """

    return Promise(OtherOps.LI, goal.reg, None, None,
                   Instruction.ImmediateConstant(32, None, goal.const.int_val))


# Map opcodes to their correct primers
primers = {
    "addi": imm_primer,
    "subi": imm_primer,
    "andi": imm_primer,
    "ori": imm_primer,
    "xori": imm_primer,
    "srli": imm_primer,
    "addiw": imm_primer,
    "slli": imm_primer,
    "lw": mem_primer,
    "lh": mem_primer,
    "lhu": mem_primer,
    "lb": mem_primer,
    "lbu": mem_primer,
    "sw": mem_primer,
    "sh": mem_primer,
    "sb": mem_primer,
    "lui": lui_primer
    }

# Catalogue of obfuscators for programmatic access
logic_obfuscators = [logic_andi_obf, logic_ori_obf, logic_xori_obf]


def generate_derivation_chain(instruction: Instruction, max_shifts: int, max_logical: int, min_length: int = 0) \
        -> List[Promise]:
    """
    Generate an obfuscated derivation chain for a given immediate instruction.

    The generated chain is random in length, composition and ordering, but respects the imposed constraints.

    :param instruction: the instruction to be obfuscated
    :param max_shifts: the maximum number of shift operations that the derivation chain should contain
    :param max_logical: the maximum number of boolean logic operations that the derivation chain should contain
    :param min_length: the minimum length of the derivation chain
    :return: a list of promises implementing the constant derivation
    """

    seed()

    # Load Immediate instructions have to be treated in a special way, since they have a very long immediate value.
    # Split the 'li' into 'lui' and 'ori', targeting the latter for obfuscation and keeping aside the 'lui' as a
    # residual.
    if instruction.opcode == 'li':
        oc = Derivation([Promise(ALOps.OR, instruction.r1, instruction.r1, 0, None)],
                        Goal(0, Instruction.ImmediateConstant(12, None, instruction.immediate.value[20:].int_val())))
        # TODO lui obfuscation should happen automatically, but how can we parameterize its?
        leftover = [Promise(OtherOps.LUI,
                            instruction.r1,
                            None,
                            None,
                            Instruction.ImmediateConstant(20, None, instruction.immediate.value[0:20].int_val()))]
    else:
        oc = primers[instruction.opcode](instruction)
        leftover = []

    # Build the obfuscators' pool
    obfuscators = choices(population=logic_obfuscators, k=max_logical) + ([shifter_obf] * max_shifts)
    obfuscators = sample(population=obfuscators, k=randrange(min_length, max_shifts + max_logical))

    # Grow the chain
    for obf in obfuscators:
        new_derivation_step, new_goal = obf(oc.remainder)
        oc = Derivation(oc.chain + [new_derivation_step], new_goal)

    # Terminate chain and return it, adding the eventually present residual
    return oc.chain + [terminator(oc.remainder)] + leftover
