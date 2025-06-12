#!/usr/bin/env python3
from libraries.sudoku_solver import sudoku_solver
import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    sudoku_solver.speedtest('libraries/puzzles.csv', 2, 1001)

"""
Stats for the above test on my PC (R7 7700x, 3070ti, 32GB DDR5 6000)

Mean: 13.052264213562012 ms
Median: 3.6373138427734375 ms
Minimum: 0.4737377166748047 ms
Maximum: 1606.2617301940918 ms
Total: 13052.264213562012 ms
"""
