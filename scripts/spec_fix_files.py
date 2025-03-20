import argparse
import json
from typing import Any

def merge_entries(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    c = {}
    c["runtime_ms"] = a["runtime_ms"] + b["runtime_ms"]
    assert a["counters"].keys() == b["counters"].keys()
    c["counters"] = {}
    for key in a["counters"].keys():
        c["counters"][key] = a["counters"][key] + b["counters"][key]
    c["energy_samples"] = a["energy_samples"] + b["energy_samples"]
    return c

def main(args: argparse.Namespace) -> None:
    for filename in args.filenames:
        with open(filename, "r") as file:
            lines = file.readlines()
        assert len(lines) % args.iterations == 0
        if len(lines) == args.iterations:
            print(f"{filename}: no need to consolidate")
            continue
        print(f"{filename}: consolidating {len(lines)} lines into {args.iterations} lines")
        data = [json.loads(line) for line in lines]
        consolidated_data  = []
        for i in range(args.iterations):
            entry = data[i * (len(lines) // args.iterations)]
            for j in range(1, len(lines) // args.iterations):
                entry = merge_entries(entry, data[i * (len(lines) // args.iterations) + j])
            consolidated_data.append(entry)
        with open(filename, "w") as file:
            for entry in consolidated_data:
                file.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, required=True, help="number of iterations performed")
    parser.add_argument("filenames", nargs="+", help="files to process")
    main(parser.parse_args())
