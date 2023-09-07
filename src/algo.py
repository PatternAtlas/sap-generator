import itertools
import copy
import logging

from graph import Graph
from aggregation_step import AggregationStep
from subgraph_operator import Operator
from solution import Solution
from mapping import Mapping

import networkx as nx

from typing import List, Tuple

# create a logger
logger = logging.getLogger(__name__)

# set the logging level
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('algo.log')

# set the logging level for the handler
handler.setLevel(logging.DEBUG)

# create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add the formatter to the handler
handler.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(handler)


def apply_aggregation_on_graph(graph: Graph, mapping: Mapping) -> Tuple[Graph, Solution]:
    aggregate = mapping.execute_aggregation()
    # remove nodes of mapping from graph
    nodes_to_remove = mapping.get_detected_solutions()
    for solution in nodes_to_remove:
        graph.nodes.remove(solution)
    removed_nodes = nodes_to_remove
    graph.nodes.append(aggregate)
    for node in removed_nodes:
        # remove edges between nodes of found mapping from graph
        # change old nodes to aggregate in remaining edges
        for edge in graph.get_edges_of_node(node):
            edge.remove(node)
            edge.add(aggregate)
            if len(edge) == 1:
                graph.edges.remove(edge)
    return graph, aggregate

def reached_finish_criteria(completed_aggregation_steps: List[List[AggregationStep]],
                            find_all_solutions):
    if len(completed_aggregation_steps) > 0 and not find_all_solutions:
        return True
    else:
        return False

counter = 0
mappings_sum = 0

def calc_aggregation_based_on_subgraphs(graph: Graph,
                                        aggregation_steps: List[AggregationStep],
                                        operators: List[Operator],
                                        complete_aggregation_steps: List[List[AggregationStep]],
                                        incompleted_aggregations: List[AggregationStep],
                                        find_all_solutions: bool = False):
    global counter
    global mappings_sum
    counter = counter + 1
    logger.debug(f"Counter: {counter} Length of Graph: {len(graph.nodes)}")
    
    # solution found
    if len(graph.nodes) == 1:
        complete_aggregation_steps.append(aggregation_steps)
        logger.debug(f"FINISH: processed ~ {mappings_sum} mappings in {counter} steps and reduces graph to 1 node")
        return

    if reached_finish_criteria(complete_aggregation_steps, find_all_solutions):
        return
    
    mapping_found = False
    for operator in operators:
        logger.debug(f"processed {mappings_sum} mappings so far")
        mappings = get_mappings(graph, operator)
        mappings_sum = mappings_sum + len(mappings)
        logger.debug(f"found {len(mappings)} new mappings")
        for mapping in mappings:
            mapping_found = True
            aggregation_steps_fork = copy.deepcopy(aggregation_steps)
            graph_fork = copy.deepcopy(graph)
            new_graph, aggregate = apply_aggregation_on_graph(graph_fork, mapping)
            aggregation_steps_fork.append(AggregationStep(graph, operator, mapping, aggregate, new_graph))
            calc_aggregation_based_on_subgraphs(new_graph,
                                                aggregation_steps_fork,
                                                operators,
                                                complete_aggregation_steps,
                                                incompleted_aggregations,
                                                find_all_solutions)
            if reached_finish_criteria(complete_aggregation_steps, find_all_solutions):
                return
        if reached_finish_criteria(complete_aggregation_steps, find_all_solutions):
            return
    
    if len(graph.nodes) > 1 and not mapping_found:
        # get longest incompleted aggregation and if this is smaller than current one, remove it and add current one
        if len(incompleted_aggregations) < len(aggregation_steps):
            incompleted_aggregations.clear()
            incompleted_aggregations.append(aggregation_steps)
            logger.debug(f"found incomplete aggregations, processed ~ {mappings_sum} mappings in {counter} steps and reduces graph to {len(graph.nodes)} nodes")

def get_mappings(graph: Graph, operator: Operator) -> List[Mapping]:
    
    mappings = []

    def node_match(n1, n2):
        match = n1['cs_type'] == n2['cs_type'] and \
        n1['requirements'] == n2['requirements'] and \
        n1['capabilities'] == n2['capabilities']
        return match

    nx_solution_graph = graph.to_nx_graph()
    supported_operations = operator.supported_operations
    for supported_operation in supported_operations:
        nx_operator_graph = supported_operation.graph.to_nx_graph()
        isomorphisms = nx.algorithms.isomorphism.GraphMatcher(
            nx_solution_graph,
            nx_operator_graph,
            node_match=node_match).subgraph_isomorphisms_iter()
        for isomorphism in isomorphisms:
            mapping = Mapping(isomorphism, supported_operation)
            mappings.append(mapping)
    return mappings

def create_joined_permuation(list_of_lists):
    if len(list_of_lists) == 1:
        return list_of_lists

    joined_permutations = []
    for i in list_of_lists[0]:
        for j in list_of_lists[1]:
            joined_permutations.append(i + j)

    list_of_lists = list_of_lists[2:]
    list_of_lists.insert(0, joined_permutations)
    return create_joined_permuation(list_of_lists)

def get_aggregator_permutations(operators: set[Operator]):
    aggregators = sorted(
        operators, key=lambda operator: operator.rank, reverse=True)
    aggregator_groups = []
    current_rank = -1
    for aggregator in aggregators:
        if aggregator.rank != current_rank:
            current_rank = aggregator.rank
            aggregator_groups.append([])
        aggregator_groups[-1].append(aggregator)

    aggregator_permutations = []
    for aggregator_group in aggregator_groups:
        aggregator_permutations.append(
            list(itertools.permutations(aggregator_group)))

    joined_permutations = create_joined_permuation(aggregator_permutations)
    return joined_permutations[0]
