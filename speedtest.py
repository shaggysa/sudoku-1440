from sudoku_solver import sudoku_solver
from time import time
import statistics

def speedtest(file:str, first_line:int, last_line:int) :
    """Tests the speed for solving a bunch of puzzles at once. 

    Args:
        file (str): _The csv file containing the puzzles you want to test the solver with. It needs to be in the format "Puzzle, Solution" or the test will fail._
        first_line (int): _The line containing the first puzzle you want to test._
        last_line (int): _The line containing the last puzzle you want to test._
    """
    solver = sudoku_solver()
    times = []
    for i in range(first_line,last_line+1):
        print("Puzzle:", i)
        last = time()
        if solver.solve_and_check(i, file) == False:
            print("Test failed!")
            return None
        times.append(time()-last)
    print("Test Suceeded!")
    print("Mean:",statistics.mean(times))
    print("Median:",statistics.median(times))
    print("Minimum:",min(times))
    print("Maximum:", max(times))
    print("Total:",sum(times))

    
speedtest('puzzles.csv', 2, 1001)

"""
Stats for the above test on my PC (R7 7700x, 3070ti, 32GB DDR5 6000)

Mean: 0.017035149574279786
Median: 0.007970571517944336
Minimum: 0.004830837249755859
Maximum: 1.5861012935638428
Total: 17.035149574279785
"""
