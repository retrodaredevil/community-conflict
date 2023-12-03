

"""
This file has logic for collapsing a multi-graph into a simple graph
"""
from typing import List, TypedDict, Dict

import networkx as nx

from community_conflict import NodeAttributes, Node
from community_conflict.visualize_graph import print_graph


class CollapsedNodeAttributes(TypedDict):
    weight: float


def contraction(
    graph: nx.MultiDiGraph, u: Node, v: Node, edge_data_list: List[NodeAttributes]
) -> CollapsedNodeAttributes:
    weight = 0.0
    for edge_data in edge_data_list:
        if edge_data["link_sentiment"] == 1:
            weight += 1
        elif edge_data["link_sentiment"] == -1:
            weight -= 2

    return {
        "weight": max(weight, 0.0)
    }


def collapse(graph: nx.MultiDiGraph) -> nx.Graph:
    collapsed_graph = nx.Graph(graph)

    for u, v in collapsed_graph.edges():
        data_dictionary_or_edge_data = graph.get_edge_data(u, v) or graph.get_edge_data(v, u)  # you have to try both, because collapsed graph is no longer directed
        edge_data_list: List[NodeAttributes] = list(data_dictionary_or_edge_data.values())
        attributes = contraction(graph, u, v, edge_data_list)
        collapsed_graph.add_edge(u, v, **attributes)

    return collapsed_graph


def __test_main():
    multi = nx.MultiDiGraph()
    multi.add_edge(1, 2, asdf=1)
    multi.add_edge(1, 2)
    multi.add_edge(1, 2)
    multi.add_edge(3, 1)
    print(multi.get_edge_data(1, 2))
    print(nx.Graph(multi).get_edge_data(1, 2))
    print(multi.get_edge_data(3, 1))
    print_graph(multi)


if __name__ == '__main__':
    __test_main()
