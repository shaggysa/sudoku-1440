#!/usr/bin/env python3
try:
    import lib_sudoku as sudoku
except ModuleNotFoundError:
    print("Please install lib_sudoku with pip")
    exit(1)
def main():
    reader = sudoku.PuzzleReader("https://raw.githubusercontent.com/shaggysa/lib_sudoku/master/puzzles.csv", True)
    sudoku.synchronous_speedtest(reader)
    sudoku.async_speedtest(reader)
    
if __name__ == "__main__":
    main()
    input('Press enter to close.')

"""
My Stats (R7 7700x, RTX 3070Ti, 32GB RAM)
Downloaded https://raw.githubusercontent.com/shaggysa/lib_sudoku/master/puzzles.csv in 136.660287ms
Parsed 1000 puzzles in 38.259µs.
---------------
Starting Synchronous Speedtest
---------------
Solved 1000 Puzzles in 8.920093ms
Validated 1000 puzzles in 11.03µs
---------------
Starting Async Speedtest
---------------
Solved 1000 Puzzles in 2.916249ms
Validated 1000 puzzles in 10.65µs
"""