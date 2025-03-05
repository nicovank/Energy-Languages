import argparse
import json
import os
import statistics
from typing import Any

import matplotlib.pyplot as plt
from packaging.version import Version


def parse_data(data_root: str) -> dict[str, Any]:
    data = {}
    for entry in os.listdir(data_root):
        if not entry.endswith(".json") or not entry.startswith("pyperformance-"):
            continue
        path = os.path.join(data_root, entry)
        assert os.path.isfile(path)
        # Format: pyperformance-<VERSION>.json
        python_version = entry[14:-5]
        with open(path, "r") as file:
            data[python_version] = json.load(file)
    return data


def main(args: argparse.Namespace):
    data = parse_data(args.data_root)
    versions = sorted(data.keys(), key=lambda v: Version(v))
    min_version = versions[0]
    benchmarks = list(
        set.intersection(
            *[set(entry["name"] for entry in entries) for entries in data.values()]
        )
    )
    means = {
        version: {e["name"]: e["mean_ns"] for e in data[version]}
        for version in versions
    }
    sigmas = {
        version: {e["name"]: e["sigma_ns"] for e in data[version]}
        for version in versions
    }

    # Pick the n benchmarks with the highest mean runtime for the lowest Python version.
    benchmarks.sort(key=lambda b: means[min_version][b], reverse=True)
    benchmarks = benchmarks[: args.n]

    # Normalize means to lowest version.
    for benchmark in benchmarks:
        baseline = means[min_version][benchmark]
        for version in versions:
            means[version][benchmark] /= baseline
            sigmas[version][benchmark] /= baseline

    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        if args.half_size:
            fig.set_size_inches(4, 3)
        else:
            fig.set_size_inches(8, 5)
        ax.set_facecolor("white")

        for benchmark in benchmarks:
            print(benchmark, [means[version][benchmark] for version in versions])
            ax.errorbar(
                versions,
                [means[version][benchmark] for version in versions],
                yerr=[sigmas[version][benchmark] for version in versions],
                label=benchmark,
                marker="o",
                capsize=5,
            )

        ax.set_xlabel("Python version")
        ax.set_ylabel("Normalized runtime")
        ax.set_ylim(bottom=0)
        plt.tight_layout()
        plt.savefig(f"benchmark_comparison.{args.format}", format=args.format)
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument("-n", type=int, default=10)
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--half-size", default=False, action="store_true")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
