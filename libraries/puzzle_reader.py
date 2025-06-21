from csv import DictReader

class PuzzleReader:
    """_A class used to read sudoku puzzles from a csv file._
    """
    def __init__(self, file:str):
        self.puzzles = []
        self.solutions = []
        self.num_puzzles = 0
        data = DictReader(open(file, "r"))
        
        for row in data:
            puzzle = []
            solution = []
            
            for num in row["puzzle"]:
                puzzle.append(int(num))
            
            for num in row["solution"]:
                solution.append(int(num))
            
            self.puzzles.append(puzzle)
            self.solutions.append(solution)
            self.num_puzzles += 1
            
    def get_puzzle(self, line_number:int) -> list:
        """_Get an unsolved puzzle from the csv library._

        Args:
            line_number (int): _The line on the csv file that you want to read the unsolved puzzle from._

        Returns:
            _list_: _The 81 length list representinge the unsolved puzzle._
        """
        return self.puzzles[line_number-2]
    
    def get_solution(self, line_number:int) -> list:
        """_Get a solved puzzle from the csv library._

        Args:
            line_number (int): _The line on the csv file that you want to read the solved puzzle from._

        Returns:
            list: _The 81 length list representinge the unsolved puzzle._
        """
        return self.solutions[line_number-2]

    