import networkx as nx
from solution import Solution

cs1 = Solution(id="cs1",
               requirements=set(),
               capabilities=set(),
               cs_type="type1")

cs2 = Solution(id="cs2",
               requirements=set(),
               capabilities=set(),
               cs_type="type1")

cs3 = Solution(id="cs3",
               requirements=set(),
               capabilities=set(),
               cs_type="type1")

cs4 = Solution(id="cs4",
               requirements=set(),
               capabilities=set(),
               cs_type="type1")

cs5 = Solution(id="cs5",
               requirements=set(),
               capabilities=set(),
               cs_type="type1")

cs6 = Solution(id="cs6",
               requirements=set(),
               capabilities=set(),
               cs_type="type1")

G1 = nx.Graph()
G1.add_node(cs1, id=cs1.id, capabilities=cs1.capabilities,
            requirements=cs1.requirements, cs_type=cs1.cs_type)
G1.add_node(cs2, id=cs2.id, capabilities=cs2.capabilities,
            requirements=cs2.requirements, cs_type=cs2.cs_type)
G1.add_node(cs3, id=cs3.id, capabilities=cs3.capabilities,
            requirements=cs3.requirements, cs_type=cs3.cs_type)
G1.add_node(cs4, id=cs4.id, capabilities=cs4.capabilities,
            requirements=cs4.requirements, cs_type=cs4.cs_type)
edges_g1 = [(cs1, cs2), (cs1, cs3), (cs1, cs4)]
G1.add_edges_from(edges_g1)

operator_graph = nx.Graph()
operator_graph.add_node(cs5, id=cs5.id, capabilities=cs5.capabilities, requirements=cs5.requirements, cs_type=cs5.cs_type)
operator_graph.add_node(cs6, id=cs6.id, capabilities=cs6.capabilities, requirements=cs6.requirements, cs_type=cs6.cs_type)
edges_operator_graph = [(cs5, cs6)]
operator_graph.add_edges_from(edges_operator_graph)

def node_match(n1, n2):
    match = n1['cs_type'] == n2['cs_type'] and \
        n1['requirements'] == n2['requirements'] and \
        n1['capabilities'] == n2['capabilities']
    return match


if nx.algorithms.isomorphism.GraphMatcher(G1, operator_graph, node_match=node_match).subgraph_is_isomorphic():
    print("is isomorphic")
    isomorphisms = nx.algorithms.isomorphism.GraphMatcher(
        G1, operator_graph, node_match=node_match).subgraph_isomorphisms_iter()
    for idx, isomorphism in enumerate(isomorphisms):
        print(idx)
        for i in isomorphism:
            print(i, isomorphism[i])
else:
    print("not isomorphic")


def test():
    G1 = nx.Graph()
    G1.add_node(1)
    G1.add_node(2)
    G1.add_node(3)
    G1.add_node(4)
    edges_g1 = [(1, 2), (1, 3), (1, 4)]
    G1.add_edges_from(edges_g1)

    operator_graph = nx.Graph()
    operator_graph.add_node(5)
    operator_graph.add_node(6)
    edges_operator_graph = [(5, 6)]
    operator_graph.add_edges_from(edges_operator_graph)

    if nx.algorithms.isomorphism.GraphMatcher(G1, operator_graph).subgraph_is_isomorphic():
        print("is isomorphic")
        isomorphisms = nx.algorithms.isomorphism.GraphMatcher(
            G1, operator_graph).subgraph_isomorphisms_iter()
        for idx, isomorphism in enumerate(isomorphisms):
            print(idx)
            for i in isomorphism:
                print(i, isomorphism[i])
    else:
        print("not isomorphic")
