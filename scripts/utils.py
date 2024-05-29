import collections
import json
import os
from typing import Any, Dict, List, Tuple


def parse(
    data_root: str, languages: List[str]
) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    for language in languages:
        LANGUAGES_ROOT = os.path.join(data_root, language)
        if not os.path.isdir(LANGUAGES_ROOT):
            languages.remove(language)
            print(f"Warning: {LANGUAGES_ROOT} does not exist, skipping")
            continue
        for benchmark in os.listdir(LANGUAGES_ROOT):
            path = os.path.join(LANGUAGES_ROOT, benchmark)
            assert os.path.isfile(path) and path.endswith(".json")
            benchmark = benchmark[:-5]
            with open(path, "r") as file:
                for line in file:
                    line = json.loads(line)
                    data[language][benchmark].append(line)

    benchmarks = sorted(list({b for l in data.values() for b in l.keys()}))
    return data, benchmarks
