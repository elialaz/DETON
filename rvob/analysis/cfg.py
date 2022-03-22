from __future__ import annotations

from enum import Enum
from functools import reduce
from itertools import chain, tee, repeat, zip_longest
from operator import attrgetter
from typing import Iterator, FrozenSet, List, Tuple, Optional, Mapping, Hashable, Iterable, MutableMapping, \
    NamedTuple, Dict, Union

from networkx import DiGraph, simple_cycles, restricted_view, all_simple_paths, relabel_nodes, dfs_preorder_nodes, \
    Graph, convert_node_labels_to_integers
from networkx.classes.graphviews import subgraph_view
from networkx.utils import generate_unique_node

from rep.base import Instruction, Directive, ASMLine, to_line_iterator
from rep.fragments import Source, FragmentView, CodeFragment


class InvalidCodeError(Exception):
    """An error raised when a code fragment doesn't follow some expected layout or assumption."""

    pass


class Transition(Enum):
    """
    A type of control flow progression.

    Each member carries some information characterizing the type of advancement:

    - resolve_symbol: whether the progression implies a symbol resolution;
    - branching: whether progressing in this direction is conditional.
    """

    SEQ = (False, False)
    """Sequential advancement: PC advances linearly, towards the instruction that follows."""

    U_JUMP = (True, False)
    """Unconditional jump: a simple local unconditional jump."""

    C_JUMP = (True, True)
    """ Conditional jump: a simple local conditional jump. An alternate sequential execution path exists."""

    CALL = (True, False)
    """Procedure call: non-local jump to an internal or external procedure."""

    RETURN = (False, False)
    """Return: return jump from a call."""

    def __new__(cls, *args, **kwargs):
        # Calculate a unique ID to avoid aliasing
        id_val = len(cls.__members__) + 1
        instance = object.__new__(cls)
        instance._value_ = id_val
        return instance

    def __init__(self, resolve_symbol: bool, branching: bool):
        self.resolve_symbol = resolve_symbol
        self.branching = branching

    def __repr__(self):
        return '<%s.%s: (%s,%s)>' % (self.__class__.__name__, self.name, self.resolve_symbol, self.branching)


jump_ops: Mapping[str, Transition] = {
    "call": Transition.CALL,
    "jr": Transition.RETURN,
    "j": Transition.U_JUMP,
    "jal": Transition.CALL,
    "jalr": Transition.CALL,
    "beq": Transition.C_JUMP,
    "beqz": Transition.C_JUMP,
    "bne": Transition.C_JUMP,
    "bnez": Transition.C_JUMP,
    "blt": Transition.C_JUMP,
    "bltz": Transition.C_JUMP,
    "bltu": Transition.C_JUMP,
    "ble": Transition.C_JUMP,
    "blez": Transition.C_JUMP,
    "bleu": Transition.C_JUMP,
    "bgt": Transition.C_JUMP,
    "bgtz": Transition.C_JUMP,
    "bgtu": Transition.C_JUMP,
    "bge": Transition.C_JUMP,
    "bgez": Transition.C_JUMP,
    "bgeu": Transition.C_JUMP
}
"""Mapping between control flow manipulation instructions and the kind of transition that they introduce."""


class BasicBlock:
    """
    A program's basic block.

    Each member of this class is a code container, decorated with additional metadata that would have to be extracted
    every time from bare assembly.

    Members of this class are identified by some hashable object. Uniqueness is not enforced.

    :ivar identifier: the hashable identifier for the basic block
    :ivar labels: labels representing marking the entry point for the basic block, if any
    :ivar code: the code fragment containing the actual code
    :ivar outgoing_flow: the shape of the outgoing flow and its destination, in the format returned by the
          execution_flow_at function
    """

    identifier: Hashable
    labels: List[str]
    code: CodeFragment
    outgoing_flow: Tuple[Transition, Optional[str]]

    def __init__(self, fragment: CodeFragment, block_id: Hashable):
        starting_line = fragment[fragment.begin]
        ending_line = fragment[fragment.end - 1]

        if not isinstance(ending_line, Instruction):
            raise InvalidCodeError("A basic block must always end with an instruction.")

        self.identifier = block_id
        self.labels = list(starting_line.labels)
        self.code = fragment
        self.outgoing_flow = execution_flow_at(ending_line)

    def __repr__(self):
        return "BasicBlock(" + repr(self.code) + ", " + repr(self.identifier) + ")"

    def __str__(self):
        return "---\nBB ID: " + str(self.identifier) + "\nLabels: " + str(self.labels) + "\n\n" + str(self.code) + \
               "\nOutgoing exec arc: " + str(self.outgoing_flow) + "\n---\n"


