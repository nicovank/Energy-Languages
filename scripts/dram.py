import argparse
import math
import statistics

import matplotlib.pyplot as plt
import scipy  # type: ignore

from . import utils


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    xs = []
    ys = []

    min_ratio = math.inf
    max_ratio = 0.0

    for language in args.languages:
        for benchmark in data[language].keys():
            for r in data[language][benchmark]:
                ratio = sum(
                    [sum(e["dram"] for e in s["energy"]) for s in r["energy_samples"]]
                ) / sum(
                    [sum(e["pkg"] for e in s["energy"]) for s in r["energy_samples"]]
                )
                min_ratio = min(min_ratio, ratio)
                max_ratio = max(max_ratio, ratio)
            x = statistics.median(
                [
                    r["counters"]["PERF_COUNT_HW_CACHE_MISSES"]
                    / (1e-3 * r["runtime_ms"])
                    for r in data[language][benchmark]
                ]
            )
            if x > args.xmax:
                continue
            xs.append(x)
            ys.append(
                statistics.median(
                    [
                        sum(
                            [
                                sum(e["dram"] for e in s["energy"])
                                for s in r["energy_samples"]
                            ]
                        )
                        / (1e-3 * r["runtime_ms"])
                        for r in data[language][benchmark]
                    ]
                )
            )

    print(
        f"% of DRAM energy over CPU energy: {min_ratio * 100:.2f}% - {max_ratio * 100:.2f}%"
    )

    plt.rcParams["font.family"] = args.font
    plt.gcf().set_size_inches(8, 5)
    with plt.style.context("bmh"):
        plt.scatter(xs, ys, s=10)

        slope, intercept, rvalue, _, _ = scipy.stats.linregress(xs, ys)
        print(f"slope: {slope:.2e}, intercept: {intercept:.2f}")
        plt.plot(
            [min(xs), max(xs)],
            [intercept + slope * min(xs), intercept + slope * max(xs)],
            color="red",
            linewidth=1,
        )
        print(f"R^2: {rvalue ** 2:.2f}")

        plt.xlabel("LLC misses per second [1/s]")
        plt.ylabel("Average power draw (DRAM) [W]")
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig(f"dram.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        required=True,
    )
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--xmax", type=int, default=math.inf)
    main(parser.parse_args())
