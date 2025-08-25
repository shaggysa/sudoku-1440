try:
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.core.window import Window
    from kivy.metrics import sp
    from kivy.graphics import Color, Line, Rectangle
    from kivy.clock import Clock
except ImportError:
    print("Kivy is a necessary dependency. Please install it with pip to use the app.")

try:
    import lib_sudoku as sudoku
except ImportError:
    print("lib_sudoku is a necessary dependency. Please install it with pip to use the app.")
from copy import copy
from random import randint

Window.maximize()
Window.clearcolor = (1,1,1,1)

class Message(FloatLayout):
    def __init__(self, message:str, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.06)

        with self.canvas.before:
            Color(0.2, 0.7, 0.3, 1)
            self.rect = Rectangle()

        self.bind(pos=self.update_rect, size=self.update_rect)
        
        self.label = Label(text=message, halign="center", valign="middle", color = (1,1,1,1))
        self.add_widget(self.label)
    
    def update_rect(self, *args):
        pos_x, pos_y = self.pos
        self.rect.pos = (pos_x*1.26, pos_y * 0.958)
        self.label.pos = (pos_x * 0.623, pos_y * 0.94)
        x, y = self.size 
        self.rect.size = (x*0.32, y*0.6)
        self.label.size = (x*0.65, y*0.7)
        self.label.font_size = self.height*0.4
        

class ResizingLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_font_size)
    
    def update_font_size(self, *args):
        self.font_size = self.height * 0.67

class OneDigitInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False

    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 1 and not from_undo:
            self.text = ''
        if substring.isdigit():
            return super().insert_text(substring, from_undo)
        return

    def on_text_change(self, instance, value:int):
        if len(value) > 1:
            self.text = value[-1]
    def update_border(self, instance):
        pass


class GridCell(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size = self.update_font_size)
        self.setup_cell()
        self.is_markdown_mode = False
    
    def setup_cell(self):
        
        self.main_input = OneDigitInput(multiline=False, size_hint=(1.2, 1.2), pos_hint={'center_x': 0.5, 'center_y': 0.325}, background_color = (0,0,0,0), halign = 'center', padding = [0,0,0,0], border = (0,0,0,0))

        self.markdown_input = TextInput(multiline=True, size_hint=(.95, .95), pos_hint={'center_x': 0.5, 'center_y': 0.5}, disabled = True, halign = 'right', background_color = (0,0,0,0), padding = [0,0,0,0], border = (0,0,0,0))
        
        self.add_widget(self.markdown_input)    
        self.add_widget(self.main_input)
        
    def update_text_size(self, instance, size):
        instance.text_size = size    
    
    def update_font_size(self, *args):
        cell_height = self.height
        self.main_input.font_size = cell_height * 0.69
        self.markdown_input.font_size = cell_height * .24

    def toggle_mode(self):
        self.is_markdown_mode =  not self.is_markdown_mode
        if self.is_markdown_mode:
            x = self.main_input.focus
            self.main_input.disabled = True
            self.main_input.opacity = 0.7
            self.markdown_input.disabled = False
            self.markdown_input.opacity = 1.0
            if x:
                self.markdown_input.unfocus_on_touch = False
                self.markdown_input.focus = True
                Clock.schedule_once(lambda dx: setattr(self.markdown_input, 'unfocus_on_touch', True), 2)
        else:
            x = self.markdown_input.focus
            self.main_input.disabled = False
            self.main_input.opacity = 1.0
            self.markdown_input.disabled = True
            self.markdown_input.opacity = 0.7
            if x:
                self.main_input.unfocus_on_touch = False
                self.markdown_input.focus = False
                self.main_input.focus = True
                Clock.schedule_once(lambda dx: setattr(self.main_input, 'unfocus_on_touch', True), 2)

