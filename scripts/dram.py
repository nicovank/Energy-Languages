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
    return f"{x / 1e9:.1f}".rstrip(".0") + "G"


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    all_xs = []
    all_ys = []

    min_ratio = math.inf
    max_ratio = 0.0

    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        if args.half_size:
            fig.set_size_inches(4, 3)
        else:
            fig.set_size_inches(8, 5)
        ax.set_facecolor("white")

        all_xs = []
        all_ys = []

        for suite in utils.suites():
            suite_xs = []
            suite_ys = []
            for language in args.languages:
                for benchmark in data[language].keys():
                    if benchmark not in utils.benchmarks_by_suite(suite):
                        continue

                    for r in data[language][benchmark]:
                        ratio = sum(
                            [
                                sum(e["dram"] for e in s["energy"])
                                for s in r["energy_samples"]
                            ]
                        ) / sum(
                            [
                                sum(e["pkg"] for e in s["energy"])
                                for s in r["energy_samples"]
                            ]
                        )
                        min_ratio = min(min_ratio, ratio)
                        max_ratio = max(max_ratio, ratio)

                        x = r["counters"]["PERF_COUNT_HW_CACHE_MISSES"] / (
                            1e-3 * r["runtime_ms"]
                        )
                        if x > args.xmax:
                            continue
                        suite_xs.append(x)
                        suite_ys.append(
                            sum(
                                [
                                    sum(e["dram"] for e in s["energy"])
                                    for s in r["energy_samples"]
                                ]
                            )
                            / (1e-3 * r["runtime_ms"])
                        )

            if not suite_xs or not suite_ys:
                continue

            ax.scatter(
                suite_xs,
                suite_ys,
                s=(0.5 if args.half_size else 1),
                label=utils.pretty_suite_name(suite),
            )

            all_xs.extend(suite_xs)
            all_ys.extend(suite_ys)

        print(
            f"% of DRAM energy over CPU energy: {min_ratio * 100:.2f}% - {max_ratio * 100:.2f}%"
        )

        slope, intercept, rvalue, _, _ = scipy.stats.linregress(all_xs, all_ys)
        print(f"slope: {slope:.2e}, intercept: {intercept:.2f}")
        ax.plot(
            [min(all_xs), max(all_xs)],
            [intercept + slope * min(all_xs), intercept + slope * max(all_xs)],
            color="red",
            linewidth=1,
        )
        print(f"R^2: {rvalue ** 2:.2f}")

        ax.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: human_readable(x))
        )

        ax.set_xlabel(
            "LLC misses per second", fontsize=("medium" if args.half_size else "large")
        )
        ax.set_ylabel(
            "Average power draw (DRAM) [W]",
            fontsize=("medium" if args.half_size else "large"),
        )
        ax.set_ylim(bottom=0)
        if args.ymax:
            ax.set_ylim(top=args.ymax)
        legend = ax.legend()
        for handle in legend.legend_handles:
            handle.set_sizes([10])
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
    parser.add_argument("--half-size", default=False, action="store_true")
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--xmax", type=float, default=math.inf)
    parser.add_argument("--ymax", type=float, default=None)
    main(parser.parse_args())
