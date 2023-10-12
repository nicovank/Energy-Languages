import argparse
import collections
import json
import os

from cycler import cycler
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def main(args):
    experiments_root = os.path.join(args.data_root, "experiments")
    java_n_experiments = [
        e for e in os.listdir(experiments_root) if e.startswith("Java-")
    ]
    data = collections.defaultdict(list)
    for experiment in java_n_experiments:
        n = int(experiment.split("-")[1])
        path = os.path.join(experiments_root, experiment, f"{args.benchmark}.json")
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            for line in f:
                data[n].append(json.loads(line))

    plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
    with plt.style.context("bmh"):
        plt.rc(
            "axes",
            prop_cycle=cycler(
                color=[plt.rcParams["axes.prop_cycle"].by_key()["color"][0]]
            ),
        )
        fig, ax = plt.subplots()
        fig.set_size_inches(7, 5)

        for n in sorted(data.keys()):
            x = np.sort(np.array(list(data.keys())))
            runtime = [[r["runtime"] for r in data[n]] for n in x]
            energy = [[r["energy"]["pkg"] for r in data[n]] for n in x]

            y = np.median(runtime, axis=1) / x
            sigma = np.std(runtime, axis=1) / x

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

        if not args.no_title:
            ax.set_title(f"Runtime per iteration for {args.benchmark} (Java)")
        ax.set_ylabel("Time [ms]")
        ax.set_xlabel("Number of iterations")
        ax.set_axisbelow(True)
        ax.set_ylim(0, ax.get_ylim()[1])

        fig.tight_layout()
        plt.savefig(f"java-n.{args.benchmark}.{args.format}", format=args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument("--benchmark", type=str, required=True)
    parser.add_argument("--format", type=str, default="png")
    parser.add_argument("--no-title", action="store_true")
    main(parser.parse_args())
