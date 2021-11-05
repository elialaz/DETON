from enum import Enum
from typing import List

from networkx import DiGraph
from random import randint, choices

from rvob.obf.obfuscator import NotEnoughRegisters
from setup_structures import get_free_regs
from structures import Register, not_modifiable_regs
from rvob.registerbinder import bind_register_to_value
from rep.instruction_generator import garbage_inst
from analysis import heatmaps

line_heat_map: List[int]


def sorting_function(val: Enum):
    return line_heat_map[val.value]


def establish_write_reg(free_reg: List[Enum], needed: int) -> List[Enum]:
    write_reg: List[Enum] = list()

    if len(free_reg) >= needed:
        return [free_reg[i] for i in range(needed)]
    else:
        return free_reg


def establish_read_reg(all_reg: List[Enum], needed: int) -> List[Enum]:
    needed *= 3
    read_reg: List[Enum] = list()
    for reg in all_reg:
        if line_heat_map[reg.value] == 0:
            read_reg.append(reg)
        elif len(read_reg) < needed:
            read_reg.append(reg)
        else:
            break
    return read_reg


def insert_garbage_instr(cfg: DiGraph, node: int = None, block_size: int = None, line_num: int = None):
    """
    This function adds a block of garbage instructions into a node of the graph
    @param line_num:
    @param cfg: the graph that represents the program
    @param node: the graph's node to which apply the function
    @param block_size: the number of garbage instructions that compose the block
    """

    if block_size is None:
        block_size = randint(1, 10)
    if node is None:
        node = randint(1, cfg.number_of_nodes() - 1)
    while 'external' in cfg.nodes[node]:
        node = randint(1, cfg.number_of_nodes() - 1)
    if line_num is None or line_num < cfg.nodes[node]['block'].begin or line_num >= cfg.nodes[node]['block'].end:
        line_num = randint(cfg.nodes[node]["block"].begin, cfg.nodes[node]["block"].end - 1)
    global line_heat_map
    try:
        line_heat_map = heatmaps.register_heatmap(cfg, 50)[line_num]
    except KeyError:
        line_heat_map = [0]*len(Register.list())
    free_regs = list(get_free_regs(cfg, line_num))
    free_regs.sort(key=sorting_function)
    all_regs = list(set(Register.list()) - not_modifiable_regs)
    all_regs.sort(key=sorting_function)

    instr_list = choices(list(garbage_inst.keys()), k=block_size)
    if len(free_regs) == 0 or len(all_regs) <= 1:
        raise NotEnoughRegisters
    for instr in instr_list:
        statement = garbage_inst[instr](free_regs, all_regs)
        statement.inserted = True
        cfg.nodes[node]["block"].insert(line_num, statement)
        bind_register_to_value(cfg, node)
        line_num += 1
