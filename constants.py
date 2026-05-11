from pathlib import Path

import customtkinter as ctk
from PIL import Image

DB_NAME = 'trainings.db'
REPO_URL = 'https://github.com/snogtev/training-diary'

ICONS = {}
for file in Path('icons').glob('*.png'):
    img = Image.open(file)
    if file.stem in ('ghost', 'weights'):
        icon_size = (57, 57)
    else:
        icon_size = (32, 32)
    ICONS[file.stem] = ctk.CTkImage(img, size=icon_size)

MAIN_WINWOD_SIZE = '1100x650'
EXERCISE_ADD_FORM_SIZE = '650x325'
EXERCISE_EDIT_FORM_SIZE = '650x275' 

TABLE_COLUMN_WIDTHS = (40, 200, 100, 150, 80, 40, 40)

TEXT_ABOUT = ('Программа разработана в рамках индивидуального проекта по дисциплине «ОУП.08 Информатика».\n\n'
              'Автор: Ногтев Степан Вячеславович, студент 1 курса группы ИСиП-2-9-25 ГАПОУ НСО «НКПиИТ».\n\n'
              'Руководитель: Груздев Евгений Александрович, преподаватель первой квалификационной категории.\n\n'
              'Технологии разработки: Python, CustomTkinter (включая сторонние библиотеки) и SQLite3.\n\n'
              'Проект имеет открытый исходный код и доступен в репозитории на ')

TABLE_HEADERS = ('№', 'Упражнение', 'Вес', 'Подходы', 'Повторения', '', '')
FORM_HEADERS = ('Упражнение', 'Вес', 'Подходы', 'Повторения')
EXERCISE_LIST = ('Жим лёжа', 'Присед', 'Становая тяга')
DAYS_OF_THE_WEEK = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')

SIDEBAR_MENU = ({'id': 'add', 'text': 'Добавить', 'icon': 'plus_circle'},
                {'id': 'history', 'text': 'История', 'icon': 'clipboard_text'},
                {'id': 'info', 'text': 'Справка', 'icon': 'info'})


BLACK_COLOR = '#242424'
BLUE_COLOR = '#1f538d'
LIGHT_BLUE_COLOR = '#3b8ed0'

FONT_FAMILY = 'Russo One'
HUGE_FONT = (FONT_FAMILY, 45)
FONT_LARGE = (FONT_FAMILY, 25)
FONT_MEDIUM = (FONT_FAMILY, 22)
FONT_SMALL = (FONT_FAMILY, 18)

WEIGHT_STEP = 2.5
DEFAULT_STEP = 1
UNIT = 'кг'