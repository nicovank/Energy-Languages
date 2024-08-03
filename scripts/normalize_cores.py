import argparse
import statistics

import matplotlib
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
                            sum([s["energy"]["pkg"] for s in r["energy_samples"]])
                            / (1e-3 * r["runtime_ms"])
                            for r in data[language][benchmark]
                        ]
                    )
                )

    plt.rcParams["font.family"] = args.font
    plt.gcf().set_size_inches(8, 5)
    with plt.style.context("bmh"):
        plt.scatter(xs, ys, s=10)

        def log_fit(x, a, b):
            return a * np.log(x) + b

        c, _ = scipy.optimize.curve_fit(log_fit, xs, ys)
        x_fit = np.linspace(0, max(xs), 100)
        y_power = log_fit(x_fit, *c)
        print(f"{c[0]:.2f} * ln(x) + {c[1]:.2f}")
        plt.plot(x_fit, y_power, color='red', linewidth=1)

        # Calculate r2
        residuals = ys - log_fit(xs, *c)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((ys - np.mean(ys)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        print(f"r2: {r2}")

        plt.xlabel("Average number of cores used")
        plt.ylabel("Average power draw [W]")
        plt.ylim(bottom=0)
        plt.tight_layout()
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
    parser.add_argument("--font", type=str, default="Linux Libertine")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
