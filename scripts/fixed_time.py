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
            * statistics.geometric_mean(
                [r["runtime_ms"] for r in data[language][benchmark]]
            )
            for benchmark in benchmarks
            if benchmark in data[language]
        }
        for language in args.languages
    }

    cpu_usages = {
        language: {
            benchmark: statistics.geometric_mean(
                [
                    utils.cpu_usage(
                        utils.timeval_to_seconds(r["rusage"]["ru_utime"]),
                        utils.timeval_to_seconds(r["rusage"]["ru_stime"]),
                        1e-3 * r["runtime_ms"],
                    )
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
            benchmark: statistics.geometric_mean(
                [
                    sum([s["energy"]["pkg"] for s in r["energy_samples"]])
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

    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    for language in args.languages:
        x = language_to_index[language]
        y = [
            sum([s["energy"]["pkg"] for s in r["energy_samples"]])
            # sum([s["energy"]["dram"] for s in r["energy_samples"]])
            for benchmark in benchmarks
            if benchmark in data[language]
            for r in data[language][benchmark]
            # if utils.cpu_usage(
            #     utils.timeval_to_seconds(r["rusage"]["ru_utime"]),
            #     utils.timeval_to_seconds(r["rusage"]["ru_stime"]),
            #     1e-3 * r["runtime_ms"],
            # )
            # < 1.2
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
    plt.savefig(f"energy.{args.format}")


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
        ],
    )
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--no-title", action="store_true")
    main(parser.parse_args())
