import customtkinter as ctk
from CTkTable import CTkTable
from CTkDatePicker import CTkDatePicker
from ctkspinbox import CTkSpinbox
from CTkScrollableDropdown import *
from CTkMessagebox import CTkMessagebox
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS workouts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT
)         
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS exercises (
id INTEGER PRIMARY KEY AUTOINCREMENT,
workout_id INTEGER,
exercise TEXT,
sets INTEGER,
weight REAL,
reps INTEGER,
FOREIGN KEY (workout_id) REFERENCES workouts (id)
)         
''')

connection.commit()

ctk.FontManager.load_font('Russo One.ttf')

HUGE_FONT = ('Russo One', 35)
FONT_LARGE = ('Russo One', 25)
FONT_MEDIUM = ('Russo One', 22)
FONT_SMALL = ('Russo One', 18)

WEIGHT_STEP = 2.5
DEFAULT_STEP = 1
UNIT = 'кг'

class MainMenu(ctk.CTkFrame):
    def __init__(self, master, navigate, **kwargs):
        super().__init__(master, **kwargs)
        
        self.tabs = ('Тренировки', 'Статистика', 'Профиль', 'Настройки', 'Помощь')
        
        self.buttons = [{'text': 'Добавить тренировку', 'command': lambda: navigate('add')},
                        {'text': 'Мои тренировки'},
                        {'text': 'Мои цели'}]
        
        self.tabview = ctk.CTkTabview(self, width=700, height=550)
        self.tabview.grid(row=0, column=0, padx=20, pady=20)
        
        for tab in self.tabs:
            self.tabview.add(tab)
        self.tabview._segmented_button.configure(font=FONT_MEDIUM)

        self.tabview.tab('Тренировки').grid_columnconfigure(0, weight=1)
        for i, btn_data in enumerate(self.buttons):
            ctk.CTkButton(self.tabview.tab('Тренировки'), **btn_data, font=FONT_LARGE).grid(row=i, pady=15, padx=50, sticky='ew')

class AddTraining(ctk.CTkFrame):
    def __init__(self, master, navigate, **kwargs):
        super().__init__(master, **kwargs)
        self.training_form = None
        self.tabling = None
        self.row_counter = 1
        self.navigate = navigate
        self.columns = ('Упражнение', 'Вес', 'Подходы', 'Повторения')
        
        self.buttons = [{'text': 'Добавить упражнение', 'command': self.add_exercise},
                        {'text': 'Назад', 'command': self.hfdffhf},
                        {'text': 'Сохранить', 'command': self.save_training, 'sticky': 's'}]
        
        self.values = ('Жим лёжа', 'Присед', 'Становая тяга')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) 
 
        self.setup_ui()

    def hfdffhf(self):
        if self.row_counter > 1:
            msg = CTkMessagebox(title='Выход', message='Сохранить тренировку?', icon='question', option_1='Отмена', option_2='Нет', option_3='Да', font=FONT_LARGE)
            response = msg.get()
            self.navigate('menu')
            self.table.delete_rows(range(1, self.row_counter))
            self.table.grid_remove()
            self.dffg.grid()
            self.row_counter = 1
        else:
            self.navigate('menu')

    def add_exercise(self):
        if self.tabling is None:
            self.table = CTkTable(self, font=FONT_LARGE, header_color = '#1f538d', values=[self.columns])
            self.tabling = True

        if self.training_form is None:
            self.training_form = ctk.CTkToplevel()
            self.training_form.title('Упражнение')
            self.training_form.geometry('650x400')
            self.spinbox = CTkSpinbox(self.training_form, unit=' ' + UNIT, step_value=WEIGHT_STEP, font=FONT_LARGE)
            self.spinbox.grid(row=1, column=0, sticky='nw', padx=250, pady=5)
            self.spinbox2 = CTkSpinbox(self.training_form, start_value=3, font=FONT_LARGE)
            self.spinbox2.grid(pady=5)
            self.spinbox3 = CTkSpinbox(self.training_form,  start_value=8, font=FONT_LARGE)
            self.spinbox3.grid(pady=5)
            self.optionmenu = ctk.CTkComboBox(self.training_form, font=FONT_LARGE, width=300)
            self.optionmenu.grid(row=0, column=0, sticky='nw', padx=250)
            self.training_form.after(1, self.optionmenu.focus)
            self.fij = ctk.CTkButton(self.training_form, text='Ещё', command=lambda: self.add_new_exercise(save=False), font=FONT_LARGE)
            self.fij.grid(pady=100, padx=250, sticky='sw')
            self.fiefj = ctk.CTkButton(self.training_form, text='Завершить', command=lambda: self.add_new_exercise(save=True), font=FONT_LARGE)
            self.fiefj.grid(row=4, column=0, sticky='nw', padx=25)

            def insert_method(e):
                self.optionmenu.set(e)
            CTkScrollableDropdown(self.optionmenu, values=self.values, command=lambda e: insert_method(e), autocomplete=True)
            self.optionmenu.set('')
            self.training_form.wm_attributes('-topmost', 1)
            for i, buttons in enumerate(self.columns):
                ctk.CTkLabel(self.training_form, text=buttons + ':', font=FONT_LARGE).grid(row=i, column=0, sticky='nw', padx=25)

    def add_new_exercise(self, save):
        if self.optionmenu.get() == '':
            CTkMessagebox(self.training_form, title='Ошибка', message='Введите название упражнения!', icon='cancel', font=FONT_LARGE)
            return
        self.table.add_row(index=self.row_counter, values='')
        self.table.insert(row=self.row_counter, column=0, value=self.optionmenu.get())
        self.table.insert(row=self.row_counter, column=1, value=self.spinbox.get())
        self.table.insert(row=self.row_counter, column=2, value=self.spinbox2.get())
        self.table.insert(row=self.row_counter, column=3, value=self.spinbox3.get())
        self.row_counter += 1
        self.training_form.destroy() 
        self.training_form = None
        self.dffg.grid_remove()
        self.table.grid(row=2)
        if save == False:
            self.add_exercise()

    def setup_ui(self):
        for i, btn_data in enumerate(self.buttons, start=2):
            fjnf = btn_data.copy()
            jfjf = fjnf.pop('sticky', 'n')
            ctk.CTkButton(self, **fjnf, font=FONT_LARGE).grid(row=i, column=0, sticky=jfjf, pady=15, padx=50)
        ctk.CTkLabel(self, text='Дата:', font=FONT_LARGE).grid(row=0, column=0, padx=25, pady=20, sticky='nw')
        self.dffg = ctk.CTkLabel(self, text='Упражнений ещё нет!', font=HUGE_FONT)
        self.dffg.grid(row=1, column=0, sticky='new')


        self.calendar = CTkDatePicker(self)
        self.calendar.set_localization("ru_RU.UTF-8")
        self.calendar.grid(row=0, column=0, padx=150, pady=20, sticky='nw')

    def save_training(self):
        ffff = self.table.get()
        ffffff = self.calendar.get_date()
        print(ffff)
        cursor.execute('INSERT INTO workouts (date) VALUES (?)', [ffffff])
        current_workout_id = cursor.lastrowid
        for i in range(len(ffff)):
            ffff[i].insert(0, current_workout_id)

        cursor.executemany('INSERT INTO exercises (workout_id, exercise, sets, weight, reps) VALUES (?, ?, ?, ?, ?)', ffff[1:])


        connection.commit()


class App(ctk.CTk):
    def __init__(self):
        
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.frames = {'menu':MainMenu(self, navigate=self.new_frame),
                       'add': AddTraining(self, navigate=self.new_frame)}
                
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
                       
        self.new_frame('menu')

    def new_frame(self, frame_name):
        self.frames[frame_name].tkraise()

app = App()
app.title('Дневник тренировок')
app.geometry('800x600')
ctk.set_appearance_mode('Dark')
app.resizable(False, False)
app.mainloop()