from subgraph_operator import Operator
from solution import Solution

class SolutionAlgebra:
    def __init__(self, solutions: set[Solution], operators: set[Operator]):
        self.carrier_set = solutions
        self.operators = operators