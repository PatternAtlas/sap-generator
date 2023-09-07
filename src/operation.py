from typing import Callable, Mapping
from solution import Solution
from graph import Graph

class Operation:
    def __init__(self, graph: Graph, operation: Callable[[Mapping], Solution]):
        self.graph = graph
        self.aggregate = operation