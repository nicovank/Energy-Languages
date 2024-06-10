import argparse
import statistics
from typing import Dict

import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
import scipy  # type: ignore

from . import utils


def main(args: argparse.Namespace) -> None:
    data, benchmarks = utils.parse(args.data_root, args.languages)

    table = Table(title=f"Average CPU usage for all (language, benchmark) pairs")
    table.add_column("Benchmark")
    for language in args.languages:
        table.add_column(f"{language}")

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

    for benchmark in benchmarks:
        row = [benchmark]
        for language in args.languages:
            if benchmark in cpu_usages[language]:
                row.append(f"{cpu_usages[language][benchmark]:.2f}")
            else:
                row.append("")
        table.add_row(*row)

    console = Console()
    console.print(table)

    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    with plt.style.context("bmh"):
        energy_over_time_ratio = {
            language: {
                benchmark: statistics.geometric_mean(
                    [
                        sum([s["energy"]["pkg"] for s in r["energy_samples"]])
                        / (1e-3 * r["runtime_ms"])
                        for r in data[language][benchmark]
                    ]
                )
                for benchmark in benchmarks
                if benchmark in data[language]
            }
            for language in args.languages
        }

        fig, ax = plt.subplots()
        if not args.no_title:
            ax.set_title(
                f"Power consumption as a function of CPU usage for all (language, benchmark) pairs"
            )
        ax.set_xlabel("CPU usage")
        ax.set_ylabel("Average power consumption [W]")

        all_xs = []
        all_ys = []
        for language in args.languages:
            x = []
            y = []
            for benchmark in benchmarks:
                if benchmark in energy_over_time_ratio[language]:
                    x.append(cpu_usages[language][benchmark])
                    y.append(energy_over_time_ratio[language][benchmark])
            all_xs.extend(x)
            all_ys.extend(y)
            # ax.scatter(
            #     x,
            #     y,
            #     marker=".",
            #     s=50,
            #     label=language.replace("#", "\\#"),
            # )
        ax.scatter(all_xs, all_ys, marker=".", s=50)

        regression = scipy.stats.linregress(all_xs, all_ys)
        print("Regression slope :", regression.slope)
        print("Regression rvalue:", regression.rvalue)
        print("Regression stderr:", regression.stderr)

        # ax.legend()
        fig.tight_layout()
        plt.savefig(f"cpu_usage.{args.format}", format=args.format)


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
