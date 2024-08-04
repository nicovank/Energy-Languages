import argparse
import statistics

import matplotlib.pyplot as plt

from . import utils


def main(args: argparse.Namespace) -> None:
    data, _ = utils.parse(args.data_root, args.languages)

    shortcut = {
        "C": ["C", "clang"],
        "C++": ["C++", "clang++"],
        "Rust": ["Rust", "Rust"],
        "C#": ["C#", ".NET"],
        "Java": ["Java", "OpenJDK"],
        "JavaScript": ["JavaScript", "Node.js"],
        "TypeScript": ["TypeScript", "Node.js"],
        "Lua": ["Lua", "Lua"],
        "LuaJIT": ["Lua", "LuaJIT"],
        "PHP": ["PHP", "PHP"],
        "Go": ["Go", "Go"],
        "Python": ["Python", "CPython"],
        "PyPy": ["Python", "PyPy"],
    }

    print("pl,plimp,appimp,ncores,memactivity,time,power,energy")

    for language in args.languages:
        for benchmark in data[language].keys():
            for r in data[language][benchmark]:
                pl = shortcut[language][0]

                plimp = shortcut[language][1]

                ncores = (r["counters"]["PERF_COUNT_SW_TASK_CLOCK"] / 1e9) / (
                    r["runtime_ms"] / 1e3
                )

                memactivity = r["counters"]["PERF_COUNT_HW_CACHE_MISSES"] / (
                    1e-3 * r["runtime_ms"]
                )

                time = 1e-3 * r["runtime_ms"]

                energy = sum(
                    [
                        s["energy"]["pkg"] + s["energy"]["dram"]
                        for s in r["energy_samples"]
                    ]
                )

                power = energy / time

                print(
                    f"{pl},{plimp},{benchmark},{ncores},{memactivity},{time},{power},{energy}"
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        required=True,
    )
    main(parser.parse_args())
