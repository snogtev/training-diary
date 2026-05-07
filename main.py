import sqlite3
import webbrowser
from datetime import datetime

import customtkinter as ctk
from CTkDatePicker import CTkDatePicker
from CTkMessagebox import CTkMessagebox
from CTkScrollableDropdown import CTkScrollableDropdown
from ctksidebar import CTkSidebarNavigation
from ctkspinbox import CTkSpinbox
from CTkTable import CTkTable
from CTkXYFrame import CTkXYFrame

ctk.FontManager.load_font('Russo One.ttf')

DB_NAME = 'trainings.db'
REPO_URL = 'https://github.com/snogtev/training-diary'
FONT_FAMILY = 'Russo One'

TEXT_ABOUT = (
       'Программа разработана в рамках индивидуального проекта по дисциплине «ОУП.08 Информатика».\n\n'
       'Автор: Ногтев Степан Вячеславович, студент 1 курса группы ИСиП-2-9-25 ГАПОУ НСО «НКПиИТ».\n\n'
        'Руководитель: Груздев Евгений Александрович, преподаватель первой квалификационной категории.\n\n'
        'Технологии разработки: Python, SQLite3 и CustomTkinter (включая сторонние библиотеки).\n\n'
        'Проект имеет открытый исходный код и доступен в репозитории на '
        )

TABLE_HEADERS = ('Упражнение', 'Вес', 'Подходы', 'Повторения')
EXERCISE_LIST = ('Жим лёжа', 'Присед', 'Становая тяга')
DAYS_OF_THE_WEEK = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')

BLACK_COLOR = '#242424'
BLUE_COLOR = '#1f538d'

HUGE_FONT = (FONT_FAMILY, 35)
FONT_LARGE = (FONT_FAMILY, 25)
FONT_MEDIUM = (FONT_FAMILY, 22)
FONT_SMALL = (FONT_FAMILY, 18)

WEIGHT_STEP = 2.5
DEFAULT_STEP = 1
UNIT = 'кг'

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS workouts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT,
is_draft INTEGER
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

