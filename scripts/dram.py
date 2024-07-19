import argparse
import statistics

import matplotlib.pyplot as plt
import scipy  # type: ignore

from . import utils


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    xs = []
    ys = []

    for language in args.languages:
        for benchmark in data[language].keys():
            if args.no_mean:
                for r in data[language][benchmark]:
                    xs.append(
                        r["counters"]["PERF_COUNT_HW_CACHE_MISSES"]
                        / (1e-3 * r["runtime_ms"])
                    )
                    ys.append(
                        sum([s["energy"]["dram"] for s in r["energy_samples"]])
                        / (1e-3 * r["runtime_ms"])
                    )
            else:
                xs.append(
                    statistics.median(
                        [
                            r["counters"]["PERF_COUNT_HW_CACHE_MISSES"]
                            / (1e-3 * r["runtime_ms"])
                            for r in data[language][benchmark]
                        ]
                    )
                )
                ys.append(
                    statistics.median(
                        [
                            sum([s["energy"]["dram"] for s in r["energy_samples"]])
                            / (1e-3 * r["runtime_ms"])
                            for r in data[language][benchmark]
                        ]
                    )
                )

    plt.rcParams["font.family"] = "Linux Libertine"
    plt.gcf().set_size_inches(8, 5)
    with plt.style.context("bmh"):
        plt.scatter(xs, ys, s=10)

        slope, intercept, rvalue, _, _ = scipy.stats.linregress(xs, ys)
        print(f"slope: {slope}, intercept: {intercept}")
        plt.plot(
            [min(xs), max(xs)],
            [intercept + slope * min(xs), intercept + slope * max(xs)],
            color="red",
            linewidth=1,
        )
        print(f"rvalue: {rvalue}")

        plt.xlabel("LLC misses per second")
        plt.ylabel("Power [W]")
        plt.ylim(bottom=0)
        # plt.xlim(right=0.5e8)
        plt.tight_layout()
        plt.savefig(f"dram.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        default=[
            "C",
            "C++",
            "Rust",
            "Go",
            "Java",
            "C#",
            "JavaScript",
            "TypeScript",
            "PHP",
            "Python",
            "Lua",
        ],
    )
    parser.add_argument("--no-mean", action="store_true")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
