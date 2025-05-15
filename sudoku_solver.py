import numpy as np
import pandas as pd

def gen_list(file:str):
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
    
def array_ify(puzzle_list:list):
    arr = np.empty((9,9))
    x = 0
    for i in range(0,9):
        for j in range(0,9):
            arr[i][j] = puzzle_list[x]
            x += 1
    return arr
            
def _no_repeats(arr):
    li = arr.tolist()
    for i in li:
        if (i[0]) != 0.0:
            if li.count(i) > 1:
                return False
    return True
            
def is_valid(puzzle:np.array):
    row_major = puzzle.reshape((81,1), order = 'C')
    column_major = puzzle.reshape((81,1), order = 'F')
     
    for i in range(0,9):
        if not _no_repeats(row_major[i*9:(i+1)*9]):
            return False
    
    for i in range(0,9):
        if not _no_repeats(column_major[i*9:(i+1)*9]):
            return False
    
    #check for repeats within squares
    for i in range(0, 54, 27):
        for j in range(i, i+9, 3):
            indices = [j, j+1, j+2, j+9, j+10, j+11, j+18, j+19, j+20]
            if not _no_repeats(row_major[indices]):
                return False
    return True

def solve(puzzle:np.array):
    flat = puzzle.reshape((81,1))
    ls = flat.tolist()
    blank = []
    for i, item in enumerate(ls):
        if item[0] == 0.0:
            blank.append(i)
    i = 0
    while 0 in flat or (not is_valid(flat.reshape((9,9)))):
        while True:
            flat[blank[i]] += 1
            if is_valid(flat.reshape((9,9))) and flat[blank[i]] <= 9:
                i += 1
                break
            if flat[blank[i]] > 9:
                flat[blank[i]] = 0
                i -= 1
                break
    return flat
         
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

def solve_and_check(puzzle_num):
    unsolved = array_ify(gen_list('puzzles.csv')[puzzle_num]).reshape((9,9))
    print(f"Unsolved\n:{unsolved.astype(int)}")
    solved = solve(array_ify(gen_list('puzzles.csv')[puzzle_num])).reshape((9,9))
    print(f'Solved:\n{solved.astype(int)}')
    ans = pd.read_csv('puzzles.csv').to_numpy()
    if check_ans(solved, ans[puzzle_num][1]):
        print('Solved puzzle matches answer key!')
    else:
        print('Solved puzzle does not match answer key...\nΣ(-᷅_-᷄๑)')

solve_and_check()
    



    



