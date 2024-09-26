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

    plt.rcParams["font.family"] = args.font
    plt.gcf().set_size_inches(8, 5)
    with plt.style.context("bmh"):
        plt.scatter(xs, ys, s=10)

        def log_fit(x, a, b):
            return a * np.log(x) + b

        def cubic_fit(x, a, b, c, d):
            # Use np.
            # return a * x**3 + b * x**2 + c * x + d
            # Numpy version
            return np.polyval([a, b, c, d], x)

        c1, _ = scipy.optimize.curve_fit(log_fit, xs, ys)
        x_fit = np.linspace(min(xs), max(xs), 100)
        y_power = log_fit(x_fit, *c1)
        print(f"{c1[0]:.2f} * ln(x) + {c1[1]:.2f}")
        plt.plot(x_fit, y_power, color="red", linewidth=1)

        # c2, _ = scipy.optimize.curve_fit(cubic_fit, xs, ys)
        # x_fit = np.linspace(0, max(xs), 100)
        # y_cubic = cubic_fit(x_fit, *c2)
        # print(f"{c2[0]:.2f} * x^3 + {c2[1]:.2f} * x^2 + {c2[2]:.2f} * x + {c2[3]:.2f}")
        # plt.plot(x_fit, y_cubic, color="green", linewidth=1)

        residuals = ys - log_fit(xs, *c1)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((ys - np.mean(ys)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        print(f"r2: {r2}")

        # residuals = ys - cubic_fit(xs, *c2)
        # ss_res = np.sum(residuals**2)
        # ss_tot = np.sum((ys - np.mean(ys)) ** 2)
        # r2 = 1 - (ss_res / ss_tot)
        # print(f"r2: {r2}")

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
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
