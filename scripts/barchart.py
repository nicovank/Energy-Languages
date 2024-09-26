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
                            s["energy"]["pkg"] + s["energy"]["dram"]
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

    print(runtime_bar, energy_bar)

    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        width = 0.25

        plt.barh(
            [3 * width / 2, 3 * width / 2 + 1],
            [1, 1],
            width,
            label=args.a,
        )

        plt.barh(
            [width / 2, width / 2 + 1],
            [runtime_bar, energy_bar],
            width,
            label=args.b,
        )

        plt.legend()
        plt.yticks(
            [width, width + 1], ["Relative runtime", "Relative energy consumption"]
        )
        plt.grid(visible=None, which="major", axis="y")
        plt.tick_params(axis="y", length=0)

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
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