class AddTraining(ctk.CTkFrame):
    def __init__(self, master, history_page, drafts_page, **kwargs):
        super().__init__(master, fg_color=BLACK_COLOR, **kwargs)
        self.history_page = history_page
        self.drafts_page = drafts_page
        
        self.window_training_form = None 
        self.table = None
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) 
 
        self.setup_ui()
    
    def setup_ui(self):
        self.label_date = ctk.CTkLabel(self, text='Дата:', font=FONT_LARGE)
        self.label_date.grid(row=0, column=0, padx=25, pady=20, sticky='e')
        self.calendar = CTkDatePicker(self)
        self.calendar.set_localization('ru_RU.UTF-8')
        self.calendar.grid(row=0, column=1, pady=20, sticky='w')

        self.label_no_exercises = ctk.CTkLabel(self, text='Упражнений ещё нет!', font=HUGE_FONT)
        self.label_no_exercises.grid(row=1, column=0, columnspan=4, sticky='nsew')
        self.table_frame = CTkXYFrame(self, height=500, width=800, fg_color=BLACK_COLOR)

        self.button_add = ctk.CTkButton(self, text='Добавить упражнение', command=self.add_exercise, font=FONT_LARGE)
        self.button_add.grid(row=2, column=0, pady=15, padx=50, columnspan=4, sticky='nsew')

        self.button_save = ctk.CTkButton(self, text='Сохранить', command=self.save_to_db, font=FONT_LARGE)
        self.button_save.grid(row=3, column=0, columnspan=2, pady=15, padx=50, sticky='ew')

        self.button_save = ctk.CTkButton(self, text='Сохранить как черновик', command=self.save_as_draft, font=FONT_LARGE)
        self.button_save.grid(row=3, column=3, pady=15, padx=50, sticky='ew')

    def save_to_db(self):
        self.save_training(is_draft=0)

    def save_as_draft(self):
        self.save_training(is_draft=1)

    def add_exercise(self):
        if self.table is None:
            self.table_frame.grid(row=1, column=0, columnspan=4, sticky='nsew')
            self.table = CTkTable(self.table_frame,font=FONT_LARGE, header_color=BLUE_COLOR, values=[TABLE_HEADERS])
            self.table.grid()
            
        if self.window_training_form is None or not self.window_training_form.winfo_exists():
            self.window_training_form = ctk.CTkToplevel()
            self.window_training_form .resizable(False, False)
            self.window_training_form.title('Упражнение')
            self.window_training_form.geometry('650x350')

            self.window_training_form.grid_columnconfigure(0, weight=0)
            self.window_training_form.grid_columnconfigure(1, weight=1)
            self.window_training_form.grid_rowconfigure(4, weight=1)

            self.spinbox_weight = CTkSpinbox(self.window_training_form, unit=' ' + UNIT, step_value=WEIGHT_STEP, font=FONT_LARGE)
            self.spinbox_sets = CTkSpinbox(self.window_training_form, start_value=3, font=FONT_LARGE)
            self.spinbox_reps = CTkSpinbox(self.window_training_form,  start_value=8, font=FONT_LARGE)

            self.spinbox_weight.grid(row=1, column=1, pady=5, sticky='w')
            self.spinbox_sets.grid(row=2, column=1, pady=5, sticky='w')
            self.spinbox_reps.grid(row=3, column=1, pady=5, sticky='w')

            self.optionmenu = ctk.CTkComboBox(self.window_training_form, font=FONT_LARGE, width=300)
            self.window_training_form.after(1, self.optionmenu.focus)
            self.button_more = ctk.CTkButton(self.window_training_form, text='Ещё', command=lambda: self.add_next_exercise(save=False), font=FONT_LARGE)
            self.button_done = ctk.CTkButton(self.window_training_form, text='Завершить', command=lambda: self.add_next_exercise(save=True), font=FONT_LARGE)

            self.optionmenu.grid(row=0, column=1, pady=5, sticky='w')
            self.button_more.grid(row=5, column=0, columnspan=2, pady=5, padx=25, sticky='nsew')
            self.button_done.grid(row=6, column=0, pady=15, padx=25, columnspan=2, sticky='nsew')

            def insert_method(e):
                self.optionmenu.set(e)
            CTkScrollableDropdown(self.optionmenu, values=EXERCISE_LIST, font=FONT_MEDIUM, command=lambda _: insert_method(_), autocomplete=True)
            self.optionmenu.set('')
            self.window_training_form.wm_attributes('-topmost', 1)
            for i, buttons in enumerate(TABLE_HEADERS):
                ctk.CTkLabel(self.window_training_form, text=buttons + ':', font=FONT_LARGE).grid(row=i, column=0, sticky='w', padx=25)

    def add_next_exercise(self, save):
        self.errors = {'название упражнения': self.optionmenu.get(),
                  'вес': self.spinbox_weight.get().replace(' ', ''),
                  'количество подходов': self.spinbox_sets.get().replace(' ', ''),
                  'количество повторений': self.spinbox_reps.get().replace(' ', '')}
        
        for key, value in self.errors.items():
            if value == '':
                CTkMessagebox(self.window_training_form, title='Ошибка', message=f'Введите {key}!', icon='cancel', font=FONT_LARGE)
                return
            
        self.columns = [self.optionmenu.get().strip(), self.spinbox_weight.get().strip(), self.spinbox_sets.get().strip(), self.spinbox_reps.get().strip()]
        self.table.add_row(values=self.columns)
        self.window_training_form.destroy() 
        self.window_training_form = None
        self.label_no_exercises.grid_remove()
        if save == False:
            self.add_exercise()

    def save_training(self, is_draft):
        cursor.execute('SELECT id FROM workouts WHERE date = ?', [self.calendar.get_date()])
        result = cursor.fetchone()
        if self.table is None or not self.table.winfo_exists():
            CTkMessagebox(self.window_training_form, title='Ошибка', message='Нельзя сохранить пустую тренировку!', icon='cancel', font=FONT_LARGE)
        elif result is not None:
            CTkMessagebox(title='Ошибка', message='Тренировка за данное число уже существует!', icon='cancel', font=FONT_LARGE)
        else:
            table_data = self.table.get()
            calendar_data = self.calendar.get_date()
            cursor.execute('INSERT INTO workouts (date, is_draft) VALUES (?, ?)', [calendar_data, is_draft])
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
        self.history_page.setup_ui()
        self.drafts_page.setup_ui() 
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
    def __init__(self, master,  **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.date = None
        self.table_frame = None
        self.is_draft = 0
        self.not_yet = 'Тренировок'
        self.counter = 1

        self.setup_ui()

    def setup_ui(self):
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            for widget in self.winfo_children():
                widget.destroy()

            cursor.execute(f'''SELECT
                           strftime('%d.%m.%Y', date),
                           exercise,
                           weight,
                           sets,
                           reps
                           FROM workouts
                           JOIN exercises
                           ON workouts.id = workout_id
                           WHERE is_draft = {self.is_draft}
                           ORDER BY date DESC
                           ''')
            rows = cursor.fetchall()
            
            if rows:
                if self.table_frame is None or not self.table_frame.winfo_exists():
                    self.table_frame = CTkXYFrame(self, height=600, fg_color=BLACK_COLOR, width=800)
                    self.table_frame.grid()
                    self.table_frame.grid_columnconfigure(0, weight=1)
                    self.table_frame.grid_columnconfigure(0, weight=1)
                for i in range (len(rows)):
                    if rows[i][0] != self.date:
                        self.date = rows[i][0]
                        sedate_object = datetime.strptime(self.date, '%d.%m.%Y').date()
                        counter = 1
                        self.training_frame = ctk.CTkFrame(self.table_frame, fg_color=BLUE_COLOR, corner_radius=15)
                        self.training_frame.grid(pady=15, ipady=10, ipadx=10)
                        self.training_frame.grid_columnconfigure(0, weight=1)
                        self.label_date = ctk.CTkLabel(self.training_frame, text=f'Дата: {rows[i][0]}', font=FONT_LARGE)
                        self.label_date.pack(pady=15)
                        self.label_date = ctk.CTkLabel(self.training_frame, text=f'{DAYS_OF_THE_WEEK[sedate_object.weekday()]}', font=FONT_LARGE)
                        self.label_date.pack()
                    self.label_exercises = ctk.CTkLabel(self.training_frame, text=f'{counter}) {' x '.join(map(str, rows[i][1:]))}', font=FONT_LARGE)
                    self.label_exercises.pack(padx=20, anchor='w')
                    counter += 1
            else:
                self.label_no_trainings = ctk.CTkLabel(self, text=f'{self.not_yet} ещё нет!', font=HUGE_FONT)
                self.label_no_trainings.grid()

class Drafts(MyTrainings):
    def __init__(self, master,  **kwargs):
        super().__init__(master, **kwargs)

        self.date = None
        self.table_frame = None
        self.is_draft = 1
        self.not_yet = 'Черновиков'
        self.counter = 1
    
        self.setup_ui()

class About(ctk.CTkFrame):
    def __init__(self, master,  **kwargs):
        super().__init__(master, fg_color=BLACK_COLOR, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 

        self.setup_ui()
    
    def setup_ui(self):
        customers_view = ctk.CTkTextbox(self, font=FONT_LARGE, fg_color='transparent', width=600, height=650, wrap='word')
        customers_view._textbox.tag_configure("center", justify='center')
        customers_view.insert('1.0', TEXT_ABOUT, 'center')
        customers_view.insert('end', 'GitHub', ('hyperlink', 'center'))
        customers_view.insert('end', '.\n\nНовосибирск, 2026', 'center')
        customers_view.configure(state='disabled')
        customers_view._textbox.bind('<B1-Motion>', lambda _: 'break')
        customers_view._textbox.bind('<Double-Button-1>', lambda _: 'break')
        customers_view.grid()
        customers_view._textbox.tag_configure('hyperlink', foreground='#3b8ed0', underline=True)
        customers_view._textbox.tag_bind('hyperlink', '<Button-1>', self.open_repository)

    def open_repository(self, _):
        webbrowser.open_new_tab(REPO_URL)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.nav = CTkSidebarNavigation(self, width=250)
        self.nav.grid(sticky='nsew')

        side = self.nav.sidebar
        header = ctk.CTkLabel(side, text='Дневник\nтренировок', font=FONT_LARGE, fg_color='transparent', anchor='center', height=70)
        side.add_frame(header)

        side.add_item(id='add', text='Добавить')
        side.add_item(id='history', text='История')
        side.add_item(id='drafts', text='Черновики')
        side.add_item(id='info', text='Справка')

        history_container = self.nav.view('history')
        history_container.grid_columnconfigure(0, weight=1)
        history_container.grid_rowconfigure(0, weight=1)
        self.add_trainindg_page = MyTrainings(history_container)
        self.add_trainindg_page.grid(row=0, column=0, sticky='nsew')

        drarts_container = self.nav.view('drafts')
        drarts_container.grid_columnconfigure(0, weight=1)
        drarts_container.grid_rowconfigure(0, weight=1)
        self.add_trainindg_page = Drafts(drarts_container)
        self.add_trainindg_page.grid(row=0, column=0, sticky='nsew')

        add_container = self.nav.view('add')
        add_container.grid_columnconfigure(0, weight=1)
        add_container.grid_rowconfigure(0, weight=1)
        self.add_training_page = AddTraining(add_container, history_page=self.add_trainindg_page, drafts_page=self.add_trainindg_page)
        self.add_training_page.grid(row=0, column=0, sticky='nsew')

        info_container = self.nav.view('info')
        info_container.grid_columnconfigure(0, weight=1)
        info_container.grid_rowconfigure(0, weight=1)
        self.add_trainindgd_page = About(info_container)
        self.add_trainindgd_page.grid(row=0, column=0, sticky='nsew')

        self.nav.set('add')

app = App()
app.title('Дневник тренировок')
app.geometry('1100x650')
ctk.set_appearance_mode('Dark')
app.resizable(False, False)
app.mainloop()