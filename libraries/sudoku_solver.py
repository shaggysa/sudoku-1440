from libraries.puzzle import Puzzle
from libraries.puzzle_reader import PuzzleReader
from time import time
from copy import copy
import statistics


try:
    import pandas as pd
except ImportError:
    print('Unable to import pandas! Please install it with "pip install pandas".')
    
class SudokuSolver:
    @staticmethod
    def print_puzzle(puzzle:list):
        for i in range (9):
            for j in range(9):
                print(puzzle[j + (i*9)], end="  ")
            print()
   
    @staticmethod
    def _no_repeats(arr:list) -> bool:
        """_Checks if there is a repetition of any number except for zero._

        Args:
            arr (_list_): _The list you want to check for repeats._

        Returns:
            bool: _Returns true if there are not any repeats, otherwise it will return false._
        """

        arr = [x for x in arr if x]
        return len(set(arr)) == len(arr)

    @staticmethod
    def pos_valid(puzzle:list, pos:int) -> bool:
        """_Checks if a number in a given position is vaid within a given puzzle._
        Args:
            puzzle (list): _The list representing your puzzle._
            pos (int): _The position within the array you want to check._

        Returns:
            bool: _Should the rows, columns, or squares affecting the given position break sudoku conventions, the method will return false. Otherwise, it will return true. Zeros are ignored._
        """
        row = pos // 9
        col = pos % 9
        
        root_row = (row // 3) * 3
        root_col = (col // 3) * 3
        
        start = row * 9
        row_to_check = puzzle[start:start + 9]
        col_to_check = puzzle[col::9]
        square_to_check = [puzzle[r * 9 + c] for r in range(root_row, root_row + 3) for c in range(root_col, root_col + 3)]
        if __class__._no_repeats(row_to_check):
            if __class__._no_repeats(col_to_check):
                if  __class__._no_repeats(square_to_check):
                    return True
        return False
   
    @staticmethod
    def solve(puzzle:list) -> list:
        """_Solves any valid unsolved sudoku puzzle._

        Args:
            puzzle (list): _The unsovled puzzle as an 81-length list with zeros representing blank squares._

        Returns:
            list: _The solved puzzle as an 81-length list._
        """
        p = Puzzle(copy(puzzle))
        if p.solved:
            return p.puzzle
        p.forward_init()
        return __class__.unwrapped_solve(p)
    
    @staticmethod
    def unwrapped_solve(puzz:Puzzle, position:int = 0) -> list:
        """_Solves a sudoku puzzle using a recursive backtracker._

        Args:
            puzz (Puzzle): _The puzzle you want to solve after initializing it as a Puzzle object._
            position (int, optional): _The current position the backtracker is working on. Used internally._ Defaults to 0.

        Returns:
            list: _The final solved puzzle._
        """
        if position < 0:
            print("The puzzle is unsolvable!")
            return []
        elif position == len(puzz.blank_positions):
            puzz.solved == True
            return puzz.puzzle
        
        spot = puzz.blank_positions[position]
        max = len(puzz.possibilities[spot]) - 1
        
        while puzz.current_position[spot] < max:
            puzz.current_position[spot] += 1
            puzz.puzzle[spot] = puzz.possibilities[spot][puzz.current_position[spot]]
            if __class__.pos_valid(puzz.puzzle, spot):
                return __class__.unwrapped_solve(puzz, position + 1)
        
        puzz.puzzle[spot] = 0
        puzz.current_position[spot] = -1
        return __class__.unwrapped_solve(puzz, position - 1)   
    
    @staticmethod
    def all_valid(puzzle:list) -> bool:
        """_Checks the entire puzzle to ensure that it does not break sudoku conventions._

        Args:
            puzzle (list): _The puzzle you want to check._

        Returns:
            bool: _Returns true if the puzzle is valid. Otherwise returns false._
        """
        for i in range(0, 81, 10):
            if not __class__.pos_valid(puzzle, i):
                return False
        return True         
  
    @staticmethod
    def speedtest(file:str, first_line:int, last_line:int) :
        """Tests the speed for solving a bunch of puzzles at once. Uses console to log information.

        Args:
            file (str): _The path to the csv file containing the puzzles you want to test the solver with. It needs to be in the format "Puzzle, Solution" or the test will fail._
            first_line (int): _The line containing the first puzzle you want to test._
            last_line (int): _The line containing the last puzzle you want to test._
        """
        times = []
        file_read_start = time()
        p = PuzzleReader(file)
        file_read_time = time() - file_read_start
        for i in range(first_line,last_line+1):
            unsolved = p.get_puzzle(i)
            print(f"Line number {i}:")
            print("Unsolved:\n")
            __class__.print_puzzle(unsolved)
            solved = p.get_solution(i)
            start_time = time()
            pc_solved = __class__.solve(unsolved)
            times.append(time() - start_time)
            print("\nSolved:\n")
            __class__.print_puzzle(pc_solved)
            if pc_solved != solved:
                print("The solved puzzle does not match the answer key! The answer is: \n")
                __class__.print_puzzle(solved)
                raise RuntimeError("Speedtest failed! Please check your CSV file and ensure it is in the correct format.")
        print(f'''\nTest Suceeded! Here are the stats:
Read {p.num_puzzles} puzzles from {file} in {file_read_time*1000} ms

Solving stats:
Mean: {statistics.mean(times)*1000} ms
Median: {statistics.median(times)*1000} ms
Minimum: {min(times)*1000} ms
Maximum: {max(times)*1000} ms
Total (solving time): {sum(times)*1000} ms

Total (all time spent including printing/checking/puzzle reading overhead): {(time() - file_read_start)*1000} ms''')



    



