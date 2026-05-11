from datetime import datetime

import customtkinter as ctk
from libs.CTkXYFrame import CTkXYFrame

from constants import *
from database import cursor

class MyTrainings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.date = None
        self.table_frame = None
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        for widget in self.winfo_children():
            widget.destroy()

        self.date = None
        self.training_frame = None
        self.table_frame = None

        cursor.execute('''SELECT
            strftime('%d.%m.%Y', date),
            exercise, weight, sets, reps
            FROM workouts
            JOIN exercises
            ON workouts.id = workout_id
            ORDER BY date DESC''')
        
        rows = cursor.fetchall()

        if rows:
            self.table_frame = CTkXYFrame(self, height=600, fg_color=BLACK_COLOR, width=800)
            self.table_frame.grid(sticky='nsew')
            self.table_frame.grid_columnconfigure(0, weight=1)

            main_row = 0
            for i in range(len(rows)):
                row_date = rows[i][0]

                if row_date != self.date or self.training_frame is None:
                    self.date = row_date
                    sedate_object = datetime.strptime(self.date, '%d.%m.%Y').date()
                    exercise_counter = 1
                    current_row = 1 

                    self.training_frame = ctk.CTkFrame(self.table_frame, fg_color=BLUE_COLOR, corner_radius=15)
                    self.training_frame.grid(row=main_row, pady=15, padx=25, ipady=10, ipadx=10, sticky='ew')
                    self.training_frame.grid_columnconfigure(0, weight=1)
                    main_row += 1

                    date_text = f' Дата: {self.date}, {DAYS_OF_THE_WEEK[sedate_object.weekday()]}'
                    label_date = ctk.CTkLabel(self.training_frame, text=date_text,
                                                   image=ICONS['calendar_dots'], compound='left', font=FONT_LARGE)
                    label_date.grid(row=0, column=0, pady=(10, 5))

                exercise_text = f"{exercise_counter}) {' x '.join(map(str, rows[i][1:]))}"
                label = ctk.CTkLabel(self.training_frame, text=exercise_text, font=FONT_LARGE)
                label.grid(row=current_row, column=0, padx=20, pady=2)
                
                exercise_counter += 1
                current_row += 1
        else:
            label_no_trainings = ctk.CTkLabel(self, text=' Тренировок ещё нет!',
                                                   image=ICONS['ghost'], compound='left', font=HUGE_FONT)
            label_no_trainings.grid(pady=100)
