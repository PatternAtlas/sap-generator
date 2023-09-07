from subgraph_operator import Operator
from solution import Solution
from mapping import Mapping
from graph import Graph


class AggregationStep:
    def __init__(self,
                 source_graph: Graph,
                 operator: Operator,
                 mapping: Mapping,
                 aggregate: Solution,
                 resulting_graph: Graph):
        self.source_graph = source_graph
        self.operator = operator
        self.mapping = mapping
        self.aggregate = aggregate
        self.resulting_graph = resulting_graph
