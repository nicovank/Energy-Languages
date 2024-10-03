import argparse
import math
import statistics

import matplotlib
import matplotlib.pyplot as plt
import scipy  # type: ignore

from . import utils


def human_readable(x):
    assert math.isclose(int(x), x)
    if x < 1e3:
        return f"{int(x)}"
    if x < 1e6:
        return f"{int(x / 1e3)}k"
    if x < 1e9:
        return f"{int(x / 1e6)}M"
    return f"{int(x / 1e9)}G"


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
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5)
        ax.set_facecolor("white")

        ax.scatter(xs, ys, s=10)

        slope, intercept, rvalue, _, _ = scipy.stats.linregress(xs, ys)
        print(f"slope: {slope:.2e}, intercept: {intercept:.2f}")
        ax.plot(
            [min(xs), max(xs)],
            [intercept + slope * min(xs), intercept + slope * max(xs)],
            color="red",
            linewidth=1,
        )
        print(f"R^2: {rvalue ** 2:.2f}")

        ax.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: human_readable(x))
        )

        ax.set_xlabel("LLC misses per second")
        ax.set_ylabel("Average power draw (DRAM) [W]")
        ax.set_ylim(bottom=0)
        fig.tight_layout()
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
