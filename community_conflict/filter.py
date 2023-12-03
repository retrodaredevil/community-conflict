import networkx as nx


def subgraph_with_negative_posts(graph: nx.DiGraph) -> nx.DiGraph:
    edges = graph.edges(data=True)
    return graph.edge_subgraph(
        (edge[0], edge[1]) for edge in edges if edge[2]["link_sentiment"] == -1
    )