class ProcedureCall(NamedTuple):
    """
    A procedure call.

    Calls are represented in terms of caller, callee and point where execution is expected to return
    (`confluence point`).
    """

    caller: Hashable
    callee: Hashable
    confluence_point: Hashable


class LocalGraph:
    """
    A CFG representing some part of a program.

    A local graph is characterized by one or more entry-points, a digraph, some terminal nodes and a collection of
    "arcs" directed to some external procedures. All entering execution flows proceed from the entry-points and reach
    the terminal nodes, unless an external call diverges.

    A local graph may not be connected, with disconnected components being confluence point for flows returning from
    external calls. The information necessary to obtain a connected graph can be extracted by resolving the external
    calls.

    Internal calls are represented by edges connecting caller and confluence point, labeled with the `CALL` transition
    kind and with a `caller` attribute indicating the called procedure's symbolic name.

    No check is performed on the consistency of the information used to instantiate these objects.
    """

    entry_labels: List[str]
    entry_point_ids: List[Hashable]
    graph: DiGraph
    external_calls: List[ProcedureCall]
    terminal_nodes_ids: List[Hashable]

    def __init__(self,
                 entry_points: Iterable[Hashable],
                 graph: DiGraph,
                 calls: Iterable[ProcedureCall],
                 terminals: Iterable[Hashable]):
        """
        Construct a new local graph.

        :param entry_points: a collection of node IDs indicating the entry-points
        :param graph: the local graph, as a NetworkX DiGraph
        :param calls: a collection of purportedly external calls
        :param terminals: a collection of node IDs indicating which are the terminal nodes
        """

        # Set up the entry-point information
        self.entry_point_ids = list(entry_points)

        # Characterize the function in terms of a graph and the nested calls it performs
        self.graph = graph
        self.external_calls = list(calls)

        # Keep track of the terminal nodes
        self.terminal_nodes_ids = list(terminals)

    @property
    def entry_labels(self) -> List[str]:
        labeling_lists = map(lambda n: self.graph.nodes[n]['labels'], self.entry_point_ids)
        return list(chain.from_iterable(labeling_lists))

    def get_symbol_table(self) -> Mapping[str, Hashable]:
        """
        Return a mapping between entry labels and entry-points' node IDs.

        :return: a mapping from public labels to their entry-point IDs
        """

        return {lab: nid for nid in self.entry_point_ids for lab in self.graph.nodes[nid]['labels']}

    def merge(self, other: LocalGraph) -> LocalGraph:
        """
        Merge this local graph with `other` into a new local graph.

        The resulting local graph has the union of entry-points, graphs and terminals. A cross-lookup is performed
        between the two objects in an attempt to resolve external calls that may become internal. Newly found internal
        calls are converted into graph edges of kind `Transition.CALL` with attribute `callee` pointing to one of the
        local entry-points. The remaining external calls are merged and included in the new object.

        :param other: the other graph that takes part in the operation
        :return: a local graph obtained by merging self with other
        :raise InvalidCodeError: when there is a naming clash between entry labels of the two graphs
        """

        self_symbols = self.get_symbol_table()
        other_symbols = other.get_symbol_table()

        # Look for entry labels collisions. If the original code is rational, this shouldn't happen.
        if not frozenset(self_symbols).isdisjoint(other_symbols):
            raise InvalidCodeError("Labeling clash")

        # Remap the other graph, entry-point IDs, callers and terminals
        other = remap_local_graph(other, solve_graph_collision(self.graph, other.graph))

        # Start merging stuff
        merged_eps = chain(self.entry_point_ids, other.entry_point_ids)
        merged_graph = self.graph.copy()
        merged_graph.update(other.graph)
        merged_terminals = chain(self.terminal_nodes_ids, other.terminal_nodes_ids)

        # TODO re-implement with partitions
        sec1, sec2 = tee(self.external_calls)
        oec1, oec2 = tee(other.external_calls)
        # Merge external calls
        merged_calls = chain(filter(lambda c: c.callee not in other_symbols, sec1),
                             filter(lambda c: c.callee not in self_symbols, oec1))
        # Resolve internal calls
        for ic in filter(lambda c: c.callee in other_symbols, sec2):
            merged_graph.add_edge(ic.caller, ic.confluence_point, kind=Transition.CALL, callee=ic.callee)
        for ic in filter(lambda c: c.callee in self_symbols, oec2):
            merged_graph.add_edge(ic.caller, ic.confluence_point, kind=Transition.CALL, callee=ic.callee)

        return LocalGraph(merged_eps, merged_graph, merged_calls, merged_terminals)


