import argparse
import statistics

import matplotlib
import matplotlib.pyplot as plt
import scipy  # type: ignore

from . import utils


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)
    # x-value: average cpu usage
    # y-value: average energy usage / average runtime

    xs = []
    ys = []

    for language in args.languages:
        for benchmark in data[language].keys():
            if args.no_mean:
                for r in data[language][benchmark]:
                    xs.append(
                        utils.cpu_usage(
                            utils.timeval_to_seconds(r["rusage"]["ru_utime"]),
                            utils.timeval_to_seconds(r["rusage"]["ru_stime"]),
                            1e-3 * r["runtime_ms"],
                        )
                    )

                    ys.append(
                        sum([s["energy"]["pkg"] for s in r["energy_samples"]])
                        / (1e-3 * r["runtime_ms"])
                    )
            else:
                xs.append(
                    statistics.mean(
                        [
                            utils.cpu_usage(
                                utils.timeval_to_seconds(r["rusage"]["ru_utime"]),
                                utils.timeval_to_seconds(r["rusage"]["ru_stime"]),
                                1e-3 * r["runtime_ms"],
                            )
                            for r in data[language][benchmark]
                        ]
                    )
                )

                ys.append(
                    statistics.mean(
                        [
                            sum([s["energy"]["pkg"] for s in r["energy_samples"]])
                            / (1e-3 * r["runtime_ms"])
                            for r in data[language][benchmark]
                        ]
                    )
                )

    plt.rcParams["font.family"] = "Linux Libertine"
    with plt.style.context("bmh"):
        plt.scatter(xs, ys)

        slope, intercept, rvalue, _, _ = scipy.stats.linregress(xs, ys)
        print(f"slope: {slope}, intercept: {intercept}")
        plt.plot(
            [min(xs), max(xs)],
            [intercept + slope * min(xs), intercept + slope * max(xs)],
            color="red",
        )
        print(f"rvalue: {rvalue}")

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
    parser.add_argument("--no-mean", action="store_true")
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--no-title", action="store_true")
    main(parser.parse_args())
