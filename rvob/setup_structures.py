from networkx import DiGraph, neighbors, reverse, simple_cycles

from rep.base import Instruction
from rep.fragments import FragmentView
from rvob.structures import opcodes
from rvob.analysis.cfg import Transition
from structures import Register, calle_saved_regs, not_modifiable_regs
from registerbinder import bind_register_to_value


def setup_contracts(cfg: DiGraph):
    """
    Function responsible for the creation of the contracts of all the nodes of a specific Cfg.
    It uses the fill_contract function called upon all the nodes one by one.
    :param cfg: The DiGraph representing the cfg
    :return: void
    """

    for node in cfg.nodes:
        if 'provides' not in cfg.nodes[node]:
            cfg.nodes[node]['provides'] = set()
        if 'requires' not in cfg.nodes[node]:
            cfg.nodes[node]['requires'] = set()
            if 'external' in cfg.nodes[node]:
                cfg.nodes[node]['requires'].add(Register.SP)
                # cfg.nodes[node]['requires'].add(Register.FP)

    visited = set()
    # Recovers the leaves of our tree
    remaining_nodes = get_leaf_nodes(cfg)

    # Core loop of the function, its behaviour is:
    # 1) check if we still have nodes that need to be analyzed, if not end
    # 2) pop the first node of the stack, put it in the visited list, create the contract for this node.
    # 3) recover its parent node and if it's not in the stack and it has never been visited append it to the stack
    # 4) start from point 1
    while len(remaining_nodes) > 0:
        node = remaining_nodes.pop(0)
        visited.add(node)
        try:
            # We need to check if the node we're dealing with has a start attribute, otherwise we ignore the node and
            # skip to the next one (should happen only at the end when dealing with the head of the cfg)
            fill_contract(cfg, node)

        except KeyError:
            continue
        for parent in reverse(cfg, False).neighbors(node):
            if parent not in remaining_nodes and parent not in visited:
                remaining_nodes.append(parent)

    sanitize_contracts(cfg)


def set_callee_saved_regs(cfg: DiGraph):
    callee_used = set()
    for node in cfg.nodes().values():
        if 'reg_bind' in node:
            for reg in node['reg_bind']:
                if reg in calle_saved_regs:
                    callee_used.add(reg)

    callee_unused = set()

    for reg in calle_saved_regs:
        if reg not in callee_used:
            callee_unused.add(reg)

    for node in get_leaf_nodes(cfg):
        cfg.nodes[node]['provides'] = cfg.nodes[node]['provides'].union(callee_unused)

    setup_contracts(cfg)
    bind_register_to_value(cfg)


def fill_contract(cfg: DiGraph, node_id: int):
    """
    This function is responsible for creating the contract of a single node and linking it to the node itself.
    A contract is composed by two different sets
    1) provides contains all the registers written in this node's code block
    2) requires contains all the registers that are read in this node's code block
    Initially requires set contains all the registers in the requires sets of the node's children, each time that a
    register is written is also removed from the set, otherwise if a register is written then we add it to the set
    :param cfg: The DiGraph representing the cfg
    :param node_id: the id of the node analized
    :return: void
    """
    provides = set()
    requires = set()
    errors = set()

    children = get_children(cfg, node_id)
    for child in children:
        for elem in cfg.nodes[child]["requires"]:
            requires.add(elem)

    if 'external' not in cfg.nodes[node_id]:

        block: FragmentView = cfg.nodes[node_id]["block"]

        for i in range(block.end - 1, block.begin - 1, -1):
            current_line = block[i]
            if type(current_line) == Instruction:
                opcode = current_line.opcode
                r1 = current_line.r1
                r2 = current_line.r2
                r3 = current_line.r3
                # Different actions are taken depending on the type of opcode we are analizing, if we have a read only
                # opcode provides set will not be modified, otherwise we make sure to deal with that set too
                if opcode in opcodes.keys():
                    if opcodes[opcode][1]:
                        provides.add(r1)
                        if r1 in requires:
                            requires.remove(r1)
                        if r2 not in requires:
                            requires.add(r2)
                        if r3 not in requires:
                            requires.add(r3)
                    else:
                        if r1 not in requires:
                            requires.add(r1)
                        if r2 not in requires:
                            requires.add(r2)
                        if r3 not in requires:
                            requires.add(r3)
                else:
                    errors.add(opcode)

        # A little bit of error management, if we have some opcodes that are not classified is better to raise an
        # exception instead of ignoring them and having to deal with bigger problems later
        if len(errors) > 0:
            raise Exception("Encountered one or more unexpected opcodes, {}".format(errors))

        # no need to keep 'unused' in our contracts
        if None in requires:
            requires.remove(None)
        if None in provides:
            requires.remove(None)

    # If the node we are dealing with is the return node of a function then it provides registers A0 and A1
    for edge in cfg.edges:
        data = cfg.get_edge_data(edge[0], edge[1])
        if edge[0] == node_id and data["kind"] == Transition.RETURN:
            provides.add(Register.A0)
            provides.add(Register.A1)

    cfg.nodes[node_id]['requires'] = cfg.nodes[node_id]['requires'].union(requires)
    cfg.nodes[node_id]['provides'] = cfg.nodes[node_id]['provides'].union(provides)


