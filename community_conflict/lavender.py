from pathlib import Path

from community_conflict.cache import read_or_parse_file


def main():
    graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    print(graph)


if __name__ == '__main__':
    main()
