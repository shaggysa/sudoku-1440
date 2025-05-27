from libraries.sudoku_solver import sudoku_solver

try:
    import numpy as np
except ImportError:
    print('Unable to import numpy! Please install it with "pip install numpy".')

from random import choice, shuffle, randint
from copy import copy
class sudoku_creator(sudoku_solver):
    def solve(self, puzzle:np.array) -> np.array:
        """_Solves any valid unsolved sudoku puzzle. The possible solutions for each square are randomized, allowing for _

        Args:
            puzzle (np.array): _The unsovled puzzle as a 9x9 numpy array._

        Returns:
            np.array: _The solved puzzle as a 9x9 numpy array._
        """
        try:
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
                shuffle(valid_nums)
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
        except IndexError:
            raise RuntimeError('The puzzle is unsolvable!')

    def reverse_solve(self, puzzle:np.array) -> np.array:
        """_Solves any valid unsolved sudoku puzzle in reverse. Can be crosschecked with the regular solver from the parent class to ensure there is only one solution._

        Args:
            puzzle (np.array): _The unsovled puzzle as a 9x9 numpy array._

        Returns:
            np.array: _The solved puzzle as a 9x9 numpy array._
        """
        try:
            new_puzz, blank = self.solving_prep(puzzle)
            if not 0 in new_puzz:
                return new_puzz
            possibilities = {}
            current_pos = {}
            flat = new_puzz.reshape((81,1))

            for i in blank:
                valid_nums = []
                for j in range(9,0,-1):
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
        except IndexError:
            raise RuntimeError('The puzzle is unsolvable!')

    def blank_puzzle(self) -> np.array:
        """_Creates a 9x9 sudoku grid filled with all zeros._

        Returns:
            np.array: _Empty sudoku grid._
        """
        puzz = np.empty((9,9))
        for i, _ in enumerate(puzz):
            puzz[i] = 0
        return puzz
        
    def create_solved_puzzle(self) -> np.array: 
        return self.solve(self.blank_puzzle())
    
    def single_solution(self, puzzle:np.array) -> bool:
        """_Checks if a puzzle only has one solution by solving it in both standard and reverse order._

        Args:
            puzzle (np.array): _The puzzle you want to check._

        Returns:
            bool: _Returns true if the puzzle only has one solution. Otherwise, it will return false._
        """
        return True if (super().solve(puzzle) == self.reverse_solve(puzzle)).all() else False
  
    def create_unsolved(self, puzzle:np.array = None, min_hints:int = randint(24,36), fails:int = 0) -> np.array:
        """_Randomly removes hints from a puzzle until it reaches the desired number of hints or there are multiple solutions._

        Args:
            puzzle (np.array, optional): _The filled puzzle. Do not need to use unless you want to remove hints from a specific puzzle._ Defaults to None.
            min_hints (int, optional): _The minimum number of hints you want your final puzzle to have. There needs to be at least 17 hints for the puzzle to be valid._ Defaults to randint(20,30).
            fails (int, optional): _Internally used to check how many times in a row the creator has removed a value that has caused the puzzle to have multiple solutions. Do not use._ Defaults to 0.

        Returns:
            np.array: _The final unsolved puzzle._
        """
        try:
            if puzzle == None:
                puzzle = self.create_solved_puzzle()
        except ValueError:
            pass

        flat = puzzle.reshape((81,1))
        filled = []
        for i, item in enumerate(flat):
            if item != 0:
                filled.append(i)
        try:
            if min_hints < len(filled):
                z = choice(filled)
                y = copy(flat[z])
                flat[z] = 0
                puzzle = flat.reshape((9,9))
                if self.single_solution(puzzle):
                    return self.create_unsolved(puzzle, min_hints)
                else:
                    flat[z] = y
                    if fails > 10:
                        return puzzle
                    return self.create_unsolved(puzzle, min_hints, fails+1)
            else:
                return puzzle
        except RecursionError:
            return puzzle,len(filled)

    
    
    


#uncomment the below lines to test out the creator

#creator = sudoku_creator()

#print(print(creator.create_unsolved(min_hints=17)))

