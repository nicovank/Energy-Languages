import argparse
import collections
import json
import statistics


def main(args: argparse.Namespace) -> None:
    with open(args.path) as f:
        data = json.load(f)

    keys = list(data["energy_samples"][0]["energy"].keys())
    energy = collections.defaultdict(list)
    duration = []
    for sample in data["energy_samples"]:
        for entry in keys:
            energy[entry].append(sample["energy"][entry])
        duration.append(sample["duration_ms"] / 1e3)

    if "pkg" in keys and "dram" in keys:
        keys.append("pkg + dram")
        energy["pkg + dram"] = [
            pkg + dram for pkg, dram in zip(energy["pkg"], energy["dram"])
        ]

    for entry in keys:
        print(
            "{} [J/s]: {:.2f} ± {:.2f}".format(
                entry,
                statistics.mean(
                    [e / d for e, d in zip(energy[entry], duration)]
                ),
                statistics.stdev(
                    [e / d for e, d in zip(energy[entry], duration)]
                ),
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    main(parser.parse_args())
