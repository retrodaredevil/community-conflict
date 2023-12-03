from pathlib import Path

import networkx as nx

from community_conflict.cache import read_or_parse_file
from community_conflict.collapse import collapse


def main():
    outputs_directory = Path("outputs")
    outputs_directory.mkdir(exist_ok=True)

    title_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"),
                                     Path(".cache/soc-redditHyperlinks-title.pickle"))
    body_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-body.tsv"),
                                    Path(".cache/soc-redditHyperlinks-body.pickle"))
    for name, graph in [
        ("title", title_graph),
        ("body", body_graph),
    ]:
        print()
        print(name)
        collapsed_graph = collapse(graph)
        print(collapsed_graph)
        louvain_coms = list(nx.algorithms.community.louvain_communities(collapsed_graph))
        with open(Path("outputs", f"{name}.txt"), 'w') as file:
            for i, community in enumerate(louvain_coms):
                if len(community) >= 3:
                    print(f"Community {i + 1}: {community}", file=file)


if __name__ == '__main__':
    main()