def solve_graph_collision(ref: Graph, other: Graph) -> Dict[Hashable, Hashable]:
    """
    Given two NetworkX graphs, find eventual name collisions between nodes and propose a solution.

    The proposed solution comes in the form of a dictionary, containing remapping rules that could be applied to the
    second graph in order to solve any clash.

    :param ref: a reference graph
    :param other: the other graph, on which renaming has to be performed
    :return: a partial mapping that solves eventual clashes once applied on the second graph
    """

    id_clashes = ref.nbunch_iter(other.nodes)
    return {idc: generate_unique_node() for idc in id_clashes}


def remap_local_graph(cfg: LocalGraph, mapping: Dict[Hashable, Hashable]) -> LocalGraph:
    """
    Given a local graph, use the provided mapping to remap node identifiers.

    An invocation of this function results in the creation of a new local graph in which node identifiers have been
    remapped according to the contents in the supplied dictionary. The original graph is left untouched.

    The new mapping may be partial. In that case, only the nodes for which a corresponding key exists are remapped.

    :param cfg: the local graph to be remapped
    :param mapping: a dictionary containing the new mappings
    :return: a new local graph where the selected nodes have been remapped
    """

    new_entry = map(lambda ep: mapping.get(ep, ep), cfg.entry_point_ids)
    new_graph = relabel_nodes(cfg.graph, mapping)
    new_calls = map(lambda c:
                    ProcedureCall(mapping.get(c.caller, c.caller),
                                  c.callee,
                                  mapping.get(c.confluence_point, c.confluence_point)), cfg.external_calls)
    new_terminals = map(lambda term: mapping.get(term, term), cfg.terminal_nodes_ids)

    return LocalGraph(new_entry, new_graph, new_calls, new_terminals)


def execution_flow_at(inst: Instruction) -> Tuple[Transition, Optional[str]]:
    """
    Determine the state of the execution flow at the given instruction.

    This function returns a tuple containing a `Transition` type specifier and, in case of a jump, the symbol
    representing its destination. The transition type indicates in what manner the execution flow shall progress past
    the given instruction.

    :param inst: the instruction at which the control flow status must be checked
    :return: the tuple containing the parting transition
    """

    if inst.opcode in jump_ops:
        trans_type = jump_ops[inst.opcode]
        if trans_type.resolve_symbol:
            return trans_type, inst.immediate.symbol
        else:
            return trans_type, None
    else:
        # Any instruction that is not a jump instruction must maintain the sequential control flow
        return Transition.SEQ, None


