from dataclasses import dataclass, field
from copy import deepcopy
import csv


@dataclass(kw_only=True)
class Puzzle:
    positions: list[set[int]] = field(
        default_factory=lambda: [set(range(1, 10)) for _ in range(9 * 9)]
    )

    def print(self) -> None:
        solutions: list[int] = [
            str(list(position)[0]) if len(position) == 1 else "0"
            for position in self.positions
        ]
        for i in range(9):
            print(" ".join(solutions[i * 9:(i + 1) * 9]))
    
    def solved(self) -> bool:
        return all(len(position) == 1 for position in self.positions)
    
    def row_positions(self, index: int, *, exclude: bool = True) -> list[set[int]]:
        """Give other positions in the same row as the given index."""
        row = index // 9
        start = row * 9
        positions = puzzle.positions[start:start + 9]
        if exclude:
            positions.remove(self.positions[index])
        return positions

    def column_positions(self, index: int, *, exclude: bool = True) -> list[set[int]]:
        """Give other positions in the same column as the given index."""
        col = index % 9
        positions = self.positions[col::9]
        if exclude:
            positions.remove(self.positions[index])
        return positions

    def box_positions(self, index: int, *, exclude: bool = True) -> list[set[int]]:
        """Give other positions in the same 3x3 box as the given index."""
        row = index // 9
        col = index % 9
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        positions = [
            self.positions[r * 9 + c]
            for r in range(box_row, box_row + 3)
            for c in range(box_col, box_col + 3)]
        if exclude:
            positions.remove(self.positions[index])
        return positions


def load() -> list[Puzzle, Puzzle]:
    reader = csv.DictReader(open("libraries/puzzles.csv", "r"))
    return [
        (
            Puzzle(positions=[
                {1,2,3,4,5,6,7,8,9} if num == "0" else {int(num)}
                for num in row["puzzle"]
            ]),
            Puzzle(positions=[{int(num)} for num in row["solution"]]),
        )
        for row in reader
    ]


def solve(unsolved: Puzzle) -> Puzzle:
    puzzle = deepcopy(unsolved)

    while not puzzle.solved():
        progressed = False

        # Algorithm 1: Remove possibilities based on existing numbers
        for i, position in enumerate(puzzle.positions):
            if len(position) != 1:
                continue
        
            value = list(position)[0]
            other_positions = [
                *puzzle.row_positions(i),
                *puzzle.column_positions(i),
                *puzzle.box_positions(i),
            ]
            for position in other_positions:
                if value in position:
                    position.remove(value)
                    progressed = True

        if not progressed:
            break

    return puzzle


if __name__ == "__main__":
    loaded = load()
    puzzle, _ = loaded[0]
    puzzle.print()

    solved = solve(puzzle)
    print()
    solved.print()
