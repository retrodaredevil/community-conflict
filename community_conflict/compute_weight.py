from datetime import datetime
from typing import List
import networkx as nx
from pathlib import Path
from community_conflict import PROPERTY_KEYS
from community_conflict.cache import read_or_parse_file

def weight(edge_data_list: List[dict]):
    weight = 0
    for property in range(PROPERTY_KEYS.index("LIWC_Funct"), len(edge_data_list[0]['properties'])):
        sum_of_property = 0
        for edge in edge_data_list:
            sum_of_property += edge['properties'][property]
        sum_of_property /= len(edge_data_list)
        weight += sum_of_property ** 2
    return weight
        
def main():
    # graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    # new_graph = convert_graph(graph)

    #dummy data
    edge_data_list = [
        {'post_id': '1ukk0ns', 'timestamp': datetime(2014, 1, 7, 9, 25, 59), 'link_sentiment': 1, 'properties': [56.0, 49.0, 0.785714285714, 0.0, 0.178571428571, 0.142857142857, 0.0714285714286, 10.0, 10.0, 1.0, 4.4, 1.0, 0.1, 1.0, 0.0, 56.0, 10.0, 9.946, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.18181818181818182, 0.09090909090909091, 0.09090909090909091, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
        {'post_id': '1ukk0ns', 'timestamp': datetime(2014, 1, 7, 9, 25, 59), 'link_sentiment': 1, 'properties': [56.0, 49.0, 0.785714285714, 0.0, 0.178571428571, 0.142857142857, 0.0714285714286, 10.0, 10.0, 1.0, 4.4, 1.0, 0.1, 1.0, 0.0, 56.0, 10.0, 9.946, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.18181818181818182, 0.09090909090909091, 0.09090909090909091, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
        {'post_id': '1ukk0ns', 'timestamp': datetime(2014, 1, 7, 9, 25, 59), 'link_sentiment': 1, 'properties': [56.0, 49.0, 0.785714285714, 0.0, 0.178571428571, 0.142857142857, 0.0714285714286, 10.0, 10.0, 1.0, 4.4, 1.0, 0.1, 1.0, 0.0, 56.0, 10.0, 9.946, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.18181818181818182, 0.09090909090909091, 0.09090909090909091, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
        {'post_id': '1ukk0ns', 'timestamp': datetime(2014, 1, 7, 9, 25, 59), 'link_sentiment': 1, 'properties': [56.0, 49.0, 0.785714285714, 0.0, 0.178571428571, 0.142857142857, 0.0714285714286, 10.0, 10.0, 1.0, 4.4, 1.0, 0.1, 1.0, 0.0, 56.0, 10.0, 9.946, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.18181818181818182, 0.09090909090909091, 0.09090909090909091, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
        {'post_id': '1ukk0ns', 'timestamp': datetime(2014, 1, 7, 9, 25, 59), 'link_sentiment': 1, 'properties': [56.0, 49.0, 0.785714285714, 0.0, 0.178571428571, 0.142857142857, 0.0714285714286, 10.0, 10.0, 1.0, 4.4, 1.0, 0.1, 1.0, 0.0, 56.0, 10.0, 9.946, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.18181818181818182, 0.09090909090909091, 0.09090909090909091, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
        {'post_id': '1ukk0ns', 'timestamp': datetime(2014, 1, 7, 9, 25, 59), 'link_sentiment': 1, 'properties': [56.0, 49.0, 0.785714285714, 0.0, 0.178571428571, 0.142857142857, 0.0714285714286, 10.0, 10.0, 1.0, 4.4, 1.0, 0.1, 1.0, 0.0, 56.0, 10.0, 9.946, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45454545454545453, 0.18181818181818182, 0.09090909090909091, 0.09090909090909091, 0.0, 0.0, 0.09090909090909091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
        #{'post_id': '1ukklqs', 'timestamp': datetime(2014, 1, 6, 17, 53, 23), 'link_sentiment': 1, 'properties': [91.0, 82.0, 0.857142857143, 0.0, 0.0769230769231, 0.10989010989, 0.032967032967, 12.0, 12.0, 6.0, 6.5, 3.0, 0.25, 1.0, 1.0, 91.0, 12.0, 20.2875, 0.217, 0.0, 0.3612, 0.23076923076923078, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.07692307692307693, 0.07692307692307693, 0.0, 0.0, 0.07692307692307693, 0.0, 0.0, 0.15384615384615385, 0.0, 0.0, 0.0, 0.0, 0.0, 0.07692307692307693, 0.0, 0.0, 0.0, 0.07692307692307693, 0.07692307692307693, 0.0, 0.0, 0.0, 0.0, 0.07692307692307693, 0.0, 0.07692307692307693, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.07692307692307693, 0.0, 0.07692307692307693, 0.0, 0.0, 0.07692307692307693, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
    ]
    print(weight(edge_data_list))

if __name__ == '__main__':
    main()