from pathlib import Path

import networkx as nx
import sys
import numpy as np
import matplotlib.pyplot as plt
import powerlaw

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

def graph_density(graph: nx.DiGraph) -> float:
    return nx.density(graph)
def plot_dist(graph):
    hist = nx.degree_histogram(graph)   
    plt.plot(range(0, len(hist)), hist, ".")
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("# of Nodes")
    plt.loglog()
    plt.show()


def basic_info(graph: nx.DiGraph):
    print("Global Clustering Coefficient:", nx.average_clustering(graph)) # large for real world networks
    #print("Path length:", nx.average_shortest_path_length(graph)) # small for real world networks
    print("Density:", nx.density(graph)) # sparse for real world network
    hist = nx.degree_histogram(graph)
    plot_dist(graph)



def main():
    graph = parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"))
    print(graph) # prints number of edges and nodes
    basic_info(graph)

    print(graph_density(graph))

