from libraries.sudoku_solver import sudoku_solver
from libraries.sudoku_creator import sudoku_creator
import tkinter as tk
from tkinter import *
from time import time as t
import numpy as np
from math import floor
from random import randint

class sudoku_gui:
    def __init__(self):
        self.current_puzzle = sudoku_creator().blank_puzzle()
        self.inputs = {}
        self.mode = 'submit_unsolved'
        self.main = tk.Tk()
        self.scale = self.main.winfo_screenheight() / 1440
        self.main.title('Sudoku')
        self.c1 = Canvas(self.main, height=round(1400*self.scale), width=round(2560*self.scale), bg='white')
        self.submit_button = Button(self.c1, text="Submit!", anchor="center", height = 2, width = 15, bg = "white", command=self.submit)
        self.read_puzzle_input = Button(self.c1, text="input your own puzzle", height=2, width = 22, bg='white', command=self.input_puzzle)
        self.read_random_button = Button(self.c1, text="read a random puzzle from file", anchor="center", height = 2, width = 22, bg = "white", command=self.read_random_puzzle)
        self.gen_random_button = Button(self.c1, text="generate a random puzzle", anchor="center", height = 2, width = 22, bg = "white", command=self.generate_puzzle)
        self.computer_solve_button = Button(self.c1, text="Solve With Computer", anchor="center", height = 2, width = 15, bg = "white", command=self.computer_solve)
        self.timer = tk.Label(self.c1, text="0:00", font=('Hellvetica', round(12*self.scale)), bg='white')
        self.validate = self.main.register(self.on_validate), '%P'
        self.stopwatch_running = False
        self.stopwatch_start_time = t()
        self.pc_solve_confirm = False
        self.input_puzzle()
        self.main.mainloop()

    def start_stopwatch(self):
        self.stopwatch_running = True
        self.stopwatch_start_time = t()
        self.update_stopwatch()

    def update_stopwatch(self):
        if self.stopwatch_running:
            total_seconds = round(t()-self.stopwatch_start_time)
            seconds_display = total_seconds % 60
            if len(str(seconds_display)) == 1:
                seconds_display = '0' + str(seconds_display)
            time = f'{floor(total_seconds/60)}:{seconds_display}'
            self.timer.config(text=time)
            self.timer.after(1000, self.update_stopwatch)
    
    def on_validate(self, new_text:str) -> bool:
        match len(new_text):
            case 0:
                return True
            case 1:
                return True if new_text.isnumeric() and new_text != '0' else False
            case _:
                return False
                
   
    def message(self, msg):
        message = self.c1.create_text(1270*self.scale, 1170*self.scale, text=msg, anchor=CENTER, font=("Arial", 24), fill='red')
        self.c1.after(2000, lambda: self.c1.delete(message))
                

    def create_grid(self) -> None:
        self.c1.delete('all')
        for i in range(1,11):
            if i in (1,4,7,10):
                t = 5
            else:
                t = 1
            
            x = ((i*100) + 718)*self.scale
            y = ((i*100) + 128)*self.scale
            self.c1.create_line(x, 228*self.scale, x, 1128*self.scale, width=t)
            self.c1.create_line(818*self.scale, y, 1718*self.scale, y, width=t)
        self.c1.pack()
        self.main.update()

    def populate_grid(self, timer = False):
        self.inputs.clear()
        self.create_grid()
        if timer:
            self.timer_id = self.c1.create_window(1750*self.scale, 190*self.scale, window=self.timer)
        flat = self.current_puzzle.reshape((81,1))
        for i, item in enumerate(flat):
            x = ((i%9)*100 + 868) * self.scale
            y = (floor(i/9)*100 + 278) * self.scale
            if item == 0:
                entry = tk.Entry(self.c1, bg='white', bd = 1, highlightthickness=0, font=("Arial", round(40*self.scale)), width=round(2*self.scale), validate = 'key', validatecommand=self.validate, justify=CENTER)
                self.c1.create_window(x, y, window=entry)
                self.inputs.update({i:entry})
            else:
                self.c1.create_text(x, y, text=int(item[0]), anchor=CENTER, font=("Arial", round(40*self.scale)))

    def buttons(self):
        self.c1.create_window(1197*self.scale, 1200*self.scale, window=self.submit_button, anchor=NW)
        self.c1.create_window(868*self.scale, 150*self.scale, window=self.read_random_button, anchor=NW)
        self.c1.create_window(1168*self.scale, 150*self.scale, window=self.read_puzzle_input, anchor=NW)
        self.c1.create_window(1468*self.scale, 150*self.scale, window=self.gen_random_button, anchor=NW)
        

    def buttons_all(self):
        self.c1.create_window(1097*self.scale, 1200*self.scale, window=self.submit_button, anchor=NW)
        self.c1.create_window(868*self.scale, 150*self.scale, window=self.read_random_button, anchor=NW)
        self.c1.create_window(1168*self.scale, 150*self.scale, window=self.read_puzzle_input, anchor=NW)
        self.c1.create_window(1468*self.scale, 150*self.scale, window=self.gen_random_button, anchor=NW)
        self.c1.create_window(1297*self.scale, 1200*self.scale, window=self.computer_solve_button, anchor=NW)
        self.timer_id = self.c1.create_window(1750*self.scale, 190*self.scale, window=self.timer)
        self.start_stopwatch()
        
        

    def submit(self):
        p = self.current_puzzle.copy()
        p = p.reshape((81,1))
        match self.mode:
            case 'submit_solved':
                nope = False
                for i in self.inputs:
                    x = self.inputs[i].get()
                    print(x)
                    if x == '':
                        self.message('Please fill the entire grid!')
                        nope = True
                        break
                    else:
                        p[i] = x
                        print(x)
                if not nope and sudoku_solver().is_valid(p.reshape((9,9))):
                    self.current_puzzle = p.reshape((9,9))
                    self.populate_grid(True)
                    self.buttons()
                    self.message('Correct!')
                    self.stopwatch_running = False
                elif not nope:
                    self.message('Incorrect!')     
            case 'submit_unsolved':
                for i in self.inputs:
                    x = self.inputs[i].get()
                    if x == '':
                        p[i] = 0  
                    else:
                        p[i] = x
                try:
                    if not sudoku_solver().is_valid(p.reshape((9,9))):
                        self.message('The puzzle you have submitted is unsolvable!')
                    elif not sudoku_creator().single_solution(p.reshape(9,9)):
                        self.message('The puzzle you have submitted has multiple solutions! Please re-check it!')
                    else:
                        self.current_puzzle = p.reshape((9,9))
                        self.populate_grid()
                        self.mode = 'submit_solved'
                        self.buttons_all()
                except RuntimeError:
                    self.message('The puzzle you have submitted is unsolvable!')
                    self.mode = 'submit_unsolved'

    def update_pc_solve_confirmation(self):
        self.pc_solve_confirm = False

    def computer_solve(self):
        if self.pc_solve_confirm:
            self.current_puzzle = sudoku_solver().solve(self.current_puzzle)
            self.populate_grid()
            self.stopwatch_running = False
            self.timer_id = self.c1.create_window(1750*self.scale, 190*self.scale, window=self.timer)
            self.buttons()
            self.pc_solve_confirm = False
        else:
            self.pc_solve_confirm = True
            self.message("Press again to confirm.")
            self.c1.after(5000, self.update_pc_solve_confirmation)

    def gen_from_input(self):
        self.mode = 'submit_solved'
        self.populate_grid()
        self.buttons_all()
    
    def generate_puzzle(self):
        self.mode = 'submit_solved'
        self.current_puzzle = sudoku_creator().create_unsolved()
        self.populate_grid()
        self.buttons_all()
        
    def read_random_puzzle(self):
        self.mode = 'submit_solved'
        self.current_puzzle = sudoku_solver().read_puzzle('libraries/puzzles.csv', randint(2,1000))
        self.populate_grid()
        self.buttons_all()
        
    def input_puzzle(self):
        self.mode = 'submit_unsolved'
        self.current_puzzle = sudoku_creator().blank_puzzle()
        self.populate_grid()
        self.buttons()

    