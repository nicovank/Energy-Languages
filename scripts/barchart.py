import argparse
import collections
import json
import math
import os
import statistics

import matplotlib.pyplot as plt
import numpy as np


def main(args):
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    for language in args.languages:
        LANGUAGES_ROOT = os.path.join(args.data_root, language)
        if not os.path.isdir(LANGUAGES_ROOT):
            args.languages.remove(language)
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
    runtimes = {
        benchmark: {
            language: statistics.geometric_mean(
                [r["runtime"] for r in data[language][benchmark]]
            )
            if benchmark in data[language]
            else 0
            for language in args.languages
        }
        for benchmark in benchmarks
    }

    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    with plt.style.context("bmh"):
        x = np.arange(len(benchmarks))
        width = 0.25
        multiplier = 0

        fig, ax = plt.subplots(layout="constrained")

        for language in args.languages:
            offset = width * multiplier
            rects = ax.bar(
                x + offset,
                [runtimes[benchmark][language] for benchmark in benchmarks],
                width,
                label=language,
            )
            multiplier += 1

        ax.legend()
        ax.set_xticks(x + width, benchmarks)
        ax.tick_params(axis="x", labelrotation=90, length=0)
        ax.grid(visible=None, which="major", axis="x")
        ax.set_ylabel("Runtime [ms]")
        if not args.no_title:
            plt.title("Benchmark Performance by Language")

        plt.savefig(f"barchart.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        default=["C", "C++", "Rust"],
    )
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--no-title", action="store_true")
    main(parser.parse_args())
