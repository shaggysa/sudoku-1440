#!/usr/bin/env python3
try:
    from sudoku_1440.sudoku_gui import SudokuApp
except ModuleNotFoundError: #in case user directly runs main.py
        from sudoku_gui import SudokuApp
def main():
    app = SudokuApp()
    app.run()

if __name__ == '__main__':
    exit(main())
    