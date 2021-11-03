import json
from typing import List, Tuple, Dict, Set
from networkx import DiGraph
import rvob.rep.base
import rvob.rep.fragments
import rvob.analysis
import rvob.registerbinder
import rvob.setup_structures
import rvob.obf.obfuscator as obfuscator
import rvob.obf.const_derivation
import rvob.garbage_inserter as garbage_inserter
import rvob.analysis.heatmaps as heatmaps
import rvob.scrambling as scrambling
import rvob.analysis.tracer as tracer
from rvob.structures import Register
from rvob.obf.obfuscator import NotEnoughtRegisters, NotValidInstruction
from os import path
import argparse

heat_map = None
heat_file = None
metrics_file = None
trace_heat_map: Dict[int, Tuple[List[int], tracer.SupplementInfo]] = None
cfg: DiGraph = None



def get_args():

    parser = argparse.ArgumentParser(description="DETON")

    parser.add_argument(
        "File",
        metavar="File path input",
        help="The path of the file in .json format to process",
        nargs='?',
        default='q',
        type=str)

    parser.add_argument(
        '-e', '-entry',
        metavar="File entry point",
        help="Entry point of the program to process",
        nargs='?',
        default='',
        const='',
        type=str)

    parser.add_argument(
        '-b', '-benchmark',
        action = 'store_true',
        default=False,
        help = "Execution of all benchmark file")

    parser.add_argument(
        "RS",
        metavar="Repetition Scrambling",
        help="Number of times the register scrambling procedure is executed",
        type=int)

    parser.add_argument(
        "RO",
        metavar="Repetition Obfuscate",
        help="Number of times the constant obfuscation procedure is executed",
        type=int)

    parser.add_argument(
        "RG",
        metavar="Repetition Garbage",
        help="Number of times the garbage instruction procedure is executed",
        type=int)

    parser.add_argument(
        "SG",
        metavar="Size block Garbage",
        help="Size of the block of garbage instruction to insert",
        type=int)

    parser.add_argument(
        "H",
        metavar="Heat",
        help="Max heat for the heatmap",
        type=int)

    parser.add_argument(
        "Output",
        metavar="Output file path",
        help="The output file path in .s format (example: /User/file.s )",
        nargs='?',
        default='q',
        type=str)

    parser.add_argument(
        '-m', '-metrics',
        action='store_true',
        default=False,
        help="Generate the metrics file of the process located in metrics directory")

    return parser.parse_args()


def write_heat(first: bool, frag: Tuple[int, List[int], int] = None):
    """
    this function is used to write the obtained results to the output files
    @param first: True if we are in the writing phase before the application of the techniques, False if we are in the
                  writing phase after the application of techniques
    @param frag: a tuple containing infos about the ValueBlocks fragmentation
    """
    global trace_heat_map
    global heat_file
    global metrics_file

    # write the heatmap for each line indicating also in the order: if the instruction is an inserted one, the original
    # first register used, the currently used first register and finally the instruction's op code
    for i in range(len(trace_heat_map.keys())):
        heat_file.write(
            str(i) + ": " + str(trace_heat_map[i][0]) + " i:" + str(trace_heat_map[i][1].inserted) + " o_r: " + str(
                trace_heat_map[i][1].o_reg) + " n_r: " + str(trace_heat_map[i][1].n_reg) + " opcd: " + str(
                trace_heat_map[i][1].op_code) + "\n")

    # evaluates the mean heat of the analyzed program
    mean_heat = [0] * len(Register)
    for val in trace_heat_map.values():
        for i in range(len(mean_heat)):
            mean_heat[i] += val[0][i]
    trace_length = len(trace_heat_map.keys())
    for i in range(len(mean_heat)):
        mean_heat[i] //= trace_length
    if first:
        metrics_file.write("Mean heat before: " + str(mean_heat) + "\n")
        metrics_file.write("Executed instructions before: " + str(len(trace_heat_map.keys())) + "\n")
    else:
        metrics_file.write("Mean heat after: " + str(mean_heat) + "\n")
        metrics_file.write("Executed instructions after: " + str(len(trace_heat_map.keys())) + "\n")

    # compute some additional metrics about the ValueBlocks fragmentation
    if frag is not None:
        # The frag tuple contains the following value:
        # [0] mean fragmentation
        # [1] list of the fragmented ValueBlock with fragment number for each ValueBlock
        # [2] number of original ValueBlock
        metrics_file.write("Mean fragmentation: " + str(frag[0]) + "\n")
        metrics_file.write("Number of original ValueBlock: " + str(frag[2]) + "\n")
        metrics_file.write("List of fragmented ValueBlock: " + str(frag[1]) + "-> " + str(len(frag[1])) + "\n")