def basic_blocks(code: CodeFragment) -> List[BasicBlock]:
    """
    Extract the basic blocks from a code fragment.

    The resulting basic blocks contain views on the source fragment, and come in the same order in which they appear in
    the original fragment. Non-code statements are discarded if they reside between BB boundaries and are not
    interleaved with code statements.

    For a correct behaviour, launch this function on a well-delimited code fragment (started by at least one label,
    terminated by a jump).

    Be aware that fancy ways of jumping around based on runtime-loaded addresses are not currently supported by this
    package.

    :param code: the code fragment whose basic blocks will be extracted
    :return: the list of basic blocks contained in the original fragment
    :raise InvalidCodeError: when the provided code fragment has no label or no outgoing jump
    """

    # Identify the block boundaries, that is: those lines marked by a label or containing a control transfer instruction
    block_boundaries = filter(lambda asl: isinstance(asl.statement, Instruction)
                                          and (asl.statement.opcode in jump_ops or len(asl.statement.labels) > 0),
                              # Use a line-oriented iterator, so that we can extract the line numbers
                              to_line_iterator(iter(code), code.begin))

    # Given the boundaries, calculate the appropriate cutoff points.
    # A dictionary is used as a way of implementing an "ordered set" for easy duplicate removal.
    # TODO find a more elegant way to remove duplicates online
    cutoff_points = dict()
    for boundary in block_boundaries:
        if len(boundary.statement.labels) > 0 and boundary.statement.opcode in jump_ops:
            # For a labeled line that also contains a jump, record two cut-points so that a single-line block can be
            # created.
            cutoff_points[boundary.number] = None
            cutoff_points[boundary.number + 1] = None
        elif len(boundary.statement.labels) > 0:
            # Labeled lines mark cut-points themselves
            cutoff_points[boundary.number] = None
        else:
            # A cut has to be made below any line containing a jump
            cutoff_points[boundary.number + 1] = None

    if len(cutoff_points) < 2:
        raise InvalidCodeError("Code fragment does not start with a label or end with a jump/return.")

    # Convert the "ordered set" back into a list
    cutoff_points = list(iter(cutoff_points))

    # Start slicing code into basic blocks
    bb = []
    head = cutoff_points[0]
    for tail in cutoff_points[1:]:
        if any(isinstance(line, Instruction) for line in code[head:tail]):
            # Since these blocks are probably gonna end up inside a graph, use the NetworkX's function for unique IDs
            bb.append(BasicBlock(FragmentView(code, head, tail, head), generate_unique_node()))
        head = tail

    return bb


# TODO patch this also in the derived package
def local_cfg(bbs: List[BasicBlock]) -> LocalGraph:
    """
    Construct a local graph from a list of basic blocks.

    Nodes and edges of the resulting graph will be decorated, respectively, with assembly labels and transition types,
    registered with the attribute names of `labels` and `kind`.

    This function works based on a few assumptions:

    - the basic blocks are provided in the same order they appear inside the original code fragment;
    - the first block is the entry-point;
    - all jumps are local;
    - all blocks with a final `RETURN` transition actually return control to whoever caused the PC to reach the EP.
    When these conditions are satisfied, a well-formed local graph is returned.

    :param bbs: the list of basic blocks of which the local graph is formed
    :return: a LocalGraph object representing the local graph
    """

    local_graph = DiGraph()

    local_symbol_table: MutableMapping[str, Hashable] = {}
    pending_jumps: List[Tuple[Hashable, str, Transition]] = []

    terminal_nodes = []
    calls = []

    parent_seq_block = None
    pending_call = None

    for bb in bbs:
        local_graph.add_node(bb.identifier, labels=list(bb.labels), block=bb.code)

        if parent_seq_block is not None:
            # Attach the current node to the sequence-wise previous one
            local_graph.add_edge(parent_seq_block, bb.identifier, kind=Transition.SEQ)
            parent_seq_block = None
        elif pending_call is not None:
            # Set the current node as the return point of an external procedure call
            calls.append(ProcedureCall(pending_call[0], pending_call[1], bb.identifier))
            pending_call = None

        # Embed the basic block's labels into the node
        local_symbol_table.update((lab, bb.identifier) for lab in bb.labels)

        outgoing_transition = bb.outgoing_flow[0]
        if outgoing_transition is Transition.RETURN:
            # The outgoing transition is a return-jump: add the node to the list of terminals.
            terminal_nodes.append(bb.identifier)
        elif outgoing_transition is Transition.CALL:
            # The outgoing transition is a procedure call: keep track of it so that the subsequent block will be set as
            # its confluence point.
            pending_call = bb.identifier, bb.outgoing_flow[1]
        else:
            if outgoing_transition is Transition.SEQ or outgoing_transition.branching:
                # In case of a sequential or branching transition, the subsequent basic block is to be attached to the
                # current one.
                parent_seq_block = bb.identifier

            if outgoing_transition.resolve_symbol:
                # In case of a jump, store its origin and symbolic destination for the coming one-pass resolution.
                pending_jumps.append((bb.identifier, bb.outgoing_flow[1], bb.outgoing_flow[0]))

    for jumper, dst, kind in pending_jumps:
        # Resolve the internal symbolic jumps and add the missing edges
        local_graph.add_edge(jumper, local_symbol_table[dst], kind=kind)

    # Transform recursive calls into internal call arcs
    # TODO re-implement with partitions or sets
    ci, ce = tee(calls)
    for cll in filter(lambda c: c.callee in local_symbol_table, ci):
        local_graph.add_edge(cll.caller, cll.confluence_point, kind=Transition.CALL, callee=cll.callee)

    return LocalGraph([bbs[0].identifier],
                      local_graph,
                      filter(lambda c: c.callee not in local_symbol_table, ce),
                      terminal_nodes)


