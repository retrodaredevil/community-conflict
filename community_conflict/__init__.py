from pathlib import Path

import networkx as nx
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
            print(f"{source_subreddit:>25}  -->  {target_subreddit}")

    return graph


def main():
    parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"))

