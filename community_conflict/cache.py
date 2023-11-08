import pickle
import traceback
from pathlib import Path

from community_conflict import parse_file


def read_or_parse_file(raw_data_file: Path, cache_file: Path):
    try:
        if cache_file.exists():
            with cache_file.open('rb') as f:
                return pickle.load(f)
    except OSError:
        raise  # we don't expect an OSError, as we should have correct permissions to write to the directory
    except Exception as e:
        traceback.print_tb(e)
        print("Failed to use cache file. Going to try to cache it again")

    graph = parse_file(raw_data_file)

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with cache_file.open('wb') as f:
        pickle.dump(graph, f)
    return graph