def internalize_calls(cfg: LocalGraph) -> LocalGraph:
    """
    Transform external callees into symbolic internal nodes.

    A symbolic node will bear an identifier and a single label, both equal to the callee's symbolic name. Of course,
    these new nodes will be isolated from the rest of the graph. Therefore, this method is of practical use only when
    the user is planning an attempt at name resolution by modifying the internal graph.

    :param cfg: a local graph
    :return: a new local graph, with all external calls converted into symbolic nodes
    """

    # Gather all the callees' names
    external_nodes_ids = set(map(attrgetter('callee'), cfg.external_calls))

    # Create a new local graph containing only the symbolic nodes
    foreign_graph = DiGraph()
    foreign_graph.add_nodes_from((i, {'labels': [i], 'external': True}) for i in external_nodes_ids)
    external = LocalGraph(external_nodes_ids, foreign_graph, [], external_nodes_ids)

    # Merge the new graph with the original and return the result
    return cfg.merge(external)


def exec_graph(cfg: LocalGraph,
               entry_point: Union[str, Hashable],
               ignore_calls: FrozenSet[str] = frozenset()) -> DiGraph:
    """
    Given a local CFG and an entry-point, return the graph of the node visits performed by the execution flow.

    The procedure consists in a recursive, depth-first visit of sub-graphs, starting from the initial node and repeating
    itself for every `CALL` arc encountered. Given their nasty nature, recursive calls are not expanded; instead, they
    are represented by special nodes with IDs of the form `call{<call destination>, <unique ID>}`.

    The user can specify additional calls that mustn't be expanded.

    Different calls to the same procedure result in differently-labeled sub-graphs being attached, so the resulting
    graph is more a substantiation of the execution paths than a sub-graph of the original CFG. As a consequence, don't
    expect a one-to-one correspondence between the CFG's nodes and the one in the execution graph.

    Terminal nodes reachability is guaranteed only if the graph is well formed and any external call reached by the
    execution flow has been internalized, if not explicitly set as ignored.

    :param cfg: a CFG description of some code
    :param entry_point: an entry-point specification for the CFG, either as a node ID or as a symbolic label
    :param ignore_calls: a set of calls that won't be expanded into sub-graphs
    :return: a directed graph representing the execution starting from the specified entry-point
    """

    # Get the entry-point ID
    source = entry_point if entry_point in cfg.entry_point_ids else cfg.get_symbol_table()[entry_point]
    source_labels = cfg.graph.nodes[source]['labels']

    # If one of the entry-point's labels is in the ignore set, return a node summarizing the call
    if not ignore_calls.isdisjoint(source_labels):
        res = DiGraph()
        # The node will have a synthetic ID 'call{<call destination>, <unique ID>}', and will carry the original labels.
        res.add_node('call{' + str(source) + ', ' + generate_unique_node() + '}', labels=source_labels, external=True)
        return res

    # Traverse the subtree rooted at the entry-point and collect the visited nodes
    visited_nodes = frozenset(dfs_preorder_nodes(cfg.graph, source))
    # Produce a view of the visited component
    visited_component: Graph = subgraph_view(cfg.graph, lambda n: n in visited_nodes)

    # Initialize the returned graph with the contents of the visited component
    res = DiGraph()
    res.update(visited_component)

    # Iterate over the CALL edges inside the visited component
    for edge in filter(lambda e: visited_component.edges[e]['kind'] == Transition.CALL, visited_component.edges):
        # Recursively compute the component of the called procedures
        nested_component = exec_graph(cfg,
                                      visited_component.edges[edge]['callee'],
                                      ignore_calls.union(source_labels))
        # Add the nested component to the result, avoiding ID clashes
        relabel_nodes(nested_component, solve_graph_collision(res, nested_component), False)
        res.update(nested_component)

        # Take the root of the sub-component and its terminal nodes
        head = next(filter(lambda n: nested_component.in_degree(n) == 0, nested_component.nodes))
        tail = filter(lambda n: nested_component.out_degree(n) == 0, nested_component.nodes)

        # Substitute the original edge with call and return edges toward/from the sub-component
        res.remove_edge(*edge)
        res.add_edge(edge[0], head, kind=Transition.CALL)
        res.add_edges_from(zip(tail, repeat(edge[1])), kind=Transition.RETURN)

    return res


