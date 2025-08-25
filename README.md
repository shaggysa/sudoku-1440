# sudoku-1440

This is an interactive sudoku creating/solving GUI created in python with kivy.

Resolution scaling has been implemented, and it should work on just about any (reasonable) screen resolution.

It can solve puzzles you input and create its own puzzles for you to solve. 

There is also a 'speedtest' application to see how fast the solver is.

## dependencies as of V3.0

lib_sudoku: My custom sudoku solver and generator.

kivy: Used for the GUI.

## usage

To install with pipx in the terminal, run

```
pipx install sudoku-1440
```

To open the gui, run
```
sudoku_1440
``` 

To speedtest the solver, run
```
sudoku_speedtest
```

If you preferred, you can also speedtest your own puzzle file with

```
sudoku_speedtest <filename>
```

One recommended dataset to try would be https://www.kaggle.com/datasets/rohanrao/sudoku.
