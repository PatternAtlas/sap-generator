from operation import Operation

class Operator:
    def __init__(self, supported_operations: list[Operation],
                 aggregate_type: str,
                 rank: int = 0,):
        self.supported_operations = supported_operations
        self.rank = rank
        self.aggregate_type = aggregate_type
    
    def __str__(self):
        return f"Operator(supported_subgraph={self.supported_operations}, rank={self.rank}, aggregate_type={self.aggregate_type})"
        