def build_cfg(src: Source, entry_point: str = "main") -> DiGraph:
    """Build CFG of the supplied assembly code, starting from the entry point.

    The entry point consists of a valid label pointing to what will be
    considered by the algorithm as the first instruction executed by a caller.

    The resulting graph's nodes either contain a reference to a view, through
    the node attribute `block`, which represents the block of serial
    instructions associated with the node, or an `external` flag, signifying
    that the referenced code is external to the analyzed code.

    Nodes are connected through unweighted edges bearing a `kind` attribute,
    which describes the type of transition that that edge represents.

    :param src: the assembler source to be analyzed
    :param entry_point: the entry point from which the execution flow will be
                        followed
    :return: a directed graph representing the CFG of the analyzed code

    """
    symbol_table = dict()
    # Get labels from text sections only
    for lbs in (s.scope.get_labels() for s in src.get_sections()
                if s.identifier == '.text'):
        symbol_table.update(lbs)

    # We assume that any label that doesn't start with a dot is a function
    function_labels = [fl[1] for fl in symbol_table.items() if not
                       fl[0].startswith('.')]
    # Extract the basic blocks of each function, storing them in different
    # collections
    functions_bbs = [basic_blocks(FragmentView(src, sl[0], sl[1], sl[0])) for
                     sl in zip_longest(function_labels, function_labels[1:],
                                       fillvalue=src.end)]
    # Build one big shared graph among all functions
    common_graph = reduce(lambda g1, g2: g1.merge(g2), (local_cfg(bbs) for bbs
                                                        in functions_bbs))

    # Extract the execution graph, relabeling nodes with progressive integer IDs
    execution_graph = exec_graph(internalize_calls(common_graph), entry_point)
    execution_graph = convert_node_labels_to_integers(execution_graph, 1)

    # Attach the special 0-node to the entry point, and redirect all terminal
    # nodes to it via a RETURN transition
    execution_graph.add_node(0, external=True)
    execution_graph.add_edge(0, 1, kind=Transition.U_JUMP)
    execution_graph.add_edges_from([(term, 0) for term in execution_graph.nodes
                                    if execution_graph.out_degree(term) == 0],
                                   kind=Transition.RETURN)

    return execution_graph