class SudokuGrid(GridLayout):
    def __init__(self, puzzle:list, **kwargs):
        super().__init__(**kwargs)
        self.puzzle = puzzle
        self.cells = {}
        for i, num in enumerate(puzzle):
            if num == 0:
                widget = GridCell()
                self.cells.update({i:widget})
            else:
                widget = ResizingLabel(text=str(num), color = (1,0.2,0.2,1), size_hint_x = .5, size_hint_y = .5, valign = 'top', font_size = '69dp')
            self.add_widget(widget)
        self.bind(pos = self.update_lines, size = self.update_lines)
        self.update_lines()


    def toggle_markdown(self):
        for i in self.cells:
            self.cells[i].toggle_mode()
    
    def read_filled_puzzle(self):
        filled_puzzle = copy(self.puzzle)
        for i in self.cells:
            x = self.cells[i].main_input.text
            if x == '':
                filled_puzzle[i] = 0
            else:
                filled_puzzle[i] = int(x)
        return filled_puzzle
            
    
    def update_lines(self, *args):
        screen_width, screen_height = Window.size
        self.size_hint = (.75*(screen_height/screen_width),.75)
        self.canvas.after.clear()
        with self.canvas.after:
            Color(0, 0, 0, 1)
            x, y = self.pos
            w, h = self.size
            rows, cols = self.rows, self.cols
            dx = w / cols
            dy = h / rows

            for i in range(cols+1):
                match i:
                    case 0 | 3 | 6 | 9:
                        width = 2.25
                    case _:
                        width = 1.5
                Line(points=[x + i * dx, y, x + i * dx, y + h], width=width)

            for i in range(rows+1):
                match i:
                    case 0 | 3 | 6 | 9:
                        width = 2.25
                    case _:
                        width = 1.5
                Line(points=[x, y + i * dy, x + w, y + i * dy], width=width)

