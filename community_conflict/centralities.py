import pickle
import networkx as nx

def compute_centraities(graph):
    """Compute various centrality measures relevant to our data and
       saves them to the computed_values folder"""
    # TODO: Katz centralities don't seem to converge with the default iterations of 1000. Possibly try larger
    # print("Computing Katz Centralities")
    # katz_cent = nx.katz_centrality(graph, max_iter=1000)
    # print("Katz centralities:", katz_cent)

    # Completed
    # with open("computed_values/closeness_cent", "wb") as f:
    #     print("Computing Closeness Centralities")
    #     closeness_cent = nx.closeness_centrality(graph)
    #     pickle.dump(closeness_cent, f)

    # Completed
    # with open("computed_values/node_betweenness_cent", "wb") as f:
    #     print("Computing Node Betweenness Centralities")
    #     node_betweenness_cent = nx.betweenness_centrality(graph)
    #     pickle.dump(node_betweenness_cent, f)

    # TODO: This one might be useful, but will likely take a very long time to compute properly
    # with open("computed_values/edge_betweenness_cent", "wb") as f:
    #     print("Computing Edge Betweenness Centralities")
    #     edge_betweenness_cent = nx.edge_betweenness_centrality(graph)
    #     pickle.dump(edge_betweenness_cent, f)

    # Completed
    # with open("computed_values/harmonic_cent", "wb") as f:
    #     print("Computing Harmonic Centralities")
    #     harmonic_cent = nx.harmonic_centrality(graph)
    #     pickle.dump(harmonic_cent, f)

    # Completed
    # with open("computed_values/degree_cent", "wb") as f:
    #     print("Computing Degree Centralities")
    #     degree_cent = nx.degree_centrality(graph)
    #     pickle.dump(degree_cent, f)


def show_centralities():
    # Node Betweenness Centrality
    with open("computed_values/node_betweenness_cent", "rb") as f:
        node_betweenness_cent = pickle.load(f)
    sorted_node_betweenness_cent = sorted(node_betweenness_cent.items(), key=lambda x: x[1], reverse=True)
    print("|{:<25}|{:>25}|".format("Subreddit Name", "Betweenness Centrality"))
    print("_"*53)
    for node in sorted_node_betweenness_cent[:15]:
        print("|{:<25}|{:>25.10f}|".format(node[0], node[1]))

    print("\n")

    # Degree Centrality
    with open("computed_values/degree_cent", "rb") as f:
        degree_cent = pickle.load(f)
    degree_cent = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)
    print("|{:<25}|{:>25}|".format("Subreddit Name", "Degree Centrality"))
    print("_"*53)
    for node in degree_cent[:15]:
        print("|{:<25}|{:>25.10f}|".format(node[0], node[1]))
