import collections
import json
import os
from typing import Any, Dict, List, Tuple


def parse(
    data_root: str, languages: List[str]
) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    data: Dict[str, Dict[str, Any]] = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )
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

    benchmarks: List[str] = sorted(list({b for l in data.values() for b in l.keys()}))
    return data, benchmarks


def timeval_to_seconds(tv: Dict[str, float]) -> float:
    return tv["tv_sec"] + 1e-6 * tv["tv_usec"]


def cpu_usage(user_cpu_time: float, kernel_cpu_time: float, runtime: float) -> float:
    return (user_cpu_time + kernel_cpu_time) / runtime
