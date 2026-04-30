import customtkinter as ctk
from CTkTable import CTkTable
from CTkDatePicker import CTkDatePicker
from ctkspinbox import CTkSpinbox
from CTkScrollableDropdown import *
from CTkMessagebox import CTkMessagebox
import sqlite3
from CTkXYFrame import CTkXYFrame

connection = sqlite3.connect('trainings.db')
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
weight REAL,
sets INTEGER,
reps INTEGER,
FOREIGN KEY (workout_id) REFERENCES workouts (id)
)         
''')

connection.commit()

ctk.FontManager.load_font('Russo One.ttf')

BLACK_COLOR = '#2b2b2b'
BLUE_COLOR = '#1f538d'

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
                        {'text': 'Мои тренировки', 'command': lambda: navigate('view')},
                        {'text': 'Мои цели'}]
        
        self.tabview = ctk.CTkTabview(self, width=800, height=600)
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

        self.navigate = navigate

        self.values = ('Жим лёжа', 'Присед', 'Становая тяга')
        self.columns = ('Упражнение', 'Вес', 'Подходы', 'Повторения')

        self.window_training_form = None 
        self.table = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) 
 
        self.setup_ui()
    
    def setup_ui(self):
        self.button_add = ctk.CTkButton(self, text='Добавить упражнение', command=self.add_exercise, font=FONT_LARGE)
        self.button_back = ctk.CTkButton(self, text='Назад', command=self.go_back, font=FONT_LARGE)
        self.button_save = ctk.CTkButton(self, text='Сохранить', command=self.save_training, font=FONT_LARGE)

        self.label_date = ctk.CTkLabel(self, text='Дата:', font=FONT_LARGE)
        self.label_no_exercises = ctk.CTkLabel(self, text='Упражнений ещё нет!', font=HUGE_FONT)
        self.table_frame = CTkXYFrame(self, height=300, width=800, fg_color=BLACK_COLOR)
        self.calendar = CTkDatePicker(self)
        self.calendar.set_localization('ru_RU.UTF-8')

        self.button_add.grid(row=3, column=0, pady=15, padx=50)
        self.button_back.grid(row=4, column=0, pady=15, padx=50)
        self.button_save.grid(row=5, column=0, pady=15, padx=50, sticky='s')

        self.label_date.grid(row=0, column=0, padx=25, pady=20, sticky='nw')
        self.label_no_exercises.grid(row=1, column=0)
        self.calendar.grid(row=0, column=0, pady=20, padx=150, sticky='nw')


    def add_exercise(self):
        if self.table is None:
            self.table_frame.grid(row=1, column=0, sticky='ew')
            self.table_frame.grid_columnconfigure(0, weight=1)

        self.table = CTkTable(self.table_frame,font=FONT_LARGE, header_color=BLUE_COLOR, values=[self.columns])
        self.table.grid(row=0, column=0)
            
        if self.window_training_form is None or not self.window_training_form.winfo_exists():
            self.window_training_form = ctk.CTkToplevel()
            self.window_training_form .resizable(False, False)
            self.window_training_form.title('Упражнение')
            self.window_training_form.geometry('650x400')

            self.spinbox_weight = CTkSpinbox(self.window_training_form, unit=' ' + UNIT, step_value=WEIGHT_STEP, font=FONT_LARGE)
            self.spinbox_sets = CTkSpinbox(self.window_training_form, start_value=3, font=FONT_LARGE)
            self.spinbox_reps = CTkSpinbox(self.window_training_form,  start_value=8, font=FONT_LARGE)

            self.spinbox_weight.grid(row=1, column=0, sticky='nw', padx=250, pady=5)
            self.spinbox_sets.grid(pady=5)
            self.spinbox_reps.grid(pady=5)

            self.optionmenu = ctk.CTkComboBox(self.window_training_form, font=FONT_LARGE, width=300)
            self.window_training_form.after(1, self.optionmenu.focus)
            self.button_more = ctk.CTkButton(self.window_training_form, text='Ещё', command=lambda: self.add_next_exercise(save=False), font=FONT_LARGE)
            self.button_done = ctk.CTkButton(self.window_training_form, text='Завершить', command=lambda: self.add_next_exercise(save=True), font=FONT_LARGE)

            self.optionmenu.grid(row=0, column=0, sticky='nw', padx=250)
            self.button_more.grid(pady=100, padx=250, sticky='sw')
            self.button_done.grid(row=4, column=0, sticky='nw', padx=25)

            def insert_method(e):
                self.optionmenu.set(e)
            CTkScrollableDropdown(self.optionmenu, values=self.values, font=FONT_MEDIUM, command=lambda e: insert_method(e), autocomplete=True)
            self.optionmenu.set('')
            self.window_training_form.wm_attributes('-topmost', 1)
            for i, buttons in enumerate(self.columns):
                ctk.CTkLabel(self.window_training_form, text=buttons + ':', font=FONT_LARGE).grid(row=i, column=0, sticky='nw', padx=25)

    def add_next_exercise(self, save):
        if self.optionmenu.get() == '':
            CTkMessagebox(self.window_training_form, title='Ошибка', message='Введите название упражнения!', icon='cancel', font=FONT_LARGE)
            return
        if self.spinbox_weight.get().replace(' ', '') == '':
            CTkMessagebox(self.window_training_form, title='Ошибка', message='Введите вес!', icon='cancel', font=FONT_LARGE)
            return
        if self.spinbox_sets.get().replace(' ', '') == '':
            CTkMessagebox(self.window_training_form, title='Ошибка', message='Введите подходы!', icon='cancel', font=FONT_LARGE)
            return
        if self.spinbox_reps.get().replace(' ', '') == '':
            CTkMessagebox(self.window_training_form, title='Ошибка', message='Введите повторения!', icon='cancel', font=FONT_LARGE)
            return
        self.table.add_row(index=self.table.rows, values='')
        self.table.insert(row=self.table.rows-1, column=0, value=self.optionmenu.get().strip())
        self.table.insert(row=self.table.rows-1, column=1, value=self.spinbox_weight.get().strip())
        self.table.insert(row=self.table.rows-1, column=2, value=self.spinbox_sets.get().strip())
        self.table.insert(row=self.table.rows-1, column=3, value=self.spinbox_reps.get().strip())
        self.window_training_form.destroy() 
        self.window_training_form = None
        self.label_no_exercises.grid_remove()
        if save == False:
            self.add_exercise()

    def save_training(self):
        cursor.execute('SELECT id FROM workouts WHERE date = ?', [self.calendar.get_date()])
        result = cursor.fetchone()
        if self.table is None or not self.table.winfo_exists():
            CTkMessagebox(self.window_training_form, title='Ошибка', message='Нельзя сохранить пустую тренировку!', icon='cancel', font=FONT_LARGE)
        elif result is not None:
            CTkMessagebox(title='Ошибка', message='Тренировка за данное число уже существует!', icon='cancel', font=FONT_LARGE)
        else:
            table_data = self.table.get()
            calendar_data = self.calendar.get_date()
            cursor.execute('INSERT INTO workouts (date) VALUES (?)', [calendar_data])
            current_workout_id = cursor.lastrowid
            for i in range(len(table_data)):
                table_data[i].insert(0, current_workout_id)
            cursor.executemany('INSERT INTO exercises (workout_id, exercise, weight, sets, reps) VALUES (?, ?, ?, ?, ?)', table_data[1:])
            connection.commit()
            CTkMessagebox(message='Тренировка успешно добавлена!', title='Успех', icon='check', option_1='ОК', font=FONT_LARGE)
        self.table.grid_remove()
        self.table_frame.grid_remove()
        self.table = None
        self.window_training_form = None
        self.setup_ui()
    
    def go_back(self):
        if self.table is not None:
            msg = CTkMessagebox(title='Выход', message='Сохранить тренировку?', icon='question', option_1='Отмена', option_2='Нет', option_3='Да', font=FONT_LARGE)
            response = msg.get()
            if response == 'Да':
                self.save_training()
            else:
                self.table.grid_remove()
                self.table_frame.grid_remove() 
            self.table = None
            self.window_training_form = None
            self.navigate('menu')
            self.label_no_exercises.grid()
            self.table = None
        else:
            self.navigate('menu')

class MyTrainings(ctk.CTkFrame):
    def __init__(self, master, navigate, **kwargs):
        super().__init__(master, **kwargs)
        self.navigate = navigate

        self.date = ''
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 

        self.setup_ui()
    
    def setup_ui(self):
            self.button_back = ctk.CTkButton(self, text='Назад', command=lambda: self.navigate('menu'), font=FONT_LARGE)
            self.table_frame = CTkXYFrame(self, height=600, width=800, fg_color=BLACK_COLOR)

            self.button_back.grid(row=1, column=0, pady=15, padx=50, sticky='s')
            self.table_frame.grid(row=0)


            cursor.execute('''SELECT
                           strftime('%d.%m.%Y', date),
                           exercise,
                           weight,
                           sets,
                           reps
                           FROM workouts
                           JOIN exercises
                           ON workouts.id = workout_id
                           ORDER BY date DESC
                           ''')
            rows = cursor.fetchall()
            
            if rows:
                for i in range (len(rows)):
                    if rows[i][0] != self.date:
                        self.date = rows[i][0]
                        counter = 1
                        self.training_frame = ctk.CTkFrame(self.table_frame, corner_radius=15, width=500, fg_color=BLUE_COLOR)
                        self.training_frame.grid(pady=15, ipady=10, ipadx=10)
                        self.training_frame.grid_columnconfigure(0, weight=1)
                        self.label_date = ctk.CTkLabel(self.training_frame, text=f'Дата: {rows[i][0]}', font=FONT_LARGE)
                        self.label_date.grid(pady=15)
                    self.label_exercises = ctk.CTkLabel(self.training_frame, text=f'{counter}) {" x ".join(map(str, rows[i][1:]))}', font=FONT_LARGE)
                    self.label_exercises.grid(padx=20, sticky='w')
                    counter += 1

class App(ctk.CTk):
    def __init__(self):
        
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.frames = {'menu':MainMenu(self, navigate=self.new_frame),
                       'add': AddTraining(self, navigate=self.new_frame),
                       'view': MyTrainings(self, navigate=self.new_frame)}
                
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
                       
        self.new_frame('menu')

    def new_frame(self, frame_name):
        self.frames[frame_name].tkraise()

app = App()
app.title('Дневник тренировок')
app.geometry('900x650')
ctk.set_appearance_mode('Dark')
app.resizable(False, False)
app.mainloop()