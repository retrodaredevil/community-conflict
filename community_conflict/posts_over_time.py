import calendar
from datetime import datetime
from pathlib import Path
from typing import List

import networkx as nx
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt

from community_conflict.cache import read_or_parse_file


def visualize_number_of_edges_each_month_in_range(title_prefix: str, start_date: datetime, end_date: datetime, graph: nx.DiGraph):
    step = relativedelta(months=1)
    edges = graph.edges(data=True)

    node_names: List[str] = []
    values: List[int] = []

    period_start = start_date
    while (period_end := period_start + step) <= end_date:
        new_graph = graph.edge_subgraph(
            (edge[0], edge[1]) for edge in edges if period_start <= edge[2]["timestamp"] <= period_end
        )
        node_names.append(f"{calendar.month_name[period_start.month]} {period_start.year}")
        values.append(len(new_graph.edges))

        period_start = period_end

    plt.bar(range(len(node_names)), values, tick_label=node_names)
    plt.xlabel('Month')
    plt.ylabel("Number of Posts")
    plt.title(f"{title_prefix} - Number of posts each month")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()


def main():
    start_date = datetime(2014, 1, 1)
    end_date = datetime(2017, 5, 1)

    title_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"), Path(".cache/soc-redditHyperlinks-title.pickle"))
    body_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-body.tsv"), Path(".cache/soc-redditHyperlinks-body.pickle"))
    for name, graph in [("title", title_graph), ("body", body_graph)]:
        print()
        print(name)
        visualize_number_of_edges_each_month_in_range(f"{name} dataset", start_date, end_date, graph)


if __name__ == '__main__':
    main()
