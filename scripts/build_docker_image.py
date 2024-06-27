import argparse
import hashlib
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def file_hash(path: str) -> str:
    with open(path, "rb", buffering=0) as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def generate_input_files() -> None:
    HASHES = {
        5000000: "97197f5957a12f8a859ba7edff6d97994daa18afacd77db21fa68c6f2e447e38",
        25000000: "3fcf4f78104c8a65ef210fe1d469f4e473456c791225f2f1f9114f4986aa09fa",
        800000000: "7fb6c91ac859dd58174ad47b328da4268876f21065a6e0c6a9cfcb7153a1f4ba",
    }

    for size in HASHES.keys():
        filename = f"fasta-{size}.txt"
        path = os.path.join(ROOT, filename)
        if not os.path.isfile(path) or file_hash(path) != HASHES[size]:
            print(f"Generating {filename} ...")
            with open(path, "w") as f:
                subprocess.check_call(
                    ["node", "benchmarks/JavaScript/fasta/fasta.js", f"{size}"],
                    stdout=f,
                )
            assert file_hash(path) == HASHES[size]


def main(args: argparse.Namespace) -> None:
    if not os.geteuid() == 0:
        print("[WARNING] This script should be run as root.")

    print("Checking input files ...")
    generate_input_files()

    print("Building RAPL tool ...")
    subprocess.check_call(["rm", "-rf", os.path.join(ROOT, "scripts/RAPL/build")])
    subprocess.check_call(
        [
            "cmake",
            os.path.join(ROOT, "scripts/RAPL"),
            "-B",
            os.path.join(ROOT, "scripts/RAPL/build"),
            "-DCMAKE_BUILD_TYPE=Release",
        ],
        stdout=(subprocess.DEVNULL if not args.verbose else None),
    )
    subprocess.check_call(
        ["cmake", "--build", os.path.join(ROOT, "scripts/RAPL/build"), "--parallel"],
        stdout=(subprocess.DEVNULL if not args.verbose else None),
    )

    print("Building Docker image ...")
    subprocess.check_call(
        [
            "docker",
            "build",
            "-f",
            os.path.join(ROOT, "docker/main.Dockerfile"),
            "-t",
            "energy-languages",
            ROOT,
        ],
        stderr=(subprocess.DEVNULL if not args.verbose else None),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    main(parser.parse_args())
