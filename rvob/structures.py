"""
Provide the common structures necessary for syntactic and semantic interpretation of the parsed code.

This module contains a collection of data structures which are used in other parts of the package that must interpret in
some way the contents of some assembly statements or assembler source.
The information contained in this module describes things such as the formal arguments of the statemets, the format of
instructions, etc.

Structures:
Register -- an enumeration of the 32 unprivileged RISC-V integer registers
opcodes -- a dictionary containing information about the number of arguments of each supported instruction, and whether
           or not they are read-only
standard_sections -- a set containing the identifiers of the standard sections that can be found in an assembler source
imm_sizes -- a dictionary associating instruction formats possessing an immediate field with the bit size of such field
"""

from enum import Enum
from typing import Set, Mapping, Tuple

# An enumeration of the 32 unprivileged RISC-V integer registers
class Register(Enum):
    ZERO = 0
    RA = 1
    SP = 2
    GP = 3
    TP = 4
    T0 = 5
    T1 = 6
    T2 = 7
    S0 = 8
    S1 = 9
    A0 = 10
    A1 = 11
    A2 = 12
    A3 = 13
    A4 = 14
    A5 = 15
    A6 = 16
    A7 = 17
    S2 = 18
    S3 = 19
    S4 = 20
    S5 = 21
    S6 = 22
    S7 = 23
    S8 = 24
    S9 = 25
    S10 = 26
    S11 = 27
    T3 = 28
    T4 = 29
    T5 = 30
    T6 = 31

    @staticmethod
    def list():
        return list(map(lambda r: r, Register))

    @staticmethod
    def get_a_regs():
        return [reg for reg in Register if 10 <= reg.value <= 17]


# This is a classification of all the possible opcodes.
# Each opcode is paired with a tuple (<int>, <boolean>) where the int value represents the number of registers used
# by that specific opcode, the boolean value instead tells if we are dealing with a write function (True)
# or a read only one (False)
opcodes: Mapping[str, Tuple[int, bool]] = {
    'lui': (1, True), 'auipc': (1, True), 'jal': (1, True), 'jalr': (2, True), 'lb': (2, True), 'lh': (2, True),
    'lw': (2, True), 'lbu': (2, True), 'lhu': (2, True), 'addi': (2, True), 'slti': (2, True),
    'sltiu': (2, True), 'xori': (2, True), 'ori': (2, True), 'andi': (2, True), 'slli': (2, True),
    'srli': (2, True), 'srai': (2, True), 'lwu': (2, True), 'ld': (2, True), 'addiw': (2, True),
    'slliw': (2, True), 'srliw': (2, True), 'sext.w': (2, True), 'mv': (2, True), 'sraiw': (2, True), 'lr.w': (2, True),
    'lr.d': (2, True), 'add': (3, True), 'sub': (3, True), 'sll': (3, True), 'slt': (3, True),
    'sltu': (3, True), 'xor': (3, True), 'srl': (3, True), 'sra': (3, True), 'or': (3, True), 'and': (3, True),
    'addw': (3, True), 'subw': (3, True), 'sllw': (3, True), 'srlw': (3, True), 'sraw': (3, True), 'mul': (3, True),
    'mulh': (3, True), 'mulhsu': (3, True), "mulhu": (3, True), 'div': (3, True), 'divu': (3, True), 'rem': (3, True),
    'remu': (3, True), 'mulw': (3, True), 'divw': (3, True), 'divuw': (3, True), 'remw': (3, True),
    'remuw': (3, True), 'sc.w': (3, True), 'amoswap.w': (3, True), 'amoadd.w': (3, True),
    'amoxor.w': (3, True), 'amoor.w': (3, True), 'amoand.w': (3, True), 'amomin.w': (3, True), 'amomax.w': (3, True),
    'amominu.w': (3, True), 'amomaxu.w': (3, True), 'sc.d': (3, True), 'amoswap.d': (3, True), 'amoadd.d': (3, True),
    'amoxor.d': (3, True), 'amoor.d': (3, True), 'amoand.d': (3, True), 'amomin.d': (3, True),
    'amomax.d': (3, True), 'amominu.d': (3, True), 'amomaxu.d': (3, True), 'jr': (1, False), 'j': (0, False),
    'beq': (2, False), 'bne': (2, False), 'blt': (2, False), 'bge': (2, False), 'ble': (2, False), 'bltu': (2, False),
    'bgeu': (2, False), 'sb': (2, False), 'sh': (2, False), 'sw': (2, False), 'sd': (2, False), 'li': (1, True),
    'beqz': (1, False), 'bnez': (1, False), 'blez': (1, False), "bgt": (2, False), "not": (2, True), "snez": (2, True),
    'bgez': (1, False), 'bgtu': (2, False), 'bleu': (2, False), 'nop': (0, False), 'call': (0, False),
    'bltz': (1, False), 'bgtz': (1, False), 'negw': (2, True)
    }

