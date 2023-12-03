import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from community_conflict.density import graph_density
import networkx as nx
import pylab as plt

assert sys.version_info >= (3, 8), "This script requires Python 3.8 or higher"


# POST_PROPERTIES: a vector representing the text properties of the source post, listed as a list of comma separated numbers. The vector elements are the following:
PROPERTY_KEYS = [
    "Number of characters",
    "Number of characters without counting white space",
    "Fraction of alphabetical characters",
    "Fraction of digits",
    "Fraction of uppercase characters",
    "Fraction of white spaces",
    "Fraction of special characters, such as comma, exclamation mark, etc.",
    "Number of words",
    "Number of unique works",
    "Number of long words (at least 6 characters)",
    "Average word length",
    "Number of unique stopwords",
    "Fraction of stopwords",
    "Number of sentences",
    "Number of long sentences (at least 10 words)",
    "Average number of characters per sentence",
    "Average number of words per sentence",
    "Automated readability index",
    "Positive sentiment calculated by VADER",
    "Negative sentiment calculated by VADER",
    "Compound sentiment calculated by VADER",
    "LIWC_Funct",
    "LIWC_Pronoun",
    "LIWC_Ppron",
    "LIWC_I",
    "LIWC_We",
    "LIWC_You",
    "LIWC_SheHe",
    "LIWC_They",
    "LIWC_Ipron",
    "LIWC_Article",
    "LIWC_Verbs",
    "LIWC_AuxVb",
    "LIWC_Past",
    "LIWC_Present",
    "LIWC_Future",
    "LIWC_Adverbs",
    "LIWC_Prep",
    "LIWC_Conj",
    "LIWC_Negate",
    "LIWC_Quant",
    "LIWC_Numbers",
    "LIWC_Swear",
    "LIWC_Social",
    "LIWC_Family",
    "LIWC_Friends",
    "LIWC_Humans",
    "LIWC_Affect",
    "LIWC_Posemo",
    "LIWC_Negemo",
    "LIWC_Anx",
    "LIWC_Anger",
    "LIWC_Sad",
    "LIWC_CogMech",
    "LIWC_Insight",
    "LIWC_Cause",
    "LIWC_Discrep",
    "LIWC_Tentat",
    "LIWC_Certain",
    "LIWC_Inhib",
    "LIWC_Incl",
    "LIWC_Excl",
    "LIWC_Percept",
    "LIWC_See",
    "LIWC_Hear",
    "LIWC_Feel",
    "LIWC_Bio",
    "LIWC_Body",
    "LIWC_Health",
    "LIWC_Sexual",
    "LIWC_Ingest",
    "LIWC_Relativ",
    "LIWC_Motion",
    "LIWC_Space",
    "LIWC_Time",
    "LIWC_Work",
    "LIWC_Achiev",
    "LIWC_Leisure",
    "LIWC_Home",
    "LIWC_Money",
    "LIWC_Relig",
    "LIWC_Death",
    "LIWC_Assent",
    "LIWC_Dissent",
    "LIWC_Nonflu",
    "LIWC_Filler",
]

# If you need to typehint a node, then you can use this type even though its not that useful as a type itself
Node = Any

def parse_file(file: Path) -> nx.DiGraph:
    graph = nx.DiGraph()
    with file.open("r") as f:
        f.readline()  # ignore the first line
        while line := f.readline():
            line = line.strip()
            parts = line.split("\t")
            source_subreddit = parts[0]
            target_subreddit = parts[1]
            post_id = parts[2]
            timestamp_string = parts[3]
            link_sentiment = int(parts[4])
            properties = [float(a) for a in parts[5].split(",")]
            # print(f"{source_subreddit:>25}  -->  {target_subreddit}")
            attributes = {
                "post_id": post_id,
                "timestamp": datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M:%S"),
                "link_sentiment": link_sentiment,
                "properties": properties,
            }
            graph.add_edge(source_subreddit, target_subreddit, **attributes)

    return graph




def filter_by_date_example(graph: nx.DiGraph):
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2015, 1, 15)
    edges = graph.edges(data=True)
    new_graph = graph.edge_subgraph((edge[0], edge[1]) for edge in edges if start_date <= edge[2]["timestamp"] <= end_date)
    print(new_graph)


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
    #print("Density:", nx.density(graph)) # sparse for real world network
    print(nx.number_strongly_connected_components(graph))
    print(nx.number_weakly_connected_components(graph))
    #hist = nx.degree_histogram(graph)
    #plot_dist(graph)
    print(sum(dict(graph.degree()).values())/float(len(graph)))

def greedy_modularity(graph: nx.DiGraph):
    gn_comm = list(nx.community.greedy_modularity_communities(graph))
    output_file_path = 'greedy_modularity.txt'
    with open(output_file_path, 'w') as file:
        for step, community in enumerate(gn_comm):
            file.write(f"Step {step + 1}: {community}\n")

def louvain(graph: nx.DiGraph):
    #output_file_path = 'louvain.txt'
    louvain_coms = list(nx.algorithms.community.asyn_lpa_communities(graph))

    superG = nx.DiGraph()

    for i, community in enumerate(louvain_coms):
        superG.add_node(f"SuperNode_{i + 1}", members=list(community))

    for edge in graph.edges():
        for i, community in enumerate(louvain_coms):
            if edge[0] in community:
                for j, other_community in enumerate(louvain_coms):
                    if edge[1] in other_community and i != j:
                        superG.add_edge(f"SuperNode_{i + 1}", f"SuperNode_{j + 1}")

    # Plot the supernode graph
    pos = nx.spring_layout(superG)
    nx.draw(superG, pos, with_labels=False, node_size=75, node_color='skyblue',edge_color='gray')
    plt.title('Supernode Graph')
    plt.show()

    #with open(output_file_path, 'w') as file:
    #    for i, community in enumerate(louvain_coms):
    #        file.write(f"Community {i + 1}: {list(community)}\n")



def main():
    graph = parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"))
    print(graph)
    print(graph_density(graph))
    basic_info(graph)

    #filter_by_date_example(graph)
