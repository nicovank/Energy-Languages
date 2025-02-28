import argparse
import re
import json

import docker


def convert_to_ns(value, unit):
    conversion_factors = {"s": 1e9, "ms": 1e6, "us": 1e3, "ns": 1}
    return float(value) * conversion_factors[unit]


def parse_benchmark_results(text):
    pattern = re.compile(r"(\w+): Mean \+- std dev: ([\d.]+) (\w+) \+- ([\d.]+) (\w+)")
    results = []

    for match in pattern.finditer(text):
        name, mean, unit1, sigma, unit2 = match.groups()
        print(f"{name}: {mean} {unit1} +- {sigma} {unit2}")
        mean_ns = convert_to_ns(mean, unit1)
        sigma_ns = convert_to_ns(sigma, unit1)
        results.append({"name": name, "mean_ns": mean_ns, "sigma_ns": sigma_ns})

    return results


def main(args: argparse.Namespace) -> None:
    client = docker.from_env()

    for version in args.versions:
        print(f"Pulling Python v{version}...")
        client.images.pull(f"python:{version}")

        print("Running pyperformance...")
        command = "pip install pyperformance && pyperformance run -r"
        if args.benchmarks:
            command += f" -b '{args.benchmarks}'"
        stdout = client.containers.run(
            f"python:{version}",
            entrypoint=["/usr/bin/bash", "-c", command],
            remove=True,
            tty=True,
        )
        with open(f"pyperformance-{version}.json", "w") as f:
            json.dump(parse_benchmark_results(stdout.decode("UTF-8")), f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--versions",
        type=str,
        nargs="+",
        default=["3.9", "3.10", "3.11", "3.12", "3.13"],
        metavar="VERSION",
        help="list of Python versions to test",
    )
    parser.add_argument(
        "--benchmarks",
        "-b",
        type=str,
        default=None,
        help="comma-separated list of benchmarks, passed as-is to pyperformance",
    )
    main(parser.parse_args())
