#!/usr/bin/env python3
from libraries.sudoku_gui import sudoku_gui
import os
import sys

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    gui = sudoku_gui()