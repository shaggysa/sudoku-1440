#!/usr/bin/env python3
from libraries.sudoku_gui import sudoku_gui
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

if __name__ == '__main__':
    gui = sudoku_gui()