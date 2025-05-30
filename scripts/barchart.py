import argparse
import statistics

import matplotlib.pyplot as plt
import numpy as np

from . import utils


def main(args: argparse.Namespace) -> None:
    data, benchmarks = utils.parse(args.data_root, [args.a, args.b])

    benchmarks = sorted(list({b for l in data.values() for b in l.keys()}))

    for benchmark in list(benchmarks):
        if benchmark not in data[args.a]:
            print(f"Missing benchmark {benchmark} in {args.a}")
            benchmarks.remove(benchmark)
        if benchmark not in data[args.b]:
            print(f"Missing benchmark {benchmark} in {args.b}")
            benchmarks.remove(benchmark)

    runtimes = {
        language: {
            benchmark: (
                statistics.median(
                    [1e-3 * r["runtime_ms"] for r in data[language][benchmark]]
                )
            )
            for benchmark in benchmarks
        }
        for language in [args.a, args.b]
    }

    energies = {
        language: {
            benchmark: statistics.median(
                [
                    sum(
                        [
                            sum(e["pkg"] + e["dram"] for e in s["energy"])
                            for s in r["energy_samples"]
                        ]
                    )
                    for r in data[language][benchmark]
                ]
            )
            for benchmark in benchmarks
        }
        for language in [args.a, args.b]
    }

    runtime_bar = statistics.geometric_mean(
        [runtimes[args.b][b] / runtimes[args.a][b] for b in benchmarks]
    )

    energy_bar = statistics.geometric_mean(
        [energies[args.b][b] / energies[args.a][b] for b in benchmarks]
    )

    if args.a == "Python":
        args.a = "CPython"
    if args.b == "Python":
        args.b = "CPython"

    print(runtime_bar, energy_bar)

    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        ax.set_facecolor("white")
        fig.set_size_inches(4, 2)

        spacing = 0.5
        width = 0.2  # < spacing / 2

        ax.barh(
            [width / 2, spacing + width / 2],
            [1, 1],
            width,
            label=args.a,
        )

        ax.barh(
            [-width / 2, spacing - width / 2],
            [runtime_bar, energy_bar],
            width,
            label=args.b,
        )

        ax.legend(
            loc="center",
            bbox_to_anchor=(0.5, 1.2),
            ncol=2,
            facecolor="white",
            edgecolor="white",
        )

        ax.set_yticks([0, spacing], ["Runtime", "Energy\nConsumption"])
        ax.set_ylim(-0.4, 0.9)
        ax.grid(visible=None, which="major", axis="y")
        ax.tick_params(axis="y", length=0)
        fig.tight_layout()
        plt.savefig(f"barchart.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "a",
        type=str,
    )
    parser.add_argument(
        "b",
        type=str,
    )
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
