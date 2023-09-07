from solution import Solution
from operation import Operation

class Mapping:
    def __init__(self, mapping: dict[Solution, Solution], operation: Operation):
        self.mapping = mapping
        self.operation = operation
    
    def get_detected_solutions(self) -> list[Solution]:
        # The keys in the mapping are the solutions of the detected subgraph of the solution graph.
        return self.mapping.keys()
    
    def execute_aggregation(self) -> Solution:
        return self.operation.aggregate(self)
    
    def __str__(self):
        result = ""
        for key in self.mapping.keys():
            result += str(key) + " -> " + str(self.mapping[key]) + "\n"
            
        return result