#!/usr/bin/env python3
from libraries.sudoku_solver import sudoku_solver
import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    sudoku_solver.speedtest('libraries/puzzles.csv', 2, 1001)

"""
Stats for the above test on my PC (R7 7700x, 3070ti, 32GB DDR5 6000)

Mean: 0.017035149574279786
Median: 0.007970571517944336
Minimum: 0.004830837249755859
Maximum: 1.5861012935638428
Total: 17.035149574279785
"""
