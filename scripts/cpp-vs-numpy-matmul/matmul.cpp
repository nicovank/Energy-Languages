#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

#include <benchmark/benchmark.h>

template <typename T> using Matrix = std::vector<std::vector<T>>;

Matrix<double> generate_random_matrix(int n) {
  std::mt19937_64 generator(std::random_device{}());
  std::normal_distribution<double> distribution(0.0, 1.0);
  Matrix<double> matrix(n, std::vector<double>(n));
  for (std::size_t i = 0; i < n; i++) {
    for (std::size_t j = 0; j < n; j++) {
      matrix[i][j] = distribution(generator);
    }
  }

  return matrix;
}

template <typename T> Matrix<T> add(const Matrix<T> &A, const Matrix<T> &B) {
  const std::size_t n = A.size();
  Matrix<T> C(n, std::vector<double>(n));
  for (std::size_t i = 0; i < n; i++) {
    for (std::size_t j = 0; j < n; j++) {
      C[i][j] = A[i][j] + B[i][j];
    }
  }
  return C;
}

template <typename T>
Matrix<T> subtract(const Matrix<T> &A, const Matrix<T> &B) {
  const std::size_t n = A.size();
  Matrix<T> C(n, std::vector<double>(n));
  for (std::size_t i = 0; i < n; i++) {
    for (std::size_t j = 0; j < n; j++) {
      C[i][j] = A[i][j] - B[i][j];
    }
  }
  return C;
}

template <typename T>
Matrix<T> fast_multiply(const Matrix<T> &A, const Matrix<T> &B) {
  const std::size_t n = A.size();
  if (n == 1) {
    return {{A[0][0] * B[0][0]}};
  }

  const std::size_t newSize = n / 2;
  Matrix<T> A11(newSize, std::vector<T>(newSize));
  Matrix<T> A12(newSize, std::vector<T>(newSize));
  Matrix<T> A21(newSize, std::vector<T>(newSize));
  Matrix<T> A22(newSize, std::vector<T>(newSize));
  Matrix<T> B11(newSize, std::vector<T>(newSize));
  Matrix<T> B12(newSize, std::vector<T>(newSize));
  Matrix<T> B21(newSize, std::vector<T>(newSize));
  Matrix<T> B22(newSize, std::vector<T>(newSize));

  for (std::size_t i = 0; i < newSize; i++) {
    for (std::size_t j = 0; j < newSize; j++) {
      A11[i][j] = A[i][j];
      A12[i][j] = A[i][j + newSize];
      A21[i][j] = A[i + newSize][j];
      A22[i][j] = A[i + newSize][j + newSize];
      B11[i][j] = B[i][j];
      B12[i][j] = B[i][j + newSize];
      B21[i][j] = B[i + newSize][j];
      B22[i][j] = B[i + newSize][j + newSize];
    }
  }

  const Matrix<T> P1 = fast_multiply(A11, subtract(B12, B22));
  const Matrix<T> P2 = fast_multiply(add(A11, A12), B22);
  const Matrix<T> P3 = fast_multiply(add(A21, A22), B11);
  const Matrix<T> P4 = fast_multiply(A22, subtract(B21, B11));
  const Matrix<T> P5 = fast_multiply(add(A11, A22), add(B11, B22));
  const Matrix<T> P6 = fast_multiply(subtract(A12, A22), add(B21, B22));
  const Matrix<T> P7 = fast_multiply(subtract(A11, A21), add(B11, B12));

  const Matrix<T> C11 = add(subtract(add(P5, P4), P2), P6);
  const Matrix<T> C12 = add(P1, P2);
  const Matrix<T> C21 = add(P3, P4);
  const Matrix<T> C22 = subtract(subtract(add(P5, P1), P3), P7);

  Matrix<T> C(n, std::vector<T>(n));
  for (std::size_t i = 0; i < newSize; i++) {
    for (std::size_t j = 0; j < newSize; j++) {
      C[i][j] = C11[i][j];
      C[i][j + newSize] = C12[i][j];
      C[i + newSize][j] = C21[i][j];
      C[i + newSize][j + newSize] = C22[i][j];
    }
  }

  return C;
}

template <typename T>
Matrix<T> multiply(const Matrix<T> &A, const Matrix<T> &B) {
  const std::size_t n = A.size();
  Matrix<T> C(n, std::vector<double>(n, 0));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        C[i][j] += A[i][k] * B[k][j];
      }
    }
  }
  return C;
}

int main(int argc, char *argv[]) {
  if (argc != 3) {
    std::cout << "Usage: " << argv[0] << " <matrix size> <iterations>"
              << std::endl;
    std::exit(EXIT_FAILURE);
  }

  const std::size_t n = atoi(argv[1]);
  const std::size_t iterations = atoi(argv[2]);

  const Matrix<double> A = generate_random_matrix(n);
  const Matrix<double> B = generate_random_matrix(n);

  for (int i = 0; i < iterations; i++) {
    benchmark::DoNotOptimize(multiply(A, B));
  }
}
