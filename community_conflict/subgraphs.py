import networkx as nx
import random

def sample_edges(graph: nx.DiGraph, sample_count: int) -> nx.DiGraph:
    random_edges = random.sample(list(graph.edges), sample_count)
    return graph.edge_subgraph(random_edges)

def sample_nodes(graph: nx.DiGraph, sample_count: int) -> nx.DiGraph:
    random_nodes = random.sample(list(graph.nodes), sample_count)
    return graph.subgraph(random_nodes)
