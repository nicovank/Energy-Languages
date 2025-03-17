import argparse
import json
import statistics


def get_mean_and_stddev(data) -> tuple[float, float]:
    mean = statistics.mean(data)
    stddev = statistics.stdev(data)
    return mean, stddev


def main(args: argparse.Namespace) -> None:
    data = []
    with open(args.path, "r") as file:
        for line in file:
            data.append(json.loads(line))

    mean_runtime, stddev_runtime = get_mean_and_stddev([d["runtime_ms"] for d in data])
    mean_energy, stddev_energy = get_mean_and_stddev(
        [
            sum([sum(e["pkg"] for e in s["energy"]) for s in d["energy_samples"]])
            for d in data
        ]
    )
    mean_cores, stddev_cores = get_mean_and_stddev(
        [
            (d["counters"]["PERF_COUNT_SW_TASK_CLOCK"] / 1e9) / (d["runtime_ms"] / 1e3)
            for d in data
        ]
    )
    print(f"Runtime: {mean_runtime:.2f} ± {stddev_runtime:.2f} ms")
    print(f"Energy: {mean_energy:.2f} ± {stddev_energy:.2f} J")
    print(f"Cores: {mean_cores:.2f} ± {stddev_cores:.2f} cores")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="path to a JSON RAPL output file")
    main(parser.parse_args())
