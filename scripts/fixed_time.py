import argparse
import statistics

import matplotlib.pyplot as plt

from . import utils


def main(args: argparse.Namespace) -> None:
    data, benchmarks = utils.parse(args.data_root, args.languages)

    if "Java" in data:
        data["OpenJDK"] = data.pop("Java")
        args.languages = ["OpenJDK" if l == "Java" else l for l in args.languages]
    if "Python" in data:
        data["CPython"] = data.pop("Python")
        args.languages = ["CPython" if l == "Python" else l for l in args.languages]

    language_to_index = {language: i for i, language in enumerate(args.languages)}

    runtimes = {
        language: {
            benchmark: 0.001
            * statistics.median([r["runtime_ms"] for r in data[language][benchmark]])
            for benchmark in benchmarks
            if benchmark in data[language]
        }
        for language in args.languages
    }

    cpu_usages = {
        language: {
            benchmark: statistics.median(
                [
                    (r["counters"]["PERF_COUNT_SW_TASK_CLOCK"] / 1e9)
                    / (r["runtime_ms"] / 1e3)
                    for r in data[language][benchmark]
                ]
            )
            for benchmark in benchmarks
            if benchmark in data[language]
        }
        for language in args.languages
    }

    energies = {
        language: {
            benchmark: statistics.median(
                [
                    sum(
                        [
                            sum(e["pkg"] + e["dram"] for e in s["energy"])
                            for s in r["energy_samples"]
                        ]
                    )
                    for r in data[language][benchmark]
                ]
            )
            for benchmark in benchmarks
            if benchmark in data[language]
        }
        for language in args.languages
    }

    for language in args.languages:
        print(f"{language}:")
        for benchmark in benchmarks:
            if benchmark in data[language]:
                print(
                    f"  {benchmark}: {runtimes[language][benchmark]:.2f} {cpu_usages[language][benchmark]:.2f} {energies[language][benchmark]:.2f}"
                )

    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5)
        ax.set_facecolor("white")

        xs = []
        ys = []
        for language in args.languages:
            x = language_to_index[language]
            y = [
                sum(
                    [
                        sum(e["pkg"] + e["dram"] for e in s["energy"])
                        for s in r["energy_samples"]
                    ]
                )
                / (r["runtime_ms"] / 1e3)
                for r in data[language][benchmark]
                for benchmark in benchmarks
                if benchmark in data[language]
            ]

            xs.extend([x] * len(y))
            ys.extend(y)

        ax.scatter(xs, ys)

        # average of ys
        y_avg = statistics.mean(ys)
        ax.axhline(y_avg, color="red", linestyle="--", linewidth=1)
        print("Average: ", y_avg)
        print("Standard deviation: ", statistics.stdev(ys))

        ax.set_xticks(
            range(len(args.languages)),
            args.languages,
            rotation=45,
        )
        if args.ymax is not None:
            ax.set_ylim(bottom=0, top=args.ymax)
        else:
            ax.set_ylim(bottom=0, top=ax.get_ylim()[1] * 1.1)
        print("ymax: ", ax.get_ylim()[1])
        ax.set_xlabel("Programming Language Implementation")
        ax.set_ylabel("Average power draw (PKG + DRAM) [W]")
        fig.tight_layout()
        plt.savefig(f"fixed_time.{args.format}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        required=True,
    )
    parser.add_argument("--ymax", type=float, default=None)
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--no-title", action="store_true")
    main(parser.parse_args())
