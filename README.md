# hpc

Sequential and parallel merge sort and quick sort in C with OpenMP, plus the tools to generate input, check the output and benchmark both versions across input sizes and thread counts.

## What is inside

| File | Role |
| --- | --- |
| `src/sort.c` | Sequential merge sort and quick sort |
| `src/sort_parallel.c` | Parallel versions: merge sort splits each half into `omp parallel sections`, quick sort spawns an `omp task` per partition inside a single parallel region |
| `src/generate.c` | Writes N random 32-bit integers to a binary file |
| `src/check_sort.c` | Reads a binary file and reports the first position out of order, if any |
| `test_performance.py` | Builds everything, runs both algorithms on 512K, 1M, 256M and 512M integers with 1, 2, 4, 8 and 16 threads, then saves `out/performance_results.json` and `out/performance_plots.png` |

Files are raw arrays of `int`, with no header.

## Build

Requires a C compiler with OpenMP support (GCC, or Clang with `libomp`).

```bash
make            # builds out/sort.exe, out/sort_parallel.exe, out/generate.exe and out/check_sort.exe
```

On macOS, Apple Clang has no `-fopenmp`; use Homebrew GCC, for example `make CC=gcc-14`.

## Run

```bash
./out/generate.exe 1000000 out/in.bin                     # 1M random integers
./out/sort.exe merge out/in.bin out/out.bin               # sequential: merge | quick
./out/sort_parallel.exe quick 8 out/in.bin out/out.bin    # parallel: algorithm, threads, input, output
./out/check_sort.exe out/out.bin                          # verifies the result is sorted
```

Every argument is optional. The defaults are `merge`, all available threads, `out/in.bin` and `out/out.bin`.

## Benchmark

```bash
./run_tests.sh   # installs matplotlib and numpy, then runs test_performance.py
```

The two largest inputs take 1 GB and 2 GB of memory per run. Trim `input_sizes` in `test_performance.py` on smaller machines.
