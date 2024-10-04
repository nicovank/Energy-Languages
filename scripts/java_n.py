import argparse
import collections
import json
import os

from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np


def main(args: argparse.Namespace) -> None:
    java_n_experiments = [
        e for e in os.listdir(args.data_root) if e.startswith(f"{args.language}-")
    ]
    data = collections.defaultdict(list)
    for experiment in java_n_experiments:
        n = int(experiment.split("-")[1])
        path = os.path.join(args.data_root, experiment, f"{args.benchmark}.json")
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            for line in f:
                data[n].append(json.loads(line))

    plt.rcParams["font.family"] = args.font
    with plt.style.context("bmh"):
        fig, ax = plt.subplots()
        ax.set_facecolor("white")
        fig.set_size_inches(4, 3)

        x = np.sort(np.array(list(data.keys())))
        runtime = [[r["runtime_ms"] for r in data[n]] for n in x]

        y = np.median(runtime, axis=1) / x
        sigma = np.std(runtime, axis=1) / x
        print(x, y, sigma)

        ax.errorbar(
            x,
            y,
            sigma,
            linestyle="",
            elinewidth=0.5,
            capsize=2,
            capthick=0.5,
        )
        ax.scatter(x, y, s=20)

        ax.set_ylabel("Time per iteration [ms]")
        ax.set_xlabel("Number of iterations")
        ax.set_axisbelow(True)
        ax.set_ylim(0, ax.get_ylim()[1])
        ax.set_xticks([0, 3, 6, 9, 12, 15])

        if args.ymax is not None:
            ax.set_ylim(0, args.ymax)
        print("ymax:", ax.get_ylim()[1])

        fig.tight_layout()
        plt.savefig(f"java-n.{args.benchmark}.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument("--benchmark", type=str, required=True)
    parser.add_argument("--language", type=str, default="Java")
    parser.add_argument("--ymax", type=float, default=None)
    parser.add_argument("--font", type=str, default="Linux Libertine O")
    parser.add_argument("--format", type=str, default="png")
    main(parser.parse_args())