# This is a mapping that, for each instruction, associate the relative family name
opcd_family: Mapping[str, str] = {
    'add': 'r', 'addw': 'r', 'and': 'r', 'or': 'r', 'sext.w': 'sext', 'sll': 'r', 'sllw': 'r', 'sub': 'r', 'subw': 'r',
    'xor': 'r', 'xori': 'i', 'jr': 'jr', 'j': 'j', 'beqz': 'bz', 'bnez': 'bz', 'nop': 'nop', 'blez': 'bz', 'beq': 'b',
    'bge': 'b', 'bgeu': 'b', 'blt': 'b', 'ble': 'b', 'bltu': 'b', 'bne': 'b', 'bgt': 'b', 'bgez': 'bz', 'bltz': 'bz',
    'bleu': 'b', 'addi': 'i', 'addiw': 'i', 'andi': 'i', 'auipc': 'u', 'jal': 'j', 'jalr': 'jr', 'ori': 'i',
    'slli': 'i', 'slliw': 'i', 'slt': 'r', 'slti': 'i', 'sltiu': 'i', 'sltu': 'r', 'sra': 'r', 'sraw': 'r', 'srai': 'i',
    'sraiw': 'i', 'srl': 'r', 'srlw': 'r', 'srli': 'i', 'srliw': 'i', 'mul': 'r', 'mulh': 'r', 'mulhsu': 'r',
    'mulhu': 'r', 'div': 'r', 'divu': 'r', 'rem': 'r', 'remu': 'r', 'mulw': 'r', 'divw': 'r', 'divuw': 'r', 'remw': 'r',
    'remuw': 'r', 'lr.w': 'al', 'lb': 'i', 'lbu': 's', 'lh': 's', 'lui': 'u', 'lw': 's', 'sb': 's', 'sh': 's',
    'sw': 's', 'call': 'j', 'sd': 's', 'mv': '_2arg', 'ld': 's', 'li': 'li', 'bgtu': 'b', 'lwu': 's', 'lhu': 's',
    'not': '_2arg', 'negw': '_2arg', 'sc.w': 'as', 'amoswap.w': 'as', 'amoadd.w': 'as', 'amoxor.w': 'as',
    'amoor.w': 'as', 'amoand.w': 'as', 'amomin.w': 'as', 'amomax.w': 'as', 'amominu.w': 'as', 'amomaxu.w': 'as',
    'lr.d': 'al', 'sc.d': 'as', 'amoswap.d': 'as', 'amoadd.d': 'as', 'amoxor.d': 'as', 'amoor.d': 'as', 'amoand.d': 'as',
    'amomin.d': 'as', 'amomax.d': 'as', 'amominu.d': 'as', 'amomaxu.d': 'as', 'bgtz': 'bz', 'snez': 'snez'
    }

# The standard section's names
# Conventionally, the sections in which a binary object gets segmented are: data, BSS and text.
standard_sections: Set[str] = {".text", ".data", ".bss"}

# Registers
registers = ["ra", "sp", "gp", "tp", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "s0", "s1", "s2", "s3", "s4",
             "s5", "s6", "s7", "s8", "s9", "s10", "s11", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7",
             "zero", "reg_err", "unused"]

# registers saved by the callee
calle_saved_regs: Set[Register] = {Register.SP, Register.S0, Register.S1, Register.S2, Register.S3, Register.S4,
                                   Register.S5, Register.S6, Register.S7, Register.S8, Register.S9, Register.S10,
                                   Register.S11}

not_modifiable_regs: Set[Register] = {Register.GP, Register.TP, Register.ZERO}

# Dictionary of immediate formats with associated immediate field size
imm_sizes: Mapping[str, int] = {
    "i": 12,
    "s": 12,
    "b": 12,
    "bz": 12,
    "u": 20,
    "j": 20,
    "li": 32
    }

