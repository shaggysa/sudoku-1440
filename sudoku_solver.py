import numpy as np
import pandas as pd
from math import floor
class sudoku_solver:
    def __init__(self):
        pass
    def _no_repeats(self,arr):
        li = arr.tolist()
        for i in li:
            if (i[0]) != 0.0:
                if li.count(i) > 1:
                    return False
        return True
                
    def is_valid(self,puzzle:np.array):
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

    def pos_valid(self,puzzle:np.array, pos):
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

    def _gen_list(self, file:str):
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
            
    def _array_ify(self, puzzle_list:list):
            arr = np.empty((9,9))
            x = 0
            for i in range(0,9):
                for j in range(0,9):
                    arr[i][j] = puzzle_list[x]
                    x += 1
            return arr
                    
    def read_puzzle(self, file:str, puzzle_num:int):
        return self._array_ify(self._gen_list(file)[puzzle_num-2]).reshape((9,9))
    
    def solve(self, puzzle:np.array):
        blank = []
        possibilities = {}
        current_pos = {}
        flat = puzzle.reshape((81,1))
        ls = flat.tolist()
        for i, item in enumerate(ls):
            if item[0] == 0.0:
                blank.append(i)

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
    
solver = sudoku_solver()

def check_ans(computer_solved:np.array, ans:list):
    fin = ''
    resized = computer_solved.reshape((81,1))
    ls = resized.tolist()
    for i in ls:
        fin += str(int((i[0])))
    if fin == ans:
        return True
    else:
        return False

def solve_and_check(puzzle_line_num, file:str):
    unsolved = solver.read_puzzle(file, puzzle_line_num)
    print(f"Unsolved:\n{unsolved.astype(int)}")
    solved = solver.solve(unsolved)
    print(f'Solved:\n{solved.astype(int)}')
    ans = pd.read_csv(file).to_numpy()
    if check_ans(solved, ans[puzzle_line_num-2][1]):
        print('Solved puzzle matches answer key!')
    else:
        print('Solved puzzle does not match answer key...\nΣ(-᷅_-᷄๑)')

#you can change the 1002 to any number you would like in order to solve a different problem
solve_and_check(1002,'puzzles.csv')








    