def analyze_node(node: DiGraph.node, frag_list: List[int]) -> int:
    """
    The function analyzes a node in search of the fragments inside it.
    @param node: the node to be analyzed
    @param frag_dict: the dictionary used to collect the fragment associated, thanks to the group_id, to the same
                      original ValueBlock. The dict use as key the group_id and as value a set of the register used
                      by the fragment with the same group_id
    @param frag_list: the list containing, for each original ValueBlock, the number of fragment that compose it.A
                      ValueBlock that has never been split has the value 1.
    @return: the number of original ValueBlocks found inside the node
    """

    # a counter of the blocks inside the node counting as single all the fragments having the same group_id
    block_num: int = 0

    # the dictionary used to collect the fragment associated, thanks to the group_id, to the same original
    # ValueBlock. The dict use as key the group_id and as value a set of the register used by the fragment with the
    # same group_id
    frag_dict: Dict[int, Set[Register]] = {}

    for (reg, v) in node['reg_bind'].items():
        v = [blk for blk in v if not blk.inserted]  # eliminate block added by some garbage instruction
        for block in v:
            if block.group_id is not None:
                # if group_id isn't None means the block is a fragment of a bigger block
                try:
                    # if a fragment associated to this block's group_id is already found add the used register to the
                    # dictionary
                    frag_dict[block.group_id].add(reg)
                except KeyError:
                    # if this is the first fragment of the original ValueBlock associated to this group_id then create a
                    # a new entry in the dictionary with the used register and increment by 1 the blocks counter
                    frag_dict[block.group_id] = {reg}
                    block_num += 1
            else:
                # if the block has its group_id set to None means that this block has never been split, so simply
                # increment by 1 the blocks counter and add 1 to the list containing the numbers of fragments of each
                # program's block
                block_num += 1
                frag_list.append(1)
    # for each value inside the frag_dict insert inside the frag_list the number of different registers used by the
    # fragments with the same group_id
    for val in frag_dict.values():
        frag_list.append(len(val))
    return block_num


def calc_fragmentation():
    """
    This calculates the fragmentation of the ValueBlocks
    @return: a tuple containing: at [0] the mean of the fragmentation level of the ValueBlocks, at [1] a list of the
             number of fragments, but only for the ValueBlocks that have been split at least one time, at [2] the number
             of ValueBlocks inside the program, but counting as 1 all the  fragments having the same group_id, because
             they are all fragments of a single original ValueBlock
    """

    frag_list: List[int] = []  # indicates how many fragments have each block of the program
    block_num: int = 0

    for nd_id in cfg.nodes:
        node = cfg.nodes[nd_id]
        if 'external' not in node:
            block_num += analyze_node(node, frag_list)

    src_list = [elm for elm in frag_list if elm > 1] # create the list of fragments of only splitted ValueBlocks
    mean_fragmentation = sum(frag_list)
    mean_fragmentation //= len(frag_list)

    return mean_fragmentation, src_list, block_num


def do_scrambling(iter_num: int, heat):
    """
    this does the scrambling techniques, that has two sub-operation the splitting that divides a ValueBlock into two
    fragment where the second one change the used register, and the substitute that changes the register used inside a
    ValueBlock
    @param iter_num: the number of iterations to do
    """
    global heat_map
    failed_splitting = 0
    failed_substitute = 0

    for t in range(iter_num):
        heat_map = heatmaps.register_heatmap(cfg, heat)

        # try to do a register substitution
        ret = scrambling.split_value_blocks(cfg, heat_map, heat)
        if ret == -1:
            failed_splitting += 1

        # try to substitute the usage of a register
        ret = scrambling.substitute_reg(cfg, heat_map, heat)
        if ret == -1:
            failed_substitute += 1

    print("Splitting failure rate: " + str(failed_splitting / iter_num * 100) + "%")
    print("Substitution failure rate: " + str(failed_substitute / iter_num * 100) + "%")


def do_garbage(iter_num: int, garb_par: int):
    """
    this perform the garbage instructions insertion
    @param iter_num: the number of iteration to do
    """
    for t in range(iter_num):
        garbage_inserter.insert_garbage_instr(cfg, None, garb_par)