def get_stepper(cfg: DiGraph, entry_pnt: int) -> Iterator[ASMLine]:
    """
    Step execution through the CFG.

    Given a CFG and an optional starting point (entry-point), generates an iterator that follows the program's execution
    flow.

    When confronted by the bifurcating edges of a conditional branch situation, callers can `.send()` the condition's
    truth value in order to select the branch to follow.

    If a node representing code not included in the represented source is encountered, the iterator emits the artificial
    directive:
        <non-local call $node_id>
    to signal the fact, then regularly proceeds by following the return arc.

    :param cfg: a control-flow graph representing the program
    :param entry_pnt: the entry point from which iteration should start, either in label form or as a line number
    :return: an iterator that produces ASMLine objects
    :raise ValueError: when the specified entry point does not belong to any node of the CFG
    """

    # Find the node containing the entry point
    # Be aware that the entry point *MUST* refer to an instruction; nodes only contain those.
    for nid in [n for n in cfg.nodes.keys() if "external" not in cfg.nodes[n]]:
        view: FragmentView = cfg.nodes[nid]["block"]
        if view.begin <= entry_pnt < view.end:
            current_node = nid
            break
    else:
        raise ValueError("Invalid entry-point: no statement at line " + str(entry_pnt) + "is contained in this graph")

    # Prepare objects for iteration
    block: FragmentView = cfg.nodes[current_node]["block"]
    line_iterator: Iterator[ASMLine] = to_line_iterator(block.iter(entry_pnt), entry_pnt)
    line: ASMLine = next(line_iterator)

    execute_jump = yield line
    while True:
        # Advance 'till the end of the current block
        for line in line_iterator:
            execute_jump = yield line

        # Identify any conditional branch
        conditional = None
        for t, s in [(cfg.edges[current_node, s]["kind"], s) for s in cfg.successors(current_node)]:
            if t.value == Transition.C_JUMP.value:
                conditional = s
            else:
                # We don't expect more than one other "default" path to follow
                current_node = s

        # Set the conditional branch's destination as the current node, if the caller told us so
        if conditional is not None and execute_jump:
            current_node = conditional

        # If we're back at node 0, then execution has finished
        if current_node == 0:
            return

        # If the node we reached is external, just yield a special value and advance to the node that follows it
        if "external" in cfg.nodes[current_node]:
            yield ASMLine(-1, Directive("<non-local call " + str(current_node) + ">"))
            current_node = next(cfg.successors(current_node))

        # Load the next block and continue iteration
        block = cfg.nodes[current_node]["block"]
        line_iterator = to_line_iterator(iter(block), block.begin)


def merge_points(cfg: DiGraph) -> FrozenSet[int]:
    """
    Find all the merge point in the CFG.

    A merge point is a node on which multiple directed edges converge.

    :arg cfg: the CFG representing a program
    :return: a frozen set containing all the merge points
    """

    # Node 0 represents the calling environment, so it must be excluded from the analysis
    return frozenset((n for n in cfg.nodes.keys() if n != 0 and cfg.in_degree(n) > 1))


def loop_back_nodes(cfg: DiGraph) -> FrozenSet[int]:
    """
    Find all the nodes of a CFG that are exclusively part of a loop.

    A node is exclusively part of a loop if it belongs only to those paths that traverse the back-loop of a cycle.

    :arg cfg: the CFG representation of a program
    :return: a frozen set of all the loop-exclusive nodes
    """

    # Node 0 closes an improper loop over the CFG, so it must be ignored
    cycle_nodes = frozenset(chain.from_iterable(simple_cycles(restricted_view(cfg, [0], []))))
    return frozenset(cycle_nodes.difference(chain.from_iterable(
        # For every path, its last component is node 0; therefore, we have to cut it.
        map(lambda l: l[:-1], all_simple_paths(cfg, 1, 0)))))
