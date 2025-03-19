import argparse
import datetime
import os
import subprocess

DACAPO_JAR = "dacapo-23.11-MR2-chopin.jar"
RAPL_PATH = "/root/rapl"
DATA_PATH = "/root/data"
PORTABILITY = {
    "cassandra": ["-Djava.security.manager=allow"],
    "h2o": ["-Dsys.ai.h2o.debug.allowJavaVersions=21"],
}


def get_benchmarks() -> list[str]:
    return subprocess.check_output(
        ["java", "-jar", DACAPO_JAR, "-l"], text=True
    ).split()


def main(args: argparse.Namespace) -> None:
    benchmarks = get_benchmarks()
    for i in range(args.copies):
        for benchmark in benchmarks:
            if args.benchmarks and benchmark not in args.benchmarks:
                continue
            print(
                f"Running {benchmark} #{i} [{datetime.datetime.now().strftime('%H:%M:%S')}]..."
            )
            subprocess.run(
                [
                    RAPL_PATH,
                    "--json",
                    os.path.join(DATA_PATH, f"{benchmark}.json"),
                    "java",
                    *PORTABILITY.get(benchmark, []),
                    "-jar",
                    DACAPO_JAR,
                    "-n",
                    str(args.iterations),
                    benchmark,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--copies", required=True, type=int, help="number of copies")
    parser.add_argument(
        "--iterations", required=True, type=int, help="number of iterations per copy"
    )
    parser.add_argument(
        "--benchmarks",
        metavar="NAME",
        nargs="+",
        help="Specific list of benchmarks to run",
    )
    main(parser.parse_args())
