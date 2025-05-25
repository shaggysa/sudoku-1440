import numpy as np
import pandas as pd
from math import floor
from time import time
class sudoku_solver:
    def __init__(self):
        pass
    def _no_repeats(self,arr) -> bool:
        """_Checks if there is a repetition of any number except for zero._

        Args:
            arr (_type_): _The array you want to check for repeats._

        Returns:
            bool: _Returns true if there are not any repeats, otherwise it will return false._
        """
        li = arr.tolist()
        for i in li:
            if (i[0]) != 0.0:
                if li.count(i) > 1:
                    return False
        return True
                
    def is_valid(self,puzzle:np.array) -> bool:
        """_Checks if the puzzle meets all the requirements to be a valid sudoku puzzle. All zeros are treated as "blank" and ignored._

        Args:
            puzzle (np.array): _The 9x9 numpy array representing your puzzle._

        Returns:
            bool: _Returns true if the puzzle is valid, otherwise it will return false._
        """
        row_major = puzzle.reshape((81,1), order = 'C')
        column_major = puzzle.reshape((81,1), order = 'F')
        
        for i in range(0,9):
            if not self._no_repeats(row_major[i*9:(i+1)*9]):
                return False
        
        for i in range(0,9):
            if not self._no_repeats(column_major[i*9:(i+1)*9]):
                return False
        
        #check for repeats within squares
        for i in range(0, 54, 27):
            for j in range(i, i+9, 3):
                indices = [j, j+1, j+2, j+9, j+10, j+11, j+18, j+19, j+20]
                if not self._no_repeats(row_major[indices]):
                    return False
        return True

    def pos_valid(self,puzzle:np.array, pos:int) -> bool:
        """_Checks if a number in a given position is vaid within a given puzzle._
        Args:
            puzzle (np.array): _The 9x9 numpy array representing your puzzle._
            pos (int): _The position within the array you want to check. The number represents the array indice if you flatten the 9x9 array in row-major._

        Returns:
            bool: _Should the rows, columns, or squares affecting the given position break sudoku conventions, the method will return false. Otherwise, it will return true. Zeros are ignored._
        """
        row_major = puzzle.reshape((81,1), order = 'C')
        column_major = puzzle.reshape((81,1), order = 'F')
        
        row = floor(pos/9)
        col = pos % 9
        
        if not self._no_repeats(row_major[row*9:(row+1)*9]):
            return False
        
        if not self._no_repeats(column_major[col*9:(col+1)*9]):
            return False
        
        #check for repeats within squares
        for i in range(0, 54, 27):
            for j in range(i, i+9, 3):
                indices = [j, j+1, j+2, j+9, j+10, j+11, j+18, j+19, j+20]
                if pos in indices:
                    if not self._no_repeats(row_major[indices]):
                        return False
                    break
        return True

    def _gen_list(self, file:str) -> list:
        """_Generates a 2D list of all the unsolved puzzles found in a csv file of the format "solved,unsolved". You can do [line_num - 2] on generated list to pick a specific puzzle._

        Args:
            file (str): _The name of the file you want to read._

        Returns:
            list: _List of the puzzles generated from the csv file._
        """
        ls = []
        data = pd.read_csv(file).to_numpy()
        for item in data:
            ls.append(item[0])
        for i, item in enumerate(ls):
            x = []
            for j in item:
                x.append(j)
            ls[i] = x
        return ls
            
    def _array_ify(self, puzzle_list:list) -> np.array:
        """_Turns a list with a length of 81 into a 9x9 numpy array._

        Args:
            puzzle_list (list): _The 81 length list you want to convert._

        Returns:
            np.array : _The 9x9 numpy array generated from the list._
        """
        if len(puzzle_list) != 81:
            raise IndexError(message = 'This method only accepts lists with a length 81')
        arr = np.empty((9,9))
        x = 0
        for i in range(0,9):
            for j in range(0,9):
                arr[i][j] = puzzle_list[x]
                x += 1
        return arr
                    
    def read_puzzle(self, file:str, puzzle_line_num:int) -> np.array:
        """_Reads a sudoku puzzle from a csv file and converts it into a 9x9 numpy array._

        Args:
            file (str): _The csv file you want to read. It should be in the format "puzzle,solution", but a solution is not required._
            puzzle_line_num (int): _The line number corresponding to the puzzle you want to read from the file._

        Returns:
            np.array: _The 9x9 numpy array generated from the line in the puzzle._
        """
        return self._array_ify(self._gen_list(file)[puzzle_line_num-2]).reshape((9,9))

    def solving_prep(self, puzzle:np.array, passthrough_params:tuple = None):
        """_Attempts to solve a sudoku by continuously eliminating all blank values in the array that only have one solution. Should successfully solve most simple puzzles.
        The result can be passed into the proper solver incase this method can't fully solve it. Returns a tuple containing the puzzle after this method has finished and the list of blank values in the array._

        Args:
            puzzle (np.array): _The 9x9 numpy array representing your unsolved puzzle._
            passthrough_params (tuple, optional): _Used internally to passthrough values for recursion. Do not use._ Defaults to None.

        """
        
        
        if passthrough_params == None:
            blank = []
            p = puzzle.copy()
            flat = p.reshape((81,1))
            for i, item in enumerate(flat):
                if item[0] == 0.0:
                    blank.append(i)
            
        else:
            p = puzzle
            flat = p.reshape((81,1))
            blank = passthrough_params[0]
            if passthrough_params[1] == True:
                return p, blank
        p = puzzle
        done = True
        to_remove = []
        for i in blank:
            valid_nums = []
            for j in range(1,10):
                flat[i] = j
                if self.pos_valid(flat.reshape((9,9)), i):
                    valid_nums.append(j)
            if len(valid_nums) == 1:
                flat[i] = valid_nums[0]
                to_remove.append(i)
                done = False
            else:
                flat[i] = 0
        for x in to_remove:
            blank.remove(x)
        return self.solving_prep(flat.reshape((9,9)), (blank, done))

    def solve(self, puzzle:np.array) -> np.array:
        """_Solves any valid unsolved sudoku puzzle._

        Args:
            puzzle (np.array): _The unsovled puzzle as a 9x9 numpy array._

        Returns:
            np.array: _The solved puzzle as a 9x9 numpy array._
        """
        new_puzz, blank = self.solving_prep(puzzle)
        if not 0 in new_puzz:
            return new_puzz
        possibilities = {}
        current_pos = {}
        flat = new_puzz.reshape((81,1))

        for i in blank:
            valid_nums = []
            for j in range(1,10):
                flat[i] = j
                if self.is_valid(flat.reshape((9,9))):
                    valid_nums.append(j)
            flat[i] = 0
            possibilities.update({i:valid_nums})
            current_pos.update({i:-1})
        item = 0
        
        while 0 in flat or (not self.is_valid(flat.reshape((9,9)))):
            found = False
            curr = blank[item]
            while current_pos[curr] < len(possibilities[curr])-1:
                current_pos[curr] += 1
                flat[curr] = possibilities[curr][(current_pos[curr])]
                if self.pos_valid(flat.reshape((9,9)), curr):
                    found = True
                    item += 1
                    break
                
            if not found:
                flat[curr] = 0
                current_pos[curr] = -1
                item -= 1
        return flat.reshape((9,9))

    def check_ans(self,computer_solved:np.array, ans:list) -> bool:
        """_Checkes if the answer given by the solver is correct using a known correct answer._

        Args:
            computer_solved (np.array): _The puzzle solved by the solving algorithm as a 9x9 numpy array._
            ans (list): _The known correct answer as a list._

        Returns:
            bool: _Returns true if the computer generated answer is correct. Otherwise, it will return false._
        """
        fin = ''
        resized = computer_solved.reshape((81,1))
        ls = resized.tolist()
        for i in ls:
            fin += str(int((i[0])))
        if fin == ans:
            return True
        else:
            return False
    
    def solve_and_check(self, puzzle_line_num:int, file:str) -> None:
        """_Prints the unsolved puzzle, the solved puzzle, and if the solved puzzle matches the answer key in the csv file if it is in the format "puzzle, solution"._

        Args:
            puzzle_line_num (_int_): _The line number of the puzzle you want to solve and check._
            file (str): _The csv file containing the puzzle you want to solve and check._
        """
        unsolved = self.read_puzzle(file, puzzle_line_num)
        print(f"Unsolved:\n{unsolved.astype(int)}")
        solved = self.solve(unsolved)
        print(f'Solved:\n{solved.astype(int)}')
        ans = pd.read_csv(file).to_numpy()
        if self.check_ans(solved, ans[puzzle_line_num-2][1]):
            print('Solved puzzle matches answer key!')
            return True
        else:
            print('Solved puzzle does not match answer key...\nΣ(-᷅_-᷄๑)')
            return False
        
solver = sudoku_solver()

#you can change the 1002 to any number you would like in order to solve a different problem

#solver.solve_and_check(1002,'puzzles.csv')








    



