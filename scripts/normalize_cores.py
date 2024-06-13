import argparse
import statistics

import matplotlib.pyplot as plt
import scipy

from . import utils


def main(args: argparse.Namespace) -> None:
    data, benchmarks = utils.parse(args.data_root, args.languages)
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

    # Group by language:
    xs_grouped = []
    ys_grouped = []

    for language in args.languages:
        xs_grouped.append([])
        ys_grouped.append([])
        for benchmark in data[language].keys():
            if args.no_mean:
                for r in data[language][benchmark]:
                    xs_grouped[-1].append(
                        utils.cpu_usage(
                            utils.timeval_to_seconds(r["rusage"]["ru_utime"]),
                            utils.timeval_to_seconds(r["rusage"]["ru_stime"]),
                            1e-3 * r["runtime_ms"],
                        )
                    )

                    ys_grouped[-1].append(
                        sum([s["energy"]["pkg"] for s in r["energy_samples"]])
                        / (1e-3 * r["runtime_ms"])
                    )
            else:
                xs_grouped[-1].append(
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

                ys_grouped[-1].append(
                    statistics.mean(
                        [
                            sum([s["energy"]["pkg"] for s in r["energy_samples"]])
                            / (1e-3 * r["runtime_ms"])
                            for r in data[language][benchmark]
                        ]
                    )
                )

    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    with plt.style.context("bmh"):
        plt.scatter(xs, ys)
        plt.plot(list(range(1, 17)), [
            34.1687, 46.5196, 50.3137, 52.3241, 54.5677, 56.5167, 58.4932, 60.9066, 63.8334, 66.3835, 68.3035, 70.4256, 73.0678, 75.3255, 77.6687, 79.6539
        ], color="red", linestyle='dashed',)

        # Plot grouped"
        # for i, language in enumerate(args.languages):
        #     plt.scatter(xs_grouped[i], ys_grouped[i], label=language.replace("#", "\\#"))
        # plt.legend()

        # slope, intercept, _, p_value, _ = scipy.stats.linregress(xs, ys)
        # plt.plot(
        #     [min(xs), max(xs)],
        #     [intercept + slope * min(xs), intercept + slope * max(xs)],
        #     color="red",
        # )
        # print(f"p-value: {p_value}")

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
