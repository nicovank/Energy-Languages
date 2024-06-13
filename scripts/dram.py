import argparse
import statistics

import matplotlib.pyplot as plt

from . import utils


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    xs = []
    ys = []

    for language in args.languages:
        for benchmark in data[language].keys():
            memory_operations_per_second = statistics.median(
                [
                    r["counters"]["PERF_COUNT_HW_CACHE_MISSES"]
                    / (1e-3 * r["runtime_ms"])
                    for r in data[language][benchmark]
                ]
            )

            dram_energy_per_second = statistics.median(
                [
                    sum([s["energy"]["dram"] for s in r["energy_samples"]])
                    / (1e-3 * r["runtime_ms"])
                    for r in data[language][benchmark]
                ]
            )

            xs.append(memory_operations_per_second)
            ys.append(dram_energy_per_second)

    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    with plt.style.context("bmh"):
        plt.scatter(xs, ys)

        plt.xlabel("Memory operations per second [1/s]")
        plt.ylabel("Power [W]")
        plt.ylim(bottom=0)
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
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
