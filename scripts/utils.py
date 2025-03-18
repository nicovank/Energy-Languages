import collections
from enum import Enum
import json
import os
from typing import Any, Dict, List, Tuple


def parse(
    data_root: str, languages: List[str]
) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    data: Dict[str, Dict[str, Any]] = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )
    for language in languages:
        LANGUAGES_ROOT = os.path.join(data_root, language)
        if not os.path.isdir(LANGUAGES_ROOT):
            languages.remove(language)
            print(f"Warning: {LANGUAGES_ROOT} does not exist, skipping")
            continue
        for benchmark in os.listdir(LANGUAGES_ROOT):
            path = os.path.join(LANGUAGES_ROOT, benchmark)
            assert os.path.isfile(path) and path.endswith(".json")
            benchmark = benchmark[:-5]
            with open(path, "r") as file:
                for line in file:
                    line = json.loads(line)
                    data[language][benchmark].append(line)

    benchmarks: List[str] = sorted(list({b for l in data.values() for b in l.keys()}))
    return data, benchmarks


def timeval_to_seconds(tv: Dict[str, float]) -> float:
    return tv["tv_sec"] + 1e-6 * tv["tv_usec"]


def cpu_usage(user_cpu_time: float, kernel_cpu_time: float, runtime: float) -> float:
    return (user_cpu_time + kernel_cpu_time) / runtime


class BenchmarkSuite(Enum):
    CLBG = 1
    SPECINT = 2
    DACAPO = 3


def suites() -> list[BenchmarkSuite]:
    return [BenchmarkSuite.CLBG, BenchmarkSuite.SPECINT, BenchmarkSuite.DACAPO]


def benchmarks_by_suite(suite: BenchmarkSuite) -> list[str]:
    return {
        BenchmarkSuite.CLBG: [
            "binary-trees",
            "binary-trees",
            "fannkuch-redux",
            "fasta",
            "k-nucleotide",
            "mandelbrot",
            "n-body",
            "pidigits",
            "regex-redux",
            "reverse-complement",
            "spectral-norm",
        ],
        BenchmarkSuite.SPECINT: [
            "600.perlbench_s",
            "602.gcc_s",
            "605.mcf_s",
            "620.omnetpp_s",
            "623.xalancbmk_s",
            "625.x264_s",
            "631.deepsjeng_s",
            "641.leela_s",
            "648.exchange2_s",
            "657.xz_s",
            "998.specrand_is",
        ],
        BenchmarkSuite.DACAPO: [
            "avrora",
            "batik",
            "biojava",
            "cassandra",
            "eclipse",
            "fop",
            "graphchi",
            "h2",
            "jme",
            "jython",
            "kafka",
            "luindex",
            "lusearch",
            "pmd",
            "spring",
            "sunflow",
            "tomcat",
            "tradebeans",
            "tradesoap",
            "xalan",
            "zxing",
        ],
    }[suite]


def suite_by_benchmark(benchmark: str) -> BenchmarkSuite:
    if benchmark in benchmarks_by_suite(BenchmarkSuite.CLBG):
        return BenchmarkSuite.CLBG
    if benchmark in benchmarks_by_suite(BenchmarkSuite.SPECINT):
        return BenchmarkSuite.SPECINT
    if benchmark in benchmarks_by_suite(BenchmarkSuite.DACAPO):
        return BenchmarkSuite.DACAPO
    raise ValueError(f"Unknown benchmark {benchmark}")


def pretty_suite_name(suite: BenchmarkSuite) -> str:
    return {
        BenchmarkSuite.CLBG: "CLBG",
        BenchmarkSuite.SPECINT: "SPECint",
        BenchmarkSuite.DACAPO: "DaCapo",
    }[suite]
