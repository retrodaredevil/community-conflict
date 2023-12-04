from pathlib import Path
import networkx as nx
import  random
from community_conflict.cache import read_or_parse_file
from community_conflict.subgraphs import sample_edges
from community_conflict.subgraphs import sample_nodes
from community_conflict.collapse import collapse
import matplotlib.pyplot as plt
"""
Purpose: To help visualize multi directed networks by drawing it in a output window
Parameters: 
graph - takes in a MultiDiGraph
layout - integer from (0 to 7) to determine the layout used
color_type - boolean detemines whether or not the function is mono-colored or multi-colored nodes
node_size - integer determines size of nodes
edge_width - boolean determines width of edges
edge_arc - float determines the curviture of the edges
"""
def draw_graph(graph: nx.MultiDiGraph, layout: int = 6, color_type: bool = False, node_size: int = 50, edge_width: float = 0.75, edge_arc: float = 0.0):
    # positions for all nodes and layouts
    if(layout == 0):
        pos = nx.bipartite_layout(graph, graph.nodes)# makes a line if not used on bipartite graph
    elif(layout == 1):
        pos = nx.circular_layout(graph) # makes a nice-ish looking oval
    elif(layout == 2):
        pos = nx.kamada_kawai_layout(graph) # looks nice, computationaly expensive, and does work well with bigger networks for some reason
    elif(layout == 3):
        pos = nx.planar_layout(graph) #looks like a pyramaid(This is one of my favorites - Ian)
    elif(layout == 4):
        pos = nx.random_layout(graph) #random places nodes looks squarish
    elif(layout == 5):
        pos = nx.shell_layout(graph) #makes an oval with overlap kind harsh on the eyes
    elif(layout == 6):
        pos = nx.spring_layout(graph) #ovalish but with random nodes thrown around(default option easy to manage)
    else:
        pos = nx.spiral_layout(graph) #makes a spiral

    if(color_type ==  True):
        count = graph.number_of_nodes()
        colors = []
        count = ["#f24141", "#60a152", "#4287f5", "#d45085"]
        for _ in range(len(list(graph.nodes))):
            colors.append(random.choice(count))
    else:
        colors = "#aaabff"

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=node_size)

    # Draw edge
    #edge_arc is a float that determines how much an arc curves(recommended to stay between 0 and 1)
    nx.draw_networkx_edges(graph, pos, width=edge_width, edge_color='#505050', arrows=True, connectionstyle = f'arc3, rad = {edge_arc}')

    # Draw labels
    #nx.draw_networkx_labels(graph, pos, font_size=3, font_color='black')

    # Display the graph
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()

def draw_communities(graph: nx.MultiDiGraph):
    node_size = []
    community_graph = nx.Graph()
    collapsed_graph = collapse(graph)
    communities = list(nx.algorithms.community.louvain_communities(collapsed_graph))
    for i, community in enumerate(communities):
        if len(community) >= 20:
            node_size.append(len(community)/2)
            community_graph.add_node(i, count = len(community))

    pos = nx.spring_layout(community_graph)
    nx.draw_networkx_nodes(community_graph, pos, node_color="#aaabff", node_size=node_size)
    nx.draw_networkx_edges(community_graph, pos, width=.75, edge_color='#505050', arrows=True, connectionstyle = f'arc3, rad = 0.0')
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()

    

def main():
    title_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    #edgeSub = sample_edges(graph, 500)
    #print(edgeSub)
    #nodeSub = sample_nodes(graph, 50)
    #print(nodeSub)
    #draw_graph(edgeSub, edge_arc = 0.6)
    #draw_graph(nodeSub, layout = 0)
    draw_communities(title_graph)


if __name__ == '__main__':
    main()