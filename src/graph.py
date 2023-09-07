from solution import Solution
from typing import List, Set

class Graph:
    def __init__(self, solutions: List[Solution], edges: List[Set[Solution]]):
        self.nodes = solutions
        self.edges = edges
    
    def has_edge(self, edge: Set[Solution]):
        return True if edge in self.edges else False
    
    def get_edges_of_node(self, node: Solution) -> List[Set[Solution]]:
        edges = []
        for edge in self.edges:
            if node in edge:
                edges.append(edge)
        return edges
    
    def to_nx_graph(self):
        import networkx as nx
        nx_graph = nx.Graph()
        for node in self.nodes:
            nx_graph.add_node(node,id=node.id, capabilities=node.capabilities,
            requirements=node.requirements, cs_type=node.cs_type)
        for edge in self.edges:
            nx_graph.add_edge(*edge)
        return nx_graph
    
    def __str__(self):
        node_ids = list(map(lambda node: node.id, self.nodes))
        edge_node_ids = list(map(lambda edge: list(map(lambda node: node.id, edge)), self.edges))
        return f"Graph(nodes={node_ids}, edges={edge_node_ids})"