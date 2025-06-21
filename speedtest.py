#!/usr/bin/env python3
from libraries.sudoku_solver import SudokuSolver
import os
import sys
sys.setrecursionlimit(1000000)



def main():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
   
    csv_file_path = os.path.join(base_path, 'libraries', 'puzzles.csv')
    
    SudokuSolver.speedtest(csv_file_path, 2, 1001)
    
if __name__ == "__main__":
    main()
    input('Press enter to close.')
"""
My stats (R7 7700x, RTX 3070ti):
Read 1000 puzzles from /home/shaggy/Documents/sudoku-1440/libraries/puzzles.csv in 10.715484619140625 ms

Solving stats:
Mean: 1.5966997146606445 ms
Median: 0.2048015594482422 ms
Minimum: 0.031948089599609375 ms
Maximum: 517.8627967834473 ms
Total (solving time): 1596.6997146606445 ms

Total (all time spent including printing/checking/puzzle reading overhead): 1692.9492950439453 ms
"""