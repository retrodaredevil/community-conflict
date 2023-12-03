from pathlib import Path

import networkx as nx
import  random
from community_conflict.cache import read_or_parse_file
from community_conflict.subgraphs import sample_edges
from community_conflict.subgraphs import sample_nodes
import matplotlib.pyplot as plt

def draw_graph(graph: nx.graph, layout: int = 3, color_type: bool = False, node_size: int = 50, edge_width: float = 0.75):
    # positions for all nodes and layouts
    if(layout == 0):
        pos = nx.kamada_kawai_layout(graph) # looks nice, computationaly expensive, and does work well with bigger networks for some reason
    elif(layout == 1):
        pos = nx.random_layout(graph) #random places nodes looks squarish
    elif(layout == 2):
        pos = nx.shell_layout(graph) #makes an oval
    elif(layout == 3):
        pos = nx.spring_layout(graph) #ovalish but with random nodes thrown around
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

    # Draw edges
    nx.draw_networkx_edges(graph, pos, width=edge_width, edge_color='#505050', arrows=True, connectionstyle='arc3, rad = 0')

    # Draw labels
    #nx.draw_networkx_labels(graph, pos, font_size=3, font_color='black')

    # Display the graph
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()

def main():
    graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    edgeSub = sample_edges(graph, 500)
    print(edgeSub)
    #nodeSub = sample_nodes(graph, 50)
    #print(nodeSub)
    draw_graph(edgeSub, layout = 2)
    #draw_graph(nodeSub, layout = 0)

if __name__ == '__main__':
    main()