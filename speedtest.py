from libraries.sudoku_solver import sudoku_solver

    
sudoku_solver().speedtest('libraries/puzzles.csv', 2, 1001)

"""
Stats for the above test on my PC (R7 7700x, 3070ti, 32GB DDR5 6000)

Mean: 0.017035149574279786
Median: 0.007970571517944336
Minimum: 0.004830837249755859
Maximum: 1.5861012935638428
Total: 17.035149574279785
"""
