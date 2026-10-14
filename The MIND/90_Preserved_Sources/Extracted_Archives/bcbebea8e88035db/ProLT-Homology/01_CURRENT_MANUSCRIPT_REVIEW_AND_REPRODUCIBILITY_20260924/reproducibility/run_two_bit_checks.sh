#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python verify_two_bit_height_two_counterexample.py | tee two_bit_7_local.out
g++ -O3 -std=c++17 two_bit_height2_exhaustive.cpp -o two_bit_height2_exhaustive
for n in 1 2 3 4 5 6; do
  ./two_bit_height2_exhaustive "$n" | tee "two_bit_n${n}_local.out"
done