def do_obfuscate(iter_num: int):
    """
    this performs the constant obfuscation technique
    @param iter_num: the number of iterations to do
    """
    failed = 0
    for t in range(iter_num):
        for z in range(5):
            try:
                obfuscator.obfuscate(cfg)
                break
            except (NotEnoughtRegisters, NotValidInstruction):
                if z == 4:
                    failed += 1
    print("Obfuscate failure rate: " + str(failed / iter_num * 100) + "%")


def apply_techniques(heat, scrambling_repetition, obfuscate_repetition, garbage_repetition, garb_par):
    """
    This function calls all the sub-functions that applies the obfuscation techniques (Scrambling, garbage instructions
    insertion and constants obfuscation)
    """

    do_obfuscate(obfuscate_repetition)
    do_garbage(garbage_repetition, garb_par)
    do_scrambling(scrambling_repetition, heat)


def execute(name: str, entry: str, heat: int, scrambling_repetition: int, obfuscate_repetition: int, garbage_repetition: int, garb_size: int, output: str, bench: bool, metric: bool):

    global heat_map
    global heat_file
    global metrics_file
    global trace_heat_map
    global cfg

    # Load the json file
    rel = path.dirname(__file__)
    if bench==True:
        src = rel + '/benchmark/benchmark_file/' + name + '.json'
        file = open(src)
        src = rvob.rep.fragments.load_src_from_maps(json.load(file))
    else:
        src = name
        file = open(src)
        src = rvob.rep.fragments.load_src_from_maps(json.load(file))

    # build the cfg of the program
    if entry:
        cfg = rvob.analysis.cfg.build_cfg(src, entry)
    else:
        cfg = rvob.analysis.cfg.build_cfg(src)

    # Make some setup operations, computing the nodes requirement contracts and filling the nodes register binder
    rvob.setup_structures.setup_contracts(cfg)
    rvob.setup_structures.sanitize_contracts(cfg)
    rvob.setup_structures.organize_calls(cfg)
    rvob.registerbinder.bind_register_to_value(cfg)

    # Initialize the program heatmap
    heat_map = heatmaps.register_heatmap(cfg, heat)

    # create the output files that will contains the metrics
    if metric==True:
        if bench==True:
            dst = rel + '/benchmark/benchmark_output/' + name + ".txt"
            metric_dst = rel + '/benchmark/benchmark_output/' + name + "_metrics.txt"
        else:
            dst = rel + '/metrics/data.txt'
            metric_dst = rel + '/metrics/data_metrics.txt'
        heat_file = open(dst, "w")
        metrics_file = open(metric_dst, "w")

        # write the value of the metrics for the plain program
        heat_file.write("Baseline:\n")
        trace_out = tracer.get_trace(cfg)
        trace_heat_map = trace_out[1]
        write_heat(first=True)

    # Apply the obfuscation techniques
    apply_techniques(heat, scrambling_repetition, obfuscate_repetition, garbage_repetition, garb_size)

    # Write the value of the metrics for the obfuscated program
    if metric==True:
        trace_out = tracer.get_trace(cfg, ex_path=trace_out[0])
        trace_heat_map = trace_out[1]
        heat_file.write("\n\n\nObfuscated version:\n")
        write_heat(False, calc_fragmentation())
        heat_file.close()
        metrics_file.close()

    # Write the output file
    if bench==True:
        dirct = rel + '/benchmark/benchmark_output/' + name + ".s"
    else:
        dirct = output
    out = open(dirct, 'w+')
    out.write(str(src))


def main():
    args = get_args()

    benchmarks = [('bubblesort', ''), ('crc_32', ''), ('dijkstra_small', ''), ('fibonacci', ''),
                  ('matrixMul', ''), ('patricia', 'bit'), ('quickSort', ''), ('sha', 'sha_transform')]

    if args.b == True:
        for elem in benchmarks:
            print("\n\033[1m\033[91mI'm Testing " + elem[0] + ':\033[0m')
            execute(elem[0], elem[1], args.H, args.RS, args.RO, args.RG, args.SG, args.Output, args.b, args.m)
    else:
        if args.File == 'q' or args.Output == 'q':
            print("Input or Output file path missing, please see -h option to more information")
        else:
            execute(args.File, args.e, args.H, args.RS, args.RO, args.RG, args.SG, args.Output, args.b, args.m)


if __name__ == "__main__":
    main()
