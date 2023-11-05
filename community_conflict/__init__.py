from pathlib import Path

import networkx as nx
import sys
import random

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

def get_random_edge_subgraph(num_edges: int, graph: nx.Graph) -> nx.Graph:
    edges = random.sample(list(graph.edges), num_edges)
    return graph.edge_subgraph(edges)

def get_random_node_subgraph(num_nodes: int, graph: nx.Graph) -> nx.Graph:
    nodes = random.sample(list(graph.nodes), num_nodes)
    return graph.subgraph(nodes)

def main():
    graph = parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"))

    print(graph)

