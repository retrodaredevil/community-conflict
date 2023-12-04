from pathlib import Path

import pickle
from typing import List

import networkx as nx

from community_conflict import Node, NodeAttributes
from community_conflict.cache import read_or_parse_file
from community_conflict.collapse import collapse, CollapsedNodeAttributes


def compute_katz_centralities(graph: nx.Graph):
    """Compute various centrality measures relevant to our data and
       saves them to the computed_values folder"""
    # Katz centralities don't seem to converge with the default iterations of 1000. Possibly try larger
    with open("computed_values/katz_cent.pickle", "wb") as f:
        print("Computing Katz Centralities")
        katz_cent = nx.katz_centrality(graph)
        pickle.dump(katz_cent, f)

def compute_node_betweenness_centralities(graph: nx.Graph):
    with open("computed_values/node_betweenness_cent.pickle", "wb") as f:
        print("Computing Node Betweenness Centralities")
        node_betweenness_cent = nx.betweenness_centrality(graph)
        pickle.dump(node_betweenness_cent, f)


def compute_edge_betweenness_centralities(graph: nx.Graph):
    with open("computed_values/edge_betweenness_cent.pickle", "wb") as f:
        print("Computing Edge Betweenness Centralities")
        edge_betweenness_cent = nx.edge_betweenness_centrality(graph)
        pickle.dump(edge_betweenness_cent, f)

def compute_harmonic_centralities(graph: nx.Graph):
    with open("computed_values/harmonic_cent.pickle", "wb") as f:
        print("Computing Harmonic Centralities")
        harmonic_cent = nx.harmonic_centrality(graph)
        pickle.dump(harmonic_cent, f)

def compute_closeness_centralities(graph: nx.Graph):
    with open("computed_values/closeness_cent.pickle", "wb") as f:
        print("Computing Closeness Centralities")
        closeness_cent = nx.closeness_centrality(graph)
        pickle.dump(closeness_cent, f)

def compute_pagerank(graph: nx.Graph):
    with open("computed_values/pagerank.pickle", "wb") as f:
        print("Computing Page Rank")
        page_rank = nx.pagerank(graph)
        pickle.dump(page_rank, f)

def compute_degree_centralities(graph: nx.Graph):
    with open("computed_values/degree_cent.pickle", "wb") as f:
        print("Computing Degree Centralities")
        degree_cent = nx.degree_centrality(graph)
        pickle.dump(degree_cent, f)


def show_centralities():
    # Node Betweenness Centrality
    with open("computed_values/node_betweenness_cent.pickle", "rb") as f:
        node_betweenness_cent = pickle.load(f)
    sorted_node_betweenness_cent = sorted(node_betweenness_cent.items(), key=lambda x: x[1], reverse=True)
    print("|{:<25}|{:>25}|".format("Subreddit Name", "Betweenness Centrality"))
    print("_"*53)
    for node in sorted_node_betweenness_cent[:15]:
        print("|{:<25}|{:>25.10f}|".format(node[0], node[1]))

    print("\n")

    # Degree Centrality
    with open("computed_values/degree_cent.pickle", "rb") as f:
        degree_cent = pickle.load(f)
    degree_cent = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)
    print("|{:<25}|{:>25}|".format("Subreddit Name", "Degree Centrality"))
    print("_"*53)
    for node in degree_cent[:15]:
        print("|{:<25}|{:>25.10f}|".format(node[0], node[1]))

    print("\n")

    # Page Rank
    with open("computed_values/pagerank.pickle", "rb") as f:
        page_rank = pickle.load(f)
    page_rank = sorted(page_rank.items(), key=lambda x: x[1], reverse=True)
    print("|{:<25}|{:>25}|".format("Subreddit Name", "Page Rank Score"))
    print("_" * 53)
    for node in page_rank[:15]:
        print("|{:<25}|{:>25.10f}|".format(node[0], node[1]))

def contraction(graph: nx.MultiDiGraph, u: Node, v: Node, edge_data_list: List[NodeAttributes]) -> CollapsedNodeAttributes:
    return {"weight": len(edge_data_list)}

def main():
    graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    graph = collapse(graph)
    compute_degree_centralities(graph)
    compute_closeness_centralities(graph)
    compute_harmonic_centralities(graph)
    #compute_node_betweenness_centralities(graph)
    compute_pagerank(graph)
    show_centralities()


if __name__ == "__main__":
    main()