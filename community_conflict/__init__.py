from pathlib import Path

import random as ran
import networkx as nx
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout
import sys

assert sys.version_info >= (3, 8), "This script requires Python 3.8 or higher"


def parse_file(file: Path) -> nx.DiGraph:
    graph = nx.DiGraph()
    with file.open("r") as f:
        f.readline()  # ignore the first line
        while line := f.readline():
            line = line.strip()
            parts = line.split("\t")
            source_subreddit = parts[0]
            target_subreddit = parts[1]
            # print(f"{source_subreddit:>25}  -->  {target_subreddit}")
            graph.add_edge(source_subreddit, target_subreddit)

    return graph

"""
Calculates Density
returns a float
"""
def graph_density(graph: nx.DiGraph) -> float:
    return nx.density(graph)

"""
Samples edges and ceates a subgraph
returns a graph
"""
def sample_edges(graph: nx.DiGraph, sample_count: int) -> nx.DiGraph:
    random_nodes = ran.sample(list(graph.edges), 1000)
    return graph.edge_subgraph(random_nodes)

def main():
    graph = parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"))
    print(graph)