class SudokuApp(App):
    def build(self):
        self.pc_solve_confirm = False
        self.clock_running = False
        self.clock_scheduler = Clock.schedule_once(lambda dt: self.reset_pc_solve, 1)
        self.clock_widget = Label(size_hint = (0.1,0.1), pos_hint = {'center_x':0.98, 'center_y':0.98}, color = (0,0,0,1), font_size = sp(16), halign = 'left')
        self.csv_puzzles = sudoku.PuzzleReader("https://raw.githubusercontent.com/shaggysa/lib_sudoku/master/puzzles.csv", True)
        self.puzzle = []
        self.main_layout = FloatLayout(size_hint = (1,1), pos_hint = {'center_x':0.5, 'center_y':0.5})
        self.build_empty(None)
        return self.main_layout
    
    def display_clock_time(self):
        self.clock_widget.text = f'{self.clock_time//60}:{self.clock_time%60}'
    
    def start_clock(self):
        self.clock_scheduler.cancel()
        self.clock_time = 0
        self.clock_running = True
        self.clock_widget.text = '0:00'
        self.clock_scheduler = Clock.schedule_once(lambda dt: self.update_clock(), 1)

    def update_clock(self):
        if self.clock_running:
            self.clock_time += 1
            x = self.clock_time%60
            if len(str(x)) == 1:
                j = '0' + str(x)
            else:
                j = x
            self.clock_widget.text = f'{self.clock_time//60}:{j}'
            self.clock_scheduler = Clock.schedule_once(lambda dt: self.update_clock(), 1)
    
    def clear(self, instance):
        self.main_layout.clear_widgets()

    def top_buttons(self):
        button_bar_1 = BoxLayout(orientation = 'horizontal', size_hint_y = 0.2, pos_hint = {'center_x':0.5, 'center_y':1}, padding = 0)
        read_csv_button = Button(text = 'read random puzzle from file', size_hint = (0.1, 0.3), on_press = self.read_random)
        input_puzzle_button = Button(text = 'input your own puzle', size_hint = (0.1, 0.3), on_press = self.build_empty)
        generate_puzzle_button = Button(text = 'generate a random puzzle', size_hint = (0.1, 0.3), on_press = self.gen_random)
        button_bar_1.add_widget(read_csv_button)
        button_bar_1.add_widget(input_puzzle_button)
        button_bar_1.add_widget(generate_puzzle_button)
        return button_bar_1
    
    def bottom_buttons_submit_unsolved(self):
        button_bar_2 = BoxLayout(orientation = 'horizontal', size_hint_y = 0.2, pos_hint = {'center_x':0.5, 'center_y':0.135})
        submit_button = Button(text = 'Submit!', size_hint = (0.1, 0.3), on_press = self.submit_unsolved)
        button_bar_2.add_widget(submit_button)
        return button_bar_2
    
    def bottom_button_submit_solved(self):
        self.clock_running = False
        button_bar_2 = BoxLayout(orientation = 'horizontal', size_hint_y = 0.2, pos_hint = {'center_x':0.5, 'center_y':0.135})
        markdown_button = Button(text = 'toggle note-taking mode', size_hint = (0.1, 0.3), on_press = self.toggle_markdown)
        submit_button = Button(text = 'Submit!', size_hint = (0.1, 0.3), on_press = self.submit_solved)
        computer_solve_button = Button(text = 'solve with computer', size_hint = (0.1, 0.3), on_press = self.computer_solve)
        button_bar_2.add_widget(markdown_button)
        button_bar_2.add_widget(submit_button)
        button_bar_2.add_widget(computer_solve_button)
        return button_bar_2
    
    def toggle_markdown(self, instance):
        self.grid.toggle_markdown()
    
    def submit_unsolved(self, instance):
        puzz = self.grid.read_filled_puzzle()
        if sudoku.is_valid(puzz):
            self.build_to_solve()
        else:
            self.message('The puzzle isn\'t valid!')
    
    def submit_solved(self, instance):
        puzz = self.grid.read_filled_puzzle()
        if sudoku.is_valid(puzz):
            if 0 in puzz:
                self.message('Please fill the entire grid!')
            else:
                self.puzzle = puzz
                self.build_filled()
                self.message('Correct!')
        else:
            self.message('Incorrect!')
            
    def computer_solve(self, instance):
        if self.pc_solve_confirm:
            self.puzzle = sudoku.solve(self.puzzle)
            self.build_filled()
        else:
            self.message('Press again to confirm.')
            self.pc_solve_confirm = True
            Clock.schedule_once(self.reset_pc_solve, 3)
    
    def reset_pc_solve(self, instance):
        self.pc_solve_confirm = False
    
    def build_empty(self, instance):
        self.puzzle = [0] * 81
        self.main_layout.clear_widgets()
        self.grid = SudokuGrid(puzzle=self.puzzle, pos_hint = {'center_x':0.5, 'center_y':0.5}, cols = 9, rows = 9)
        self.main_layout.add_widget(self.grid)
        self.main_layout.add_widget(self.top_buttons())
        self.main_layout.add_widget(self.bottom_buttons_submit_unsolved())
        
    def build_filled(self):
        self.clock_running = False
        self.pc_solve_confirm = False
        self.main_layout.clear_widgets()
        self.grid = SudokuGrid(puzzle=self.puzzle, pos_hint = {'center_x':0.5, 'center_y':0.5}, cols = 9, rows = 9)
        self.main_layout.add_widget(self.grid)
        self.main_layout.add_widget(self.top_buttons())
        self.main_layout.add_widget(self.clock_widget)
    
    def build_to_solve(self):
        self.main_layout.clear_widgets()
        self.grid = SudokuGrid(puzzle=self.puzzle, pos_hint = {'center_x':0.5, 'center_y':0.5}, cols = 9, rows = 9)
        self.main_layout.add_widget(self.grid)
        self.main_layout.add_widget(self.top_buttons())
        self.main_layout.add_widget(self.bottom_button_submit_solved())
        self.main_layout.add_widget(self.clock_widget)
        self.start_clock()
    
    def message(self, text):
        overlay = Message(text, pos_hint = {'x':0.32, 'y':0.5})
        self.main_layout.add_widget(overlay)
        Clock.schedule_once(lambda dt: self.main_layout.remove_widget(overlay), 2)
        
    def read_random(self, instance):
        self.puzzle = list(self.csv_puzzles.get_unsolved_puzz(randint(2,1001)))
        self.build_to_solve()
    
    def gen_random(self, instance):
        self.puzzle = list(sudoku.gen_unsolved(randint(24,36)))
        self.build_to_solve()
        self.build_to_solve()

