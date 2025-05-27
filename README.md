# sudoku-1440

This is an interactive sudoku creating/solving GUI in 1440p created in python with Tkinter.

Resolution scaling has been implemented, but it is a work in progress.

It can solve puzzles you input and create its own puzzles for you to solve.

## dependencies

Numpy: Puzzles are internally represented as numpy arrays.

Pandas: Reuqired in order to read from the "puzzles.csv file."

Tk: GUI is coded with Tk.

## usage

Once you have installed the dependancies with pip and downloaded the source code, simply run "python3 main.py" in a terminal within the project's folder and the gui will pop up. You can also run speedtest.py to test the speed of the solver. Double clicking on the file to execute it may or may not work depending on the environment.

The GUI has two main modes: an "input mode" and a "solving mode". By default, the GUI is in the input mode. If you input a valid puzzle and press submit, it will take the puzzle and bring you to solving mode if the puzzle is valid. In solving mode, you can either solve it yourself and have the computer check your work or have the computer solve it on its own.

