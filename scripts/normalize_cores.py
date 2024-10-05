import argparse
import statistics

import matplotlib.pyplot as plt
import numpy as np
import scipy  # type: ignore

from . import utils


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    xs = []
    ys = []

    for language in args.languages:
        for benchmark in data[language].keys():
            xs.append(
                statistics.median(
                    [
                        (r["counters"]["PERF_COUNT_SW_TASK_CLOCK"] / 1e9)
                        / (r["runtime_ms"] / 1e3)
                        for r in data[language][benchmark]
                    ]
                )
            )

            ys.append(
                statistics.median(
                    [
                        sum(
                            [
                                sum(e["pkg"] for e in s["energy"])
                                for s in r["energy_samples"]
                            ]
                        )
                        / (1e-3 * r["runtime_ms"])
                        for r in data[language][benchmark]
                    ]
                )
            )

            print(f"{language} {benchmark}, {xs[-1]:.1f}, {int(ys[-1])}")

    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        if args.half_size:
            fig.set_size_inches(4, 3)
        else:
            fig.set_size_inches(8, 5)
        ax.set_facecolor("white")

        ax.scatter(xs, ys, s=(5 if args.half_size else 10))

        def linear_fit(x, a, b):
            return a * np.array(x) + b

        def log_fit(x, a, b):
            return a * np.log(x) + b

        x_fit = np.linspace(min(xs), max(xs), 100)

        if args.fit == "linear":
            c1, _ = scipy.optimize.curve_fit(linear_fit, xs, ys)
            y_fit = linear_fit(x_fit, *c1)
            residuals = ys - linear_fit(xs, *c1)
            print(f"{c1[0]:.2f} * x + {c1[1]:.2f}")
        elif args.fit == "log":
            c1, _ = scipy.optimize.curve_fit(log_fit, xs, ys)
            y_fit = log_fit(x_fit, *c1)
            residuals = ys - log_fit(xs, *c1)
            print(f"{c1[0]:.2f} * ln(x) + {c1[1]:.2f}")

        ax.plot(x_fit, y_fit, color="red", linewidth=1)

        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((ys - np.mean(ys)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        print(f"r2: {r2}")

        print("ymax:", ax.get_ylim()[1])

        ax.set_xlabel(
            "Average number of active cores",
            fontsize=("medium" if args.half_size else "large"),
        )
        ax.set_ylabel(
            "Average power draw (PKG) [W]",
            fontsize=("medium" if args.half_size else "large"),
        )
        ax.set_ylim(bottom=0)
        fig.tight_layout()
        plt.savefig(f"normalize_cores.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        required=True,
    )
    parser.add_argument("--fit", type=str, choices=["linear", "log"], default="log")
    parser.add_argument("--half-size", default=False, action="store_true")
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
