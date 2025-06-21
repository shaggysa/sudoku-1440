#!/usr/bin/env python3
from libraries.sudoku_gui import SudokuApp
import os
import sys

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(base_path, 'libraries', 'puzzles.csv')
    app = SudokuApp(csv_file_path)
    app.run()
    