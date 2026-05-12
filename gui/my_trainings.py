from datetime import datetime

import customtkinter as ctk
from libs.CTkXYFrame import CTkXYFrame

from constants import *
from database import cursor

class MyTrainings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.table_frame = None
        self.no_trainings_label = None
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        for widget in self.winfo_children():
            widget.destroy()

        self.table_frame = CTkXYFrame(self, height=600, fg_color=BLACK_COLOR, width=800)
        self.table_frame.grid(sticky='nsew')
        self.table_frame.grid_columnconfigure(0, weight=1)

        self.refresh()

    def refresh(self):
        if not self.table_frame:
            return

        # Очищаем содержимое table_frame
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Убираем надпись "Тренировок ещё нет", если она была
        if self.no_trainings_label:
            self.no_trainings_label.destroy()
            self.no_trainings_label = None

        cursor.execute('''SELECT
            strftime('%d.%m.%Y', date),
            exercise, weight, sets, reps
            FROM workouts
            JOIN exercises ON workouts.id = workout_id
            ORDER BY date DESC''')
        rows = cursor.fetchall()

        if not rows:
            # Показываем надпись по центру
            self.table_frame.grid_remove()
            self.no_trainings_label = ctk.CTkLabel(self, text=' Тренировок ещё нет!',
                                                   image=ICONS['ghost'], compound='left', font=HUGE_FONT)
            self.no_trainings_label.grid(row=0, column=0, sticky='nsew')
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            return

        # Если данные есть, показываем table_frame
        self.table_frame.grid()
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)

        current_date = None
        main_row = 0
        training_frame = None

        for i, row in enumerate(rows):
            row_date = row[0]

            if row_date != current_date:
                current_date = row_date
                date_obj = datetime.strptime(current_date, '%d.%m.%Y').date()
                exercise_counter = 1
                current_row = 1

                training_frame = ctk.CTkFrame(self.table_frame, fg_color=BLUE_COLOR, corner_radius=15)
                training_frame.grid(row=main_row, column=0, pady=15, padx=25, ipady=10, ipadx=10, sticky='ew')
                training_frame.grid_columnconfigure(0, weight=1)
                main_row += 1

                date_text = f' Дата: {current_date}, {DAYS_OF_THE_WEEK[date_obj.weekday()]}'
                label_date = ctk.CTkLabel(training_frame, text=date_text,
                                          image=ICONS['calendar_dots'], compound='left', font=FONT_LARGE)
                label_date.grid(row=0, column=0, pady=(10, 5))

            exercise_text = f"{exercise_counter}) {' x '.join(map(str, row[1:]))}"
            label_ex = ctk.CTkLabel(training_frame, text=exercise_text, font=FONT_LARGE)
            label_ex.grid(row=current_row, column=0, padx=20, pady=2)

            exercise_counter += 1
            current_row += 1

        self.table_frame.update_idletasks()