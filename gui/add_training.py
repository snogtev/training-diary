import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from libs.CTkTable import CTkTable
from libs.CTkDatePicker import CTkDatePicker
from libs.CTkScrollableDropdown import CTkScrollableDropdown
from libs.ctkspinbox import CTkSpinbox
from libs.CTkTable import CTkTable
from libs.CTkXYFrame import CTkXYFrame

from constants import *
from database import connection, cursor

class AddTraining(ctk.CTkFrame):
    def __init__(self, master, history_page, **kwargs):
        super().__init__(master, fg_color=BLACK_COLOR, **kwargs)
        self.history_page = history_page
        self.window_training_form = None
        self.table = None
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.setup_ui()

    def setup_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.label_date = ctk.CTkLabel(self, text=' Дата:', image=ICONS['calendar_dots'],
                                       compound='left', font=FONT_LARGE)
        self.label_date.grid(row=0, column=0, padx=25, pady=20, sticky='e')

        self.calendar = CTkDatePicker(self)
        self.calendar.set_localization('ru_RU.UTF-8')
        self.calendar.grid(row=0, column=1, pady=20, sticky='w')

        self.label_no_exercises = ctk.CTkLabel(self, text=' Упражнений ещё нет!', image=ICONS['ghost'],
                                               compound='left', font=HUGE_FONT)
        self.label_no_exercises.grid(row=1, column=0, columnspan=4, sticky='nsew')

        self.table_frame = CTkXYFrame(self, height=500, width=800, fg_color=BLACK_COLOR)

        self.button_add = ctk.CTkButton(self, text='Добавить упражнение', image=ICONS['plus_circle'],
                                        corner_radius=15, height=45, command=self.open_exercise_entry_form,
                                        font=FONT_LARGE)
        self.button_add.grid(row=2, column=0, pady=15, padx=25, columnspan=4, sticky='nsew')

        self.button_save = ctk.CTkButton(self, text='Сохранить', image=ICONS['floppy_disk'],
                                         corner_radius=15, height=45, command=self.save_training,
                                         font=FONT_LARGE)
        self.button_save.grid(row=3, column=0, columnspan=4, pady=15, padx=25, sticky='ew')

        self.button_reset = ctk.CTkButton(self, text='', hover=False, image=ICONS['arrow_counter_clockwise'],
                                          corner_radius=15, fg_color=BLACK_COLOR, width=45, height=45,
                                          command=self.reset, font=FONT_LARGE)

    def open_exercise_entry_form(self):
        if self.window_training_form is None or not self.window_training_form.winfo_exists():
            self.window_training_form = ctk.CTkToplevel()
            self.window_training_form.resizable(False, False)
            self.window_training_form.title('Упражнение')
            self.window_training_form.geometry(EXERCISE_ADD_FORM_SIZE)
            self.window_training_form.grid_columnconfigure(0, weight=0)
            self.window_training_form.grid_columnconfigure(1, weight=1)
            self.window_training_form.grid_rowconfigure(4, weight=1)

            self.spinbox_weight = CTkSpinbox(self.window_training_form, unit=' ' + UNIT,
                                             step_value=WEIGHT_STEP, font=FONT_LARGE)
            self.spinbox_sets = CTkSpinbox(self.window_training_form, start_value=3, font=FONT_LARGE)
            self.spinbox_reps = CTkSpinbox(self.window_training_form, start_value=8, font=FONT_LARGE)

            self.spinbox_weight.grid(row=1, column=1, pady=5, sticky='w')
            self.spinbox_sets.grid(row=2, column=1, pady=5, sticky='w')
            self.spinbox_reps.grid(row=3, column=1, pady=5, sticky='w')

            self.optionmenu = ctk.CTkComboBox(self.window_training_form, font=FONT_LARGE, width=350)
            self.optionmenu.set('')
            self.window_training_form.after(1, self.optionmenu.focus)

            self.button_more = ctk.CTkButton(self.window_training_form, text='Ещё', image=ICONS['plus_circle'],
                                             corner_radius=15, command=lambda: self.submit_exercise(save=False),
                                             font=FONT_LARGE)
            self.button_done = ctk.CTkButton(self.window_training_form, text='Завершить', image=ICONS['check_circle'],
                                             corner_radius=15, command=lambda: self.submit_exercise(save=True, data=None),
                                             font=FONT_LARGE)

            self.optionmenu.grid(row=0, column=1, pady=5, sticky='w')
            self.button_more.grid(row=5, column=0, columnspan=2, pady=5, padx=25, sticky='nsew')
            self.button_done.grid(row=6, column=0, pady=15, padx=25, columnspan=2, sticky='nsew')

            def insert_method(e):
                self.optionmenu.set(e)

            CTkScrollableDropdown(self.optionmenu, values=EXERCISE_LIST, font=FONT_SMALL,
                                  command=lambda _: insert_method(_), autocomplete=True)
            self.optionmenu.set('')

            for i, buttons in enumerate(FORM_HEADERS):
                ctk.CTkLabel(self.window_training_form, text=buttons + ':', font=FONT_LARGE).grid(
                    row=i, column=0, sticky='w', padx=25)

    def open_exercise_edit_form(self, data):
        def clean_num(val):
            f_val = float(val)
            return int(f_val) if f_val == int(f_val) else f_val

        if self.window_training_form is None or not self.window_training_form.winfo_exists():
            self.window_training_form = ctk.CTkToplevel()
            self.window_training_form.resizable(False, False)
            self.window_training_form.title('Упражнение')
            self.window_training_form.geometry(EXERCISE_EDIT_FORM_SIZE)
            self.window_training_form.grid_columnconfigure(0, weight=0)
            self.window_training_form.grid_columnconfigure(1, weight=1)
            self.window_training_form.grid_rowconfigure(4, weight=1)

            self.spinbox_weight = CTkSpinbox(self.window_training_form, unit=' ' + UNIT,
                                             start_value=clean_num(self.table.get(data['row'])[1][2]),
                                             step_value=WEIGHT_STEP, font=FONT_LARGE)
            self.spinbox_sets = CTkSpinbox(self.window_training_form,
                                           start_value=clean_num(self.table.get(data['row'])[1][3]),
                                           font=FONT_LARGE)
            self.spinbox_reps = CTkSpinbox(self.window_training_form,
                                           start_value=clean_num(self.table.get(data['row'])[1][4]),
                                           font=FONT_LARGE)

            self.spinbox_weight.grid(row=1, column=1, pady=5, sticky='w')
            self.spinbox_sets.grid(row=2, column=1, pady=5, sticky='w')
            self.spinbox_reps.grid(row=3, column=1, pady=5, sticky='w')

            self.optionmenu = ctk.CTkComboBox(self.window_training_form, font=FONT_LARGE, width=300)
            self.window_training_form.after(1, self.optionmenu.focus)

            self.button_done = ctk.CTkButton(self.window_training_form, text='Готово', image=ICONS['check_circle'],
                                             corner_radius=15, command=lambda: self.submit_exercise(True, data),
                                             font=FONT_LARGE)

            self.optionmenu.grid(row=0, column=1, pady=5, sticky='w')
            self.button_done.grid(row=5, column=0, columnspan=2, pady=(5, 20), padx=25, sticky='nsew')

            def insert_method(e):
                self.optionmenu.set(e)

            CTkScrollableDropdown(self.optionmenu, values=EXERCISE_LIST, font=FONT_MEDIUM,
                                  command=lambda _: insert_method(_), autocomplete=True)
            self.optionmenu.set(self.table.get(data['row'])[1][1])
            self.window_training_form.wm_attributes('-topmost', 1)

            for i, buttons in enumerate(FORM_HEADERS):
                ctk.CTkLabel(self.window_training_form, text=buttons + ':', font=FONT_LARGE).grid(
                    row=i, column=0, sticky='w', padx=25)

    def submit_exercise(self, save, data=None):
        exercise_name = self.optionmenu.get().strip()
        if not exercise_name:
            CTkMessagebox(self.window_training_form, title='Ошибка', 
                          message='Введите название упражнения!', icon='cancel', font=FONT_LARGE)
            return
        if len(exercise_name) > 50:
            CTkMessagebox(self.window_training_form, title='Ошибка', 
                          message='Название не должно превышать 50 символов!', icon='cancel', font=FONT_LARGE)
            return
        
        weight_str = self.spinbox_weight.get().replace(' ', '')
        if not weight_str:
            CTkMessagebox(self.window_training_form, title='Ошибка', 
                          message='Введите вес!', icon='cancel', font=FONT_LARGE)
            return
        try:
            weight = float(weight_str)
            if weight < 0:
                CTkMessagebox(self.window_training_form, title='Ошибка', 
                              message='Вес не может быть отрицательным!', icon='cancel', font=FONT_LARGE)
                return
            if weight > 1000:
                CTkMessagebox(self.window_training_form, title='Ошибка', 
                              message='Вес не может превышать 1000 кг!', icon='cancel', font=FONT_LARGE)
                return
        except ValueError:
            pass

        sets_str = self.spinbox_sets.get().replace(' ', '')
        if not sets_str:
            CTkMessagebox(self.window_training_form, title='Ошибка', 
                          message='Введите количество подходов!', icon='cancel', font=FONT_LARGE)
            return
        
        try:
            sets = int(sets_str)
            if sets <= 0:
                CTkMessagebox(self.window_training_form, title='Ошибка', 
                              message='Подходов должно быть больше 0!', icon='cancel', font=FONT_LARGE)
                return
            if sets > 50:
                CTkMessagebox(self.window_training_form, title='Ошибка', 
                              message='Максимум подходов - 50!', icon='cancel', font=FONT_LARGE)
                return
        except ValueError:
            pass

        reps_str = self.spinbox_reps.get().replace(' ', '')
        if not reps_str:
            CTkMessagebox(self.window_training_form, title='Ошибка', 
                          message='Введите количество повторений!', icon='cancel', font=FONT_LARGE)
            return
        
        try:
            reps = int(reps_str)
            if reps <= 0:
                CTkMessagebox(self.window_training_form, title='Ошибка', 
                              message='Повторений должно быть больше 0!', icon='cancel', font=FONT_LARGE)
                return
            if reps > 100:
                CTkMessagebox(self.window_training_form, title='Ошибка', 
                              message='Максимум повторений - 100!', icon='cancel', font=FONT_LARGE)
                return
        except ValueError:
            pass

        if self.table is None:
            self.create_table()

        if data is None:
            self.add_exercise_row(save)
        else:
            self.edit_exercise_row(data)

        self.create_table()

    def add_exercise_row(self, save):
        if self.table is None:
            return
        
        columns = [len(self.table.get()),
                   self.optionmenu.get().strip(),
                   self.spinbox_weight.get().strip(),
                   self.spinbox_sets.get().strip(),
                   self.spinbox_reps.get().strip(),
                   '', '']

        self.table.add_row(values=columns)
        row_idx = len(self.table.get()) - 1
        self.table.insert(row_idx, 5, value='', image=ICONS['pencil'], anchor="w")
        self.table.insert(row_idx, 6, value='', image=ICONS['trash'], anchor="w")

        for r in range(len(self.table.get())):
            self.table.edit(r, 5, fg_color='transparent', corner_radius=0)
            self.table.edit(r, 6, fg_color='transparent', corner_radius=0)

        self.window_training_form.destroy()
        self.window_training_form = None
        self.label_no_exercises.grid_remove()

        if not save:
            self.open_exercise_entry_form()

        if len(self.table.get()) == 2:
            self.button_reset.grid(row=0, column=3, padx=25, pady=20, sticky='e')

    def edit_exercise_row(self, data):
        if self.table is None:
            return
        
        columns = [data['row'], self.optionmenu.get().strip(),
                   self.spinbox_weight.get().strip(), self.spinbox_sets.get().strip(),
                   self.spinbox_reps.get().strip(), '', '']

        for col_index, value in enumerate(columns):
            self.table.insert(data['row'], col_index, value)

        for r in range(len(self.table.get())):
            self.table.edit(r, 5, fg_color='transparent', corner_radius=0)
            self.table.edit(r, 6, fg_color='transparent', corner_radius=0)

        self.window_training_form.destroy()
        self.window_training_form = None
        self.label_no_exercises.grid_remove()

    def create_table(self):
        if self.table is None:
            self.table_frame.grid(row=1, column=0, columnspan=5, sticky='nsew')
            self.table = CTkTable(self.table_frame, font=FONT_LARGE, header_color=BLUE_COLOR,
                                  width=40, values=[TABLE_HEADERS], command=self.manage_exercises)
            for index, width in enumerate(TABLE_COLUMN_WIDTHS):
                self.table.edit_column(index, width=width)
            self.table.grid()

    def manage_exercises(self, data):
        if data['column'] == 5 and data['row'] != 0:
            self.open_exercise_edit_form(data)
        elif data['column'] == 6 and data['row'] != 0:
            self.table.delete_row(data['row'])
            if len(self.table.get()) == 1:
                self.reset()
                self.setup_ui()
                return
            for i in range(1, len(self.table.get())):
                self.table.insert(i, 0, i)
            for r in range(len(self.table.get())):
                self.table.edit(r, 5, fg_color='transparent', corner_radius=0)
                self.table.edit(r, 6, fg_color='transparent', corner_radius=0)

    def save_training(self):
        try:
            selected_date = self.calendar.get_date()
        except:
            CTkMessagebox(self, title='Ошибка', 
                          message='Введите корректную дату или\nвыберите её в календаре!', 
                          icon='cancel', font=FONT_LARGE)
            return
        
        if not selected_date:
            CTkMessagebox(self, title='Ошибка', message='Выберите дату!', icon='cancel', font=FONT_LARGE)
            return
        
        if self.table is None or len(self.table.get()) <= 1:
            CTkMessagebox(self, title='Ошибка', message='Нельзя сохранить пустую тренировку!',
                          icon='cancel', font=FONT_LARGE)
            return
        
        cursor.execute('SELECT id FROM workouts WHERE date = ?', [selected_date])
        result = cursor.fetchone()
        
        if result is not None:
            CTkMessagebox(self, title='Ошибка', message='Тренировка за данное число уже существует!',
                          icon='cancel', font=FONT_LARGE)
            return
        
        table_data = self.table.get()
        calendar_data = self.calendar.get_date()
        new_data = []

        cursor.execute('INSERT INTO workouts (date) VALUES (?)', [calendar_data])
        current_workout_id = cursor.lastrowid

        for row in table_data:
            trimmed_row = row[1:5]
            trimmed_row.insert(0, current_workout_id)
            new_data.append(trimmed_row)

        cursor.executemany('INSERT INTO exercises (workout_id, exercise, weight, sets, reps) VALUES (?, ?, ?, ?, ?)',
                           new_data[1:])
        connection.commit()

        CTkMessagebox(message='Тренировка успешно добавлена!', title='Успех',
                      icon='check', option_1='ОК', font=FONT_LARGE)
        self.reset()

    def reset(self):
        if self.table:
            self.table.grid_remove()
        self.table_frame.grid_remove()
        self.table = None
        self.window_training_form = None
        self.setup_ui()