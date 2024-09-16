import argparse
import statistics

import matplotlib.pyplot as plt

from . import utils


def main(args: argparse.Namespace) -> None:
    data, benchmarks = utils.parse(args.data_root, args.languages)

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
        for language in args.languages:
            x = language_to_index[language]
            y = [
                statistics.median(
                    [
                        sum(
                            [
                                sum(e["pkg"] + e["dram"] for e in s["energy"])
                                for s in r["energy_samples"]
                            ]
                        ) / (r["runtime_ms"] / 1e3)
                        for r in data[language][benchmark]
                    ]
                )
                for benchmark in benchmarks
                if benchmark in data[language]
            ]

            plt.scatter([x] * len(y), y, label=language)

        plt.xticks(
            range(len(args.languages)),
            [pl.replace("#", "\\#") for pl in args.languages],
            rotation=45,
        )
        plt.ylim(bottom=0)
        plt.xlabel("Language")
        plt.ylabel("Energy [J]")
        plt.tight_layout()
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
    parser.add_argument("--font", type=str, default="Linux Libertine")
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--no-title", action="store_true")
    main(parser.parse_args())
