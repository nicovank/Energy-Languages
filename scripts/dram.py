import argparse
import math
import statistics

import matplotlib
import matplotlib.pyplot as plt
import scipy  # type: ignore

from . import utils


def human_readable(x):
    assert math.isclose(int(x), x)
    if x < 1e3:
        return f"{int(x)}"
    if x < 1e6:
        return f"{int(x / 1e3)}k"
    if x < 1e9:
        return f"{int(x / 1e6)}M"
    return f"{int(x / 1e9)}G"


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    xs = []
    ys = []

    min_ratio = math.inf
    max_ratio = 0.0

    # Format: (llc miss rate, average cores, llc misses per second, pkg power draw, dram power draw)

    microbenchmark_points = [
        # repeat 10 { sudo ./build/benchmark_iteration -c 64 -i 1000000000 -n 2500000}
        (90.95, 60.90, 1705765000.00, 486.21, 26.45),
        (90.97, 60.84, 1704694000.00, 486.39, 26.53),
        (91.13, 61.89, 1732059000.00, 488.41, 26.83),
        (90.96, 60.90, 1707007000.00, 486.67, 26.54),
        (90.94, 60.09, 1672147000.00, 483.77, 26.36),
        (90.87, 60.95, 1706984000.00, 487.14, 26.40),
        (90.80, 58.45, 1633252000.00, 479.64, 25.77),
        (90.88, 61.02, 1707069000.00, 487.05, 26.51),
        (90.86, 60.99, 1708121000.00, 487.12, 26.39),
        (90.92, 61.08, 1710484000.00, 487.37, 26.44),
        # repeat 10 { sudo ./build/benchmark_iteration -c 64 -i 1000000000 -n 600000}
        (42.67, 60.28, 827711000.00, 474.32, 21.10),
        (42.84, 63.36, 877099000.00, 484.15, 21.56),
        (42.72, 63.41, 877215000.00, 485.79, 21.51),
        (42.84, 62.89, 868753000.00, 484.20, 21.44),
        (42.90, 52.30, 718783000.00, 457.76, 20.14),
        (43.19, 61.27, 856011000.00, 483.16, 21.48),
        (43.43, 63.42, 892971000.00, 489.41, 22.02),
        (43.42, 63.44, 891762000.00, 490.07, 22.04),
        (43.26, 63.44, 888513000.00, 489.13, 22.22),
        (42.72, 62.44, 859831000.00, 484.70, 21.32),
        # repeat 10 { sudo ./build/benchmark_iteration -c 64 -i 1000000000 -n 1200000}
        (79.92, 53.89, 1364812000.00, 464.14, 24.06),
        (80.76, 58.95, 1521799000.00, 481.88, 25.16),
        (80.24, 59.31, 1528741000.00, 483.80, 25.25),
        (79.81, 59.52, 1510057000.00, 483.93, 25.22),
        (80.13, 58.77, 1502386000.00, 482.22, 25.14),
        (80.12, 59.22, 1517082000.00, 484.12, 25.14),
        (80.56, 60.82, 1572513000.00, 488.67, 25.64),
        (80.33, 62.26, 1593738000.00, 492.43, 26.00),
        (79.70, 56.75, 1439720000.00, 476.71, 24.44),
        (80.19, 59.78, 1535966000.00, 485.38, 25.25),
        # repeat 10 { sudo ./build/benchmark_iteration -c 64 -i 1000000000 -n 1100000}
        (78.48, 61.11, 1507542000.00, 481.30, 25.69),
        (78.23, 55.52, 1383245000.00, 470.76, 24.28),
        (78.37, 61.64, 1537553000.00, 488.89, 25.63),
        (78.39, 58.81, 1480142000.00, 482.53, 25.20),
        (78.12, 59.77, 1482468000.00, 483.91, 25.25),
        (77.55, 58.49, 1434959000.00, 480.73, 24.93),
        (78.30, 59.18, 1476719000.00, 482.81, 25.12),
        (77.61, 56.72, 1396886000.00, 476.51, 24.50),
        (78.13, 58.43, 1461331000.00, 481.74, 24.93),
        (78.06, 61.13, 1523191000.00, 489.08, 25.60),
        # repeat 10 { sudo ./build/benchmark_iteration -c 64 -i 1000000000 -n 700000}
        (55.98, 59.64, 1065301000.00, 468.73, 22.70),
        (55.97, 58.40, 1050946000.00, 469.51, 22.42),
        (56.18, 59.28, 1076771000.00, 473.62, 22.72),
        (56.51, 62.62, 1143756000.00, 483.82, 23.51),
        (56.45, 62.76, 1142053000.00, 485.51, 23.47),
        (56.49, 63.20, 1155595000.00, 488.44, 23.51),
        (55.24, 54.16, 953864000.00, 462.42, 21.46),
        (56.46, 62.70, 1144949000.00, 486.92, 23.45),
        (56.45, 63.41, 1159570000.00, 489.71, 23.52),
        (56.32, 59.96, 1087020000.00, 479.58, 22.85),
        # repeat 10 { sudo ./build/benchmark_iteration -c 64 -i 1000000000 -n 400000}
        (2.46, 62.12, 45434000.00, 457.90, 13.12),
        (2.26, 63.55, 43530000.00, 466.65, 13.07),
        (2.42, 63.57, 46596000.00, 467.80, 13.18),
        (2.47, 52.91, 39126000.00, 442.40, 12.90),
        (2.38, 62.76, 44914000.00, 466.67, 12.97),
        (2.42, 63.58, 46299000.00, 469.46, 13.13),
        (2.42, 63.67, 46365000.00, 470.41, 13.15),
        (2.41, 63.56, 46144000.00, 470.90, 13.13),
        (2.47, 63.55, 47138000.00, 471.51, 13.13),
        (2.16, 63.58, 41440000.00, 471.59, 12.90),
        # repeat 10 { sudo ./build/benchmark_iteration -c 128 -i 1000000000 -n 2000000}
        (93.96, 119.40, 1764152000.00, 488.84, 27.92),
        (93.82, 120.61, 1782318000.00, 493.04, 28.04),
        (93.84, 120.36, 1790899000.00, 497.56, 28.16),
        (93.84, 119.63, 1769152000.00, 494.07, 27.89),
        (94.07, 120.72, 1795014000.00, 498.85, 28.25),
        (93.88, 120.83, 1785964000.00, 496.78, 28.15),
        (93.94, 121.09, 1792383000.00, 497.52, 28.16),
        (93.98, 120.75, 1787950000.00, 497.16, 28.18),
        (93.78, 119.45, 1781402000.00, 498.16, 28.41),
        (93.90, 119.34, 1760668000.00, 495.13, 27.87),
        # repeat 10 { sudo ./build/benchmark_iteration -c 128 -i 1000000000 -n 300000}
        (43.64, 127.16, 906644000.00, 490.51, 21.97),
        (43.61, 127.26, 906134000.00, 491.81, 22.10),
        (43.69, 127.31, 907831000.00, 493.32, 22.10),
        (43.62, 127.36, 906647000.00, 494.79, 21.78),
        (43.61, 127.24, 905722000.00, 494.19, 21.94),
        (43.63, 127.32, 906196000.00, 493.38, 22.34),
        (43.69, 127.27, 907354000.00, 494.23, 22.38),
        (43.67, 127.24, 907046000.00, 494.77, 22.12),
        (43.64, 127.29, 906280000.00, 494.03, 22.34),
        (43.63, 127.23, 906150000.00, 494.92, 22.10),
        # repeat 10 { sudo ./build/benchmark_iteration -c 128 -i 1000000000 -n 200000}
        (2.41, 127.17, 46257000.00, 469.51, 13.16),
        (2.53, 126.70, 48767000.00, 473.90, 13.39),
        (2.58, 127.43, 49895000.00, 475.83, 13.36),
        (2.53, 127.41, 48833000.00, 476.58, 13.35),
        (2.50, 127.56, 48170000.00, 477.25, 13.25),
        (2.44, 127.48, 47068000.00, 477.84, 13.22),
        (2.40, 127.53, 46428000.00, 478.44, 13.09),
        (2.58, 127.58, 49960000.00, 478.57, 13.19),
        (2.58, 126.45, 49581000.00, 478.55, 13.30),
        (2.72, 125.72, 52190000.00, 479.09, 13.53),
        # repeat 10 { sudo ./build/benchmark_iteration -c 128 -i 1000000000 -n 250000}
        (22.20, 125.83, 450728000.00, 477.60, 18.18),
        (22.24, 127.39, 457821000.00, 483.48, 18.35),
        (22.25, 127.47, 458783000.00, 485.59, 18.39),
        (22.27, 127.47, 458546000.00, 486.84, 18.40),
        (22.16, 127.39, 456455000.00, 487.25, 18.48),
        (22.15, 127.42, 456106000.00, 487.99, 18.30),
        (22.23, 127.36, 458227000.00, 488.36, 18.32),
        (22.22, 127.40, 457563000.00, 488.68, 18.23),
        (22.14, 127.38, 456044000.00, 488.92, 18.22),
        (22.12, 127.36, 455988000.00, 488.89, 18.32),
        # repeat 10 { sudo ./build/benchmark_iteration -c 128 -i 1000000000 -n 275000}
        (34.24, 126.63, 704903000.00, 483.35, 20.46),
        (34.17, 127.32, 708477000.00, 487.89, 20.56),
        (34.17, 127.38, 708862000.00, 488.82, 20.67),
        (34.22, 127.35, 709729000.00, 488.60, 21.03),
        (34.23, 127.41, 710195000.00, 490.07, 20.72),
        (34.19, 127.39, 709103000.00, 490.86, 20.74),
        (34.23, 127.35, 709331000.00, 491.67, 20.71),
        (34.27, 127.33, 710692000.00, 490.92, 20.91),
        (34.22, 127.00, 708293000.00, 492.64, 20.69),
        (34.27, 127.30, 710944000.00, 493.49, 20.65),
        # repeat 10 { sudo ./build/benchmark_iteration -c 128 -i 1000000000 -n 400000}
        (65.58, 125.94, 1350407000.00, 488.99, 24.94),
        (65.60, 127.16, 1365555000.00, 492.89, 25.44),
        (65.58, 127.04, 1363924000.00, 494.48, 25.16),
        (65.60, 127.08, 1365120000.00, 495.87, 25.34),
        (65.61, 126.42, 1358781000.00, 495.87, 25.32),
        (65.60, 127.14, 1364652000.00, 498.18, 25.00),
        (65.53, 127.09, 1363071000.00, 497.92, 25.17),
        (65.57, 127.15, 1365405000.00, 498.47, 25.40),
        (65.61, 127.18, 1365993000.00, 498.00, 25.48),
        (65.61, 127.11, 1365129000.00, 499.78, 25.03),
    ]

    for language in args.languages:
        for benchmark in data[language].keys():
            for r in data[language][benchmark]:
                ratio = sum(
                    [sum(e["dram"] for e in s["energy"]) for s in r["energy_samples"]]
                ) / sum(
                    [sum(e["pkg"] for e in s["energy"]) for s in r["energy_samples"]]
                )
                min_ratio = min(min_ratio, ratio)
                max_ratio = max(max_ratio, ratio)
            x = statistics.median(
                [
                    r["counters"]["PERF_COUNT_HW_CACHE_MISSES"]
                    / (1e-3 * r["runtime_ms"])
                    for r in data[language][benchmark]
                ]
            )
            miss_rate = statistics.median(
                [
                    100
                    * r["counters"]["PERF_COUNT_HW_CACHE_MISSES"]
                    / r["counters"]["PERF_COUNT_HW_CACHE_REFERENCES"]
                    for r in data[language][benchmark]
                ]
            )
            print(
                language,
                benchmark,
                x,
                f"{miss_rate:.2f}",
                r["counters"]["PERF_COUNT_HW_CACHE_REFERENCES"],
                sep=";",
            )
            if x > args.xmax:
                continue
            xs.append(x)
            ys.append(
                statistics.median(
                    [
                        sum(
                            [
                                sum(e["dram"] for e in s["energy"])
                                for s in r["energy_samples"]
                            ]
                        )
                        / (1e-3 * r["runtime_ms"])
                        for r in data[language][benchmark]
                    ]
                )
            )

    print(
        f"% of DRAM energy over CPU energy: {min_ratio * 100:.2f}% - {max_ratio * 100:.2f}%"
    )

    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        if args.half_size:
            fig.set_size_inches(4, 3)
        else:
            fig.set_size_inches(8, 5)
        ax.set_facecolor("white")

        ax.scatter(xs, ys, s=(5 if args.half_size else 10))

        slope, intercept, rvalue, _, _ = scipy.stats.linregress(xs, ys)
        print(f"slope: {slope:.2e}, intercept: {intercept:.2f}")
        ax.plot(
            [min(xs), max(xs)],
            [intercept + slope * min(xs), intercept + slope * max(xs)],
            color="red",
            linewidth=1,
        )
        print(f"R^2: {rvalue ** 2:.2f}")

        ax.scatter(
            [x[2] for x in microbenchmark_points],
            [x[4] for x in microbenchmark_points],
            s=20,
            marker="+",
            color="black",
        )

        ax.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: human_readable(x))
        )

        ax.set_xlabel(
            "LLC misses per second", fontsize=("medium" if args.half_size else "large")
        )
        ax.set_ylabel(
            "Average power draw (DRAM) [W]",
            fontsize=("medium" if args.half_size else "large"),
        )
        ax.set_ylim(bottom=0)
        if args.ymax:
            ax.set_ylim(top=args.ymax)
        fig.tight_layout()
        plt.savefig(f"dram.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        required=True,
    )
    parser.add_argument("--half-size", default=False, action="store_true")
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--xmax", type=float, default=math.inf)
    parser.add_argument("--ymax", type=float, default=None)
    main(parser.parse_args())
