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
        benchmark: {
            language: (
                statistics.geometric_mean(
                    [1e-3 * r["runtime_ms"] for r in data[language][benchmark]]
                )
            )
            for language in [args.a, args.b]
        }
        for benchmark in benchmarks
    }

    energies = {
        language: {
            benchmark: statistics.geometric_mean(
                [
                    sum(
                        [
                            s["energy"]["pkg"] + s["energy"]["dram"]
                            for s in r["energy_samples"]
                        ]
                    )
                    for r in data[language][benchmark]
                ]
            )
            for benchmark in benchmarks
            if benchmark in data[language]
        }
        for language in [args.a, args.b]
    }

    plt.rcParams["font.family"] = "Linux Libertine"
    with plt.style.context("bmh"):
        y = np.arange(len(benchmarks))
        width = 0.25

        fig, ax = plt.subplots(layout="constrained")

        ax.barh(
            y + 3 * width / 2,
            [runtimes[benchmark][args.a] for benchmark in benchmarks],
            width,
            label=args.a,
        )

        ax.barh(
            y + width / 2,
            [runtimes[benchmark][args.b] for benchmark in benchmarks],
            width,
            label=args.b,
        )

        ax.legend()
        ax.set_yticks(y + width, benchmarks)
        ax.grid(visible=None, which="major", axis="y")
        ax.yaxis.set_tick_params(length=0)
        ax.set_xlabel("Runtime [s]")
        ax.set_ylabel("Benchmark")
        ax.set_xlim(right=100)

        plt.savefig(f"barchart.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "a",
        type=str,
        default="Lua",
    )
    parser.add_argument(
        "b",
        type=str,
        default="LuaJIT",
    )
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
