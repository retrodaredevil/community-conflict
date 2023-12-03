from pathlib import Path
from typing import Callable, Any

import networkx as nx

from community_conflict.cache import read_or_parse_file
from community_conflict.subgraphs import sample_edges
from community_conflict.subgraphs import sample_nodes
import matplotlib
import matplotlib.pyplot as plt

def print_graph(graph: nx.digraph):
    pos = nx.spring_layout(graph)  # positions for all nodes

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=100)

    # Draw directed edges
    nx.draw_networkx_edges(graph, pos, width=1, edge_color='gray', arrows=True, connectionstyle='arc3, rad = 0.1')

    # Draw labels
    #nx.draw_networkx_labels(graph, pos, font_size=3, font_color='black')

    # Display the graph
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()

def main():
    graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    #edgeSub = sample_edges(graph, 1500)
    #print(edgeSub)
    nodeSub = sample_nodes(graph, 2000)
    print(nodeSub)
    #print_graph(edgeSub)
    print_graph(nodeSub)

if __name__ == '__main__':
    main()