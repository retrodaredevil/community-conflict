import networkx as nx


def subgraph_with_negative_posts(graph: nx.MultiDiGraph) -> nx.MultiDiGraph:
    edges = graph.edges(keys=True, data=True)
    return graph.edge_subgraph(
        (u, v, key) for u, v, key, data in edges if data["link_sentiment"] == -1
    )
