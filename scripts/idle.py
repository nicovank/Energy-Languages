import argparse
from typing import Any

import numpy as np
import pandas


def main(args: argparse.Namespace) -> None:
    data = pandas.read_csv(
        args.path,
        delimiter=",",
        names=["timestamp", "energy"],
        dtype={"timestamp": np.int64, "energy": np.float64},
    )

    def get_values(id: str) -> np.ndarray[Any, Any]:
        series = data.get(id)
        assert series is not None
        return series.values.astype(np.float64)

    timestamp = get_values("timestamp")
    energy = get_values("energy")

    timestamp /= 1e9

    assert all(timestamp[i] <= timestamp[i + 1] for i in range(len(timestamp) - 1))

    data = energy[1:] / np.diff(timestamp)
    print(f"Geometric mean: {np.exp(np.log(data).mean()):.2f} J")
    print(f"Sigma: {np.std(data):.2f} J")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    main(parser.parse_args())
