from pathlib import Path
from typing import Callable, Any

import networkx as nx

from community_conflict import Node
from community_conflict.cache import read_or_parse_file
import matplotlib.pyplot as plt


def visualize_top_statistic(graph: nx.DiGraph, title_prefix: str, statistic_name: str, statistic: Callable[[nx.DiGraph, Node], float], num_items=10):
    # Calculate the out-degrees of all nodes
    statistic_map = {node: statistic(graph, node) for node in graph.nodes()}

    # Sort nodes by out-degree in descending order
    sorted_nodes = sorted(statistic_map.items(), key=lambda x: x[1], reverse=True)

    # Select the top 10 nodes
    top_nodes = sorted_nodes[:num_items]

    # Extract the node names and out-degrees for visualization
    node_names, statistic_values = zip(*top_nodes)

    # Bar plot
    plt.bar(range(len(node_names)), statistic_values, tick_label=node_names)
    plt.xlabel('Nodes')
    plt.ylabel(statistic_name)
    plt.title(f'{title_prefix} - Top {num_items} Nodes by {statistic_name}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()


def main():
    title_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    body_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-body.tsv"), Path(".cache/soc-redditHyperlinks-body.pickle"))
    for name, graph in [("title", title_graph), ("body", body_graph)]:
        print()
        print(name)
        print(graph)
        prefix = f"{name} dataset"
        visualize_top_statistic(graph, prefix, "Out-degree", lambda _, node: graph.out_degree(node), 15)
        visualize_top_statistic(graph, prefix, "In-degree", lambda _, node: graph.in_degree(node), 15)


if __name__ == '__main__':
    main()