def get_children(cfg: DiGraph, node_id: int):
    """
    Utility function, recovers the children of a specific node, if the head of the tree should appear as a child it
    will be ignored
    :param cfg: The DiGraph representing the cfg
    :param node_id: Id of the node
    :return: list of children
    """
    children = []
    for child in neighbors(cfg, node_id):
        children.append(child)
    if 0 in children:
        children.remove(0)
    return children


def is_sublist(sublist: list, main_list: list):
    """
    Utility functions, given two strings checks if the first one is totally contained in the second one
    :param sublist: First list
    :param main_list: List that could contain the other list
    :return: Boolean value
    """
    if len(sublist) >= len(main_list):
        return False
    else:
        for elem in sublist:
            if elem not in main_list:
                return False
    return True


def sanitize_contracts(cfg: DiGraph):
    """
    This function sanitizes all the contracts, firstly it finds all the cycles in the graph, then
    it copies the cycle head's "requires" contract into each node of the cycle
    :param cfg: The DiGraph representing the cfg
    :return: void
    """
    cycles = list(simple_cycles(cfg))

    for elem in list(cycles):
        if 0 in elem:
            cycles.remove(elem)

    for elem in list(cycles):
        for elem2 in list(cycles):
            if is_sublist(elem, elem2):
                cycles.remove(elem)
                break

    for cycle in cycles:
        req = cfg.nodes[cycle[0]]['requires']
        for node in cycle:
            cfg.nodes[node]['requires'] = req


def get_leaf_nodes(cfg: DiGraph):
    nodes = []
    for node in reverse(cfg, False).neighbors(0):
        if cfg.out_degree(node) == 1:
            nodes.append(node)

    return nodes


def get_node_from_line(cfg: DiGraph, line_value: int):
    for node in cfg.nodes.values():
        if 'block' in node:
            if node['block'].begin <= line_value <= node['block'].end:
                return node
    return None


def get_free_regs(cfg: DiGraph, line_value: int):
    # Utility function, given a cfg and a line value returns all the available registers at that point of the program
    used_regs = []
    unused_regs = Register.list()
    node = get_node_from_line(cfg, line_value)

    if node is None:
        return []

    for reg in Register:
        if reg in node['reg_bind']:
            for bind in node['reg_bind'][reg]:
                if bind.init_line <= line_value <= bind.end_line:
                    used_regs.append(reg)
                    break

    for reg in used_regs:
        if reg in unused_regs:
            unused_regs.remove(reg)

    for reg in not_modifiable_regs:
        if reg in unused_regs:
            unused_regs.remove(reg)

    return unused_regs


def get_call_edges(cfg: DiGraph):
    edges = []
    for edge in cfg.edges(data=True):
        if edge[2]['kind'] == Transition.CALL:
            edges.append(edge)
    return edges


