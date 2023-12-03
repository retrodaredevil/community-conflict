import pickle
import traceback
from pathlib import Path

import networkx as nx

from community_conflict import parse_file


def read_or_parse_file(raw_data_file: Path, cache_file: Path) -> nx.MultiDiGraph:
    try:
        if cache_file.exists():
            with cache_file.open('rb') as f:
                graph = pickle.load(f)
            # We have this if statement here because we used to only store the data as a DiGraph.
            #   So, if we come across a cache that is a DiGraph but not a MultiDiGraph, we need to parse the file again
            if isinstance(graph, nx.MultiDiGraph):
                return graph
    except OSError:
        raise  # we don't expect an OSError, as we should have correct permissions to write to the directory
    except Exception:
        traceback.print_exc()
        print("Failed to use cache file. Going to try to cache it again")

    graph = parse_file(raw_data_file)

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with cache_file.open('wb') as f:
        pickle.dump(graph, f)
    return graph
