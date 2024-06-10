import argparse
import math
import statistics

import matplotlib.pyplot as plt

from . import utils


def main(args: argparse.Namespace) -> None:
    data, benchmarks = utils.parse(args.data_root, args.languages)
    # x-value: average cpu usage
    # y-value: average energy usage / average runtime

    xs = []
    ys = []

    for language in args.languages:
        for benchmark in data[language].keys():
            x = statistics.mean(
                [
                    utils.cpu_usage(
                        utils.timeval_to_seconds(r["rusage"]["ru_utime"]),
                        utils.timeval_to_seconds(r["rusage"]["ru_stime"]),
                        1e-3 * r["runtime_ms"],
                    )
                    for r in data[language][benchmark]
                ]
            )

            y = statistics.mean(
                [
                    sum([s["energy"]["pkg"] for s in r["energy_samples"]])
                    / (1e-3 * r["runtime_ms"])
                    for r in data[language][benchmark]
                ]
            )

            xs.append(x)
            ys.append(y)

    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    with plt.style.context("bmh"):
        plt.scatter(xs, ys)
        plt.xlabel("Average cores used")
        plt.ylabel("Average power [W]")
        plt.ylim(bottom=0)
        plt.savefig(f"normalize_cores.{args.format}", format=args.format)


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
    parser.add_argument("--no-title", action="store_true")
    main(parser.parse_args())
