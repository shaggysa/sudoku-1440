# sudoku-1440

This is an interactive sudoku creating/solving GUI created in python utilizing kivy.

Resolution scaling has been implemented, and it should work on just about any (reasonable) screen resolution.

It can solve puzzles you input and create its own puzzles for you to solve. There is also a 'speedtest' file to see how fast it can solve 1000 puzzles.

## dependencies as of V2.0

csv: Used to read the 'puzzles.csv' file

kivy: Used for the GUI.

## Usage

Once you have installed the dependancies, simply run main.py with python and the gui will pop up. You can run speedtest.py to test the speed of the solver.

As of release 2.0, executables are released with the code. Linux, MacOS, and Windows are all supported in the x64 architecture.
Simply download the correct execuatable and run it!

If your architecture is not supported, you can build the packages yourself by running pyinstaller with the included .spec files. 

*note for linux users: The speedtest.py/executable must open a terminal for you to see the results. Some Desktop Environments such as KDE with not automatically open a termianl and you must run the file directly using the terminal.*

