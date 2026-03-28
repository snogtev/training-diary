"""
Custom Spinbox For CustomTkinter
Author : Sheikh Rashdan
Version : 1.4.1
"""

'''CHANGELOG:
 • 1.4:
    - Fixed scrollwheel interaction when widget was disabled. (Reported By : RaymondWK)
 • 1.4.1:
    - Added docstrings for functions.
    - Fixed enabling the widget using ".enable()".
    - Reorganized code.
'''

import customtkinter as ctk

class CTkSpinbox(ctk.CTkFrame):
    def __init__(self,
                 master: any,
                 width: int = 350,                            # width of the frame
                 height: int = 40,                            # height of the frame
                 start_value: float = 20,                        
                 min_value: float = 0,
                 max_value: float = 1000,
                 step_value: float = 1,
                 scroll_value: float = 5,
                 variable: any = None,
                 font: tuple = ('X', 20),
                 fg_color: str = None,
                 border_color: str = ('#AAA', '#555'),
                 text_color: str = ('Black', 'White'),
                 button_color: str = ('#BBB','#444'),
                 button_hover_color: str = ('#AAA', '#555'),
                 border_width: int = 2,
                 corner_radius: int = 5,
                 button_corner_radius: int = 5,
                 button_border_width: int = 2,
                 button_border_color: str = ('#AAA', '#555'),
                 state: str = 'normal',
                 command: any = None):
        super().__init__(master,
                         height = height,
                         width = width,
                         fg_color = fg_color,
                         border_color = border_color,
                         border_width = border_width,
                         corner_radius = corner_radius)

        # values
        self.start_value = max(min(start_value, max_value), min_value)       # start value must not exceed limits
        self.min_value = min_value
        self.max_value = max_value
        self.step_value = abs(step_value)
        self.scroll_value = abs(scroll_value)
        self.variable = variable
        if self.variable:
            self.variable.set(self.start_value)
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.button_corner_radius = button_corner_radius 
        self.button_border_width = button_border_width
        self.button_border_color = button_border_color
        self.state = state
        self.command = command

        # counter label 

        def validate_username(P):
            return P.endswith(' кг')
        self.num = self.start_value
        self.counter_var = str(self.num) + ' кг'
        vcmd = (self.register(validate_username), "%P")
        self.counter = ctk.CTkEntry(self,
                                    font = self.font, validate="key", validatecommand=vcmd,
                                    text_color = self.text_color)
        self.counter.insert(0, self.counter_var)
        self.counter.grid()
        self.counter.bind('<ButtonRelease-1>', lambda e: 
                          self.counter.icursor(len(self.counter.get()) - 3) 
                          if self.counter.index("insert") > len(self.counter.get()) - 3 
                          else None
        )




        # decrement button
        self.decrement = ctk.CTkButton(self,
                                       text = '-',
                                       font = self.font,
                                       text_color = self.text_color,
                                       fg_color = self.button_color,
                                       hover_color = self.button_hover_color,
                                       text_color_disabled = '#888',
                                       corner_radius = self.button_corner_radius,
                                       border_width = self.button_border_width,
                                       border_color = self.button_border_color,
                                       command = self.decrement_counter)

        # increment button
        self.increment = ctk.CTkButton(self,
                                       text = '+',
                                       font = self.font,
                                       text_color = self.text_color,
                                       fg_color = self.button_color,
                                       hover_color = self.button_hover_color,
                                       text_color_disabled = '#888',
                                       corner_radius = self.button_corner_radius,
                                       border_width = self.button_border_width,
                                       border_color = self.button_border_color,
                                       command = self.increment_counter)
        
        # grid
        self.rowconfigure(0, weight = 1, uniform = 'X')
        self.columnconfigure((0,2), weight = 11, uniform = 'X')
        self.columnconfigure(1, weight = 10, uniform = 'X')
        self.grid_propagate(False)

        # layout
        self.decrement.grid(row = 0, column = 0, sticky = 'news', padx = (4,0), pady = 4)
        self.counter.grid(row = 0, column = 1, sticky = 'news', padx = 0, pady = 4)
        self.increment.grid(row = 0, column = 2, sticky = 'news', padx = (0,4), pady = 4)

        # scroll bind
        self.bind('<MouseWheel>', self.scroll)

        # update state
        if self.state == 'disabled':
            self.disable()

    def decrement_counter(self):
        '''Decrements the value of the counter by the step value.'''
        self.num = float(self.counter.get()[:-3])
        self.num = self.num - self.step_value
        self.update_counter()

    def increment_counter(self):
        '''Increments the value of the counter by the step value.'''
        self.num = float(self.counter.get()[:-3])
        self.num = self.num + self.step_value
        self.update_counter()

    def scroll(self, scroll):
        '''Increments/Decrements the value of the counter by the scroll value depending on scroll direction.'''
        if self.state == 'normal':
            dirn = 1 if scroll.delta>0 else -1
            if dirn == -1: self.num = self.num - self.scroll_value
            else: self.num = self.num +self.scroll_value
            self.update_counter()

    def get(self):
        '''Returns the value of the counter.'''
        return self.num
    
    def set(self, value):
        '''Sets the counter to a particular value.'''
        self.num = (max(min(value, self.max_value), self.min_value))
    
    def disable(self):
        '''Disables the functionality of the counter.'''
        self.state = 'disabled'
        self.increment.configure(state = 'disabled')
        self.decrement.configure(state = 'disabled')

    def enable(self):
        '''Enables the functionality of the counter.'''
        self.state = 'normal'
        self.increment.configure(state = 'normal')
        self.decrement.configure(state = 'normal')

    def bind(self, key, function, add = True):
        '''binds a key to a function.'''

        super().bind(key, function, add)
        self.counter.bind(key, function, add)
        self.increment.bind(key, function, add)
        self.decrement.bind(key, function, add)

    def update_counter(self):
        '''Updates the counter variable and calls the counter command.'''

        self.limit_counter()
        if int(self.num) == self.num:
            self.num = int(self.num)
        if self.variable: self.variable = self.num
        if self.command: self.command(self.num)
        self.counter_var = f'{self.num} кг'
        self.counter.delete(0, len(self.counter.get()) - 3)
        self.counter.insert(0, self.num)
        


    def limit_counter(self):
        '''Limits the value of the counter within the minimum and maximum values.'''

        counter_value = self.num
        new_counter_value = max(min(counter_value, self.max_value), self.min_value)
        self.num = (new_counter_value)

    def configure(self, **kwargs):
        '''Update widget values.'''
        
        # conditions
        for value in ['font', 'text_color', 'button_color', 'button_hover_color', 'button_corner_radius', 'button_border_color', 'button_border_width']:
            if value in kwargs:
                new_value = kwargs.pop(value)
                if value not in ['font', 'button_corner_radius']:
                    if value not in ['button_hover_color', 'button_color', 'button_corner_radius']:
                        exec(f"self.counter.configure({value} = '{new_value}')")
                    value = {'button_color' : 'fg_color'}[value] if value in ['button_color', 'button_corner_radius'] else value
                    exec(f"self.increment.configure({value} = '{new_value}')")
                    exec(f"self.decrement.configure({value} = '{new_value}')")
                else:
                    value = {'button_corner_radius' : 'corner_radius'}[value] if value in ['button_color', 'button_corner_radius'] else value
                    exec(f"self.increment.configure({value} = {new_value})")
                    exec(f"self.decrement.configure({value} = {new_value})")
                    if value == 'font':
                        exec(f"self.counter.configure({value} = {new_value})")

        for value in ['min_value', 'max_value', 'step_value', 'scroll_value', 'variable']:
            if value in kwargs:
                new_value = kwargs.pop(value)
                exec(f'self.{value} = {new_value}')

        if 'command' in kwargs:
            self.command = kwargs.pop('command')
        elif 'state' in kwargs:
            self.state = kwargs.pop('state')
            if self.state == 'normal':
                self.enable()
            elif self.state == 'disabled':
                self.disable()

        super().configure(**kwargs)