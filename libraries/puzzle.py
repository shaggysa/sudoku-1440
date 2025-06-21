from random import shuffle
from copy import copy
class Puzzle:
    def __init__(self, puzzle:list):
        self.puzzle = copy(puzzle)
        self.blank_positions = []
        self.possibilities = {}
        self.current_position = {}
        self.solved = False
        self.unsolvable = False
        self._gather_blanks()
        self._pre_init()
    
    def _gather_blanks(self):
        """_Checks all positions in the puzzle for zeros (blank squares)._
        """
        for i, _ in ((i, item) for i, item in enumerate(self.puzzle) if not item):
            self.blank_positions.append(i)
    
    def _pre_init(self):
        """_Iterates through the list of blank squares in the puzzle and checks if any square only has one possible number that can fill it out. It will fill all squares that meet this requirement and recursively call itself until it can't fill out any more squares._
        """
        progressed = False
        for i in copy(self.blank_positions):
            nums = __class__.get_possibilities(self.puzzle, i)
            if len(nums) == 1:
                progressed = True
                self.puzzle[i] = nums.pop()
                self.blank_positions.remove(i)
        
        if progressed:
            self._pre_init()
        
        elif not len(self.blank_positions):
            self.solved = True

    def forward_init(self):
        """_Iterates through all of the blank positions in the puzzle and checks what numbers can fill it out._
        """
        for i in self.blank_positions:
            self.possibilities.update({i:sorted(__class__.get_possibilities(self.puzzle, i))})
            self.current_position.update({i:-1})
            
    def reverse_init(self):
        """_Iterates through all of the blank positions in the puzzle and checks what numbers can fill it out. Reverses ordering of said numbers._
        """
        for i in self.blank_positions:
            self.possibilities.update({i:sorted(__class__.get_possibilities(self.puzzle, i), reverse=True)})
            self.current_position.update({i:-1})
            
    def random_init(self):
        """_Iterates through all of the blank positions in the puzzle and checks what numbers can fill it out. Randomizes ordering of said numbers._
        """
        for i in self.blank_positions:
            x = list(__class__.get_possibilities(self.puzzle, i))
            shuffle(x)
            self.possibilities.update({i:x})
            self.current_position.update({i:-1})
            
    
    @staticmethod
    def get_possibilities(puzzle:list, pos:int) -> set:
        """_Finds all of the possible numbers that can fill out a specific position given a puzzle and the position to check._

        Args:
            puzzle (list): _The puzzle._
            pos (int): _The position you want to check._

        Returns:
            set: _All of the numbers that can occupy the given position._
        """
        row = pos // 9
        col = pos % 9
        
        root_row = (row // 3) * 3
        root_col = (col // 3) * 3
        
        start = row * 9
        row_to_check = set(puzzle[start:start + 9])
        
        col_to_check = set(puzzle[col::9])
        
        square_to_check = set([puzzle[r * 9 + c] for r in range(root_row, root_row + 3) for c in range(root_col, root_col + 3)])
        
        return set(range(1,10)).difference(row_to_check.union(col_to_check.union(square_to_check)))
    