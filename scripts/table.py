import argparse
import statistics
from typing import Any, Dict, Optional

from rich.console import Console
from rich.table import Table
from rich.text import Text

from . import utils


def table(
    title: str,
    args: argparse.Namespace,
    data: Dict[str, Dict[str, Any]],
    means: Dict[str, Dict[str, float]],
    baseline: Optional[str],
) -> Table:
    table = Table(title=title)
    table.add_column("Benchmark")
    for language in args.languages:
        table.add_column(
            f"{language} / {baseline}"
            if baseline and language != baseline
            else language
        )

    benchmarks = sorted(list({b for l in data.values() for b in l.keys()}))
    missing_benchmarks = []
    for benchmark in benchmarks:
        if baseline and benchmark not in data[baseline]:
            missing_benchmarks.append(benchmark)
            continue

        entries = []
        for language in args.languages:
            if benchmark not in data[language]:
                entries.append("")
            elif language == baseline:
                entries.append(f"{means[language][benchmark]:.2f}")
            else:
                entry = (
                    (means[language][benchmark] / means[baseline][benchmark])
                    if baseline
                    else means[language][benchmark]
                )
                entries.append(f"{entry:.2f}")
        table.add_row(*(benchmark, *entries))

    if baseline:
        for benchmark in missing_benchmarks:
            text = Text(benchmark)
            text.stylize("strike")
            table.add_row(text)

        per_language_normalized_means = {
            language: statistics.geometric_mean(
                [
                    means[language][b] / means[baseline][b]
                    for b in benchmarks
                    if b in means[language] and b in means[baseline]
                ]
            )
            for language in args.languages
        }

        table.add_row()
        table.add_row(
            "Geometric Mean",
            *[f"{per_language_normalized_means[l]:.2f}" for l in args.languages],
        )

    return table


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    Console().print(
        table(
            "Runtime",
            args,
            data,
            {
                language: {
                    benchmark: statistics.geometric_mean(
                        [e["runtime_ms"] for e in subdata]
                    )
                    for benchmark, subdata in data[language].items()
                }
                for language in args.languages
            },
            args.baseline,
        )
    )

    Console().print(
        table(
            "Energy consumption",
            args,
            data,
            {
                language: {
                    benchmark: statistics.geometric_mean(
                        [
                            sum([s["energy"]["pkg"] for s in e["energy_samples"]])
                            for e in subdata
                        ]
                    )
                    for benchmark, subdata in data[language].items()
                }
                for language in args.languages
            },
            args.baseline,
        )
    )


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
    parser.add_argument("--baseline", type=str, default="C")
    main(parser.parse_args())
