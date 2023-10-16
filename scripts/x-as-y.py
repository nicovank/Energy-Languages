import argparse
import collections
import json
import os
import statistics

import numpy as np
from rich.console import Console
from rich.table import Table


def main(args):
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    LANGUAGES = [args.x, args.y, args.experiment]
    for language in LANGUAGES:
        LANGUAGES_ROOT = os.path.join(args.data_root, language)
        assert os.path.isdir(LANGUAGES_ROOT), LANGUAGES_ROOT
        for benchmark in os.listdir(LANGUAGES_ROOT):
            path = os.path.join(LANGUAGES_ROOT, benchmark)
            assert os.path.isfile(path) and path.endswith(".json")
            benchmark = benchmark[:-5]
            with open(path, "r") as file:
                for line in file:
                    line = json.loads(line)
                    data[language][benchmark].append(line)

    benchmarks = sorted(list({b for l in data.values() for b in l.keys()}))
    benchmarks = [b for b in benchmarks if np.all([b in data[l] for l in LANGUAGES])]

    table = Table(
        title=f"Runtime geometric mean of {args.x} source benchmarks compiled in {args.x} and {args.y} modes"
    )
    table.add_column("Benchmark")
    table.add_column(f"{args.x} runtime [ms]")
    table.add_column(f"{args.y} runtime [ms]")
    table.add_column("Ratio [%]")
    table.add_column(f"Original {args.y} runtime [ms]")
    table.add_column("Ratio [%]")

    runtimes = [
        [
            statistics.geometric_mean([r["runtime"] for r in data[language][b]])
            for b in benchmarks
        ]
        for language in LANGUAGES
    ]

    for i, benchmark in enumerate(benchmarks):
        table.add_row(
            benchmark,
            f"{runtimes[0][i]:.0f}",
            f"{runtimes[2][i]:.0f}",
            f"{100 * runtimes[2][i] / runtimes[0][i]:.1f}",
            f"{runtimes[1][i]:.0f}",
            f"{100 * runtimes[1][i] / runtimes[0][i]:.1f}",
        )

    console = Console()
    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument("-x", type=str, required=True)
    parser.add_argument("-y", type=str, required=True)
    parser.add_argument("--experiment", type=str, required=True)
    main(parser.parse_args())