def get_return_edges(cfg: DiGraph):
    edges = []
    for edge in cfg.edges(data=True):
        if edge[2]['kind'] == Transition.RETURN:
            edges.append(edge)
    return edges


def get_track_return(cfg: DiGraph, starting_edge) -> list:
    """
    Given a starting edge this function returns a list containing the track from the node where the edge generates
    through the next RETURN edge. The list is given in reverse order
    :param cfg:
    :param starting_edge:
    :return:
    """
    track = []
    visited_edges = []
    unvisited_edges = [starting_edge]
    ending_node = starting_edge[0]
    call_nums = 0

    while len(unvisited_edges) > 0:
        curr_edge = unvisited_edges.pop()
        if curr_edge[0] not in track:
            track.append(curr_edge[0])

        for edge in cfg.out_edges(curr_edge[1], data=True):
            if edge not in visited_edges and edge[2]['kind'] != Transition.RETURN:
                unvisited_edges.append(edge)

            if edge[2]['kind'] == Transition.CALL:
                call_nums += 1
            if edge[2]['kind'] == Transition.RETURN and not call_nums and ending_node != edge[0]:
                ending_node = edge[0]
            if edge[2]['kind'] == Transition.RETURN and call_nums and edge not in visited_edges:
                call_nums -= 1
                unvisited_edges.append(edge)

        visited_edges.append(curr_edge)

    track.append(ending_node)
    track.reverse()
    return track


def organize_calls(cfg: DiGraph):
    """
    This function takes all the external nodes and foreach node modifies the requires set adding all the A regs
    that are written in the nodes found between the external one and a CALL edge.
    :param cfg:
    :return:
    """
    nodes = get_external_nodes(cfg)
    ret_regs = {Register.A0, Register.A1}
    for node in nodes:
        track = get_call_track(cfg, node)
        add_set = set()
        for track_node in track:
            if 'external' not in cfg.nodes[track_node]:
                add_set = add_set.union(get_used_a_regs(cfg, track_node))

        cfg.nodes[node[0]]['requires'] = cfg.nodes[node[0]]['requires'].union(add_set)
        cfg.nodes[node[0]]['provides'] = cfg.nodes[node[0]]['provides'].union(ret_regs)


def get_call_track(cfg: DiGraph, node):
    """
    Returns a list containing all the nodes that are placed between the given one and the first CALL edge found
    going upward
    :param cfg:
    :param node:
    :return:
    """
    track = []
    unvisited_edges = set()
    visited_edges = []
    for edge in cfg.in_edges(node[0]):
        track.append(edge[0])
        for edge_t in cfg.in_edges(edge[0]):
            unvisited_edges.add(edge_t)

    while len(unvisited_edges) > 0:
        curr_edge = unvisited_edges.pop()
        if curr_edge[0] not in track:
            track.append(curr_edge[0])
        if cfg.get_edge_data(curr_edge[0], curr_edge[1])['kind'] == Transition.CALL:
            return track

        for edge in cfg.in_edges(curr_edge[0]):
            if edge not in visited_edges:
                unvisited_edges.add(edge)

        visited_edges.append(curr_edge)

    if node in track:
        track.remove(node)

    return track


def get_external_nodes(cfg: DiGraph):
    """
    Retrieves list of nodes marked as external
    :param cfg:
    :return:
    """
    nodes = []
    for node in cfg.nodes(data=True):
        if 'external' in node[1]:
            nodes.append(node)
    return nodes


def get_used_a_regs(cfg: DiGraph, node_id: int):
    a_regs = Register.get_a_regs()
    regs = set()
    block: FragmentView = cfg.node[node_id]["block"]
    for i in range(block.end - 1, block.begin - 1, -1):
        current_line = block[i]
        if type(current_line) == Instruction:
            opcode = current_line.opcode
            r1 = current_line.r1
            if r1 in a_regs and opcode in opcodes.keys():
                if opcodes[opcode][1]:
                    regs.add(r1)
    return regs
