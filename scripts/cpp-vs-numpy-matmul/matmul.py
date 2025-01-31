import argparse

import numpy as np


def main(args: argparse.Namespace):
    A = np.random.rand(args.n, args.n)
    B = np.random.rand(args.n, args.n)

    for _ in range(args.i):
        C = np.matmul(A, B)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="size of matrices")
    parser.add_argument("i", type=int, help="number of iterations")
    args = parser.parse_args()
    main(args)
