import networkx as nx
"""
Calculates Density
returns a float
"""
def graph_density(graph: nx.MultiDiGraph) -> float:
    return nx.density(graph)
