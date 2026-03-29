import customtkinter as ctk
from CTkTable import CTkTable
from CTkDatePicker import CTkDatePicker
from ctkspinbox import CTkSpinbox

ctk.FontManager.load_font('Russo One.ttf')

FONT_LARGE = ('Russo One', 25)
FONT_MEDIUM = ('Russo One', 22)
FONT_SMALL = ('Russo One', 18)


class MainMenu(ctk.CTkFrame):
    def __init__(self, master, navigate, **kwargs,):
        self.tabs = ('Тренировки',
                'Статистика',
                'Профиль',
                'Настройки',
                'Помощь')
        
        self.buttons = [
                   {'text': 'Добавить тренировку', 'command': lambda: navigate('add')},
                   {'text': 'Мои тренировки'},
                   {'text': 'Мои цели'}
]
        
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
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

        self.columns = ('Упражнение',
                        'Вес',
                        'Подходы',
                        'Повторения')
        self.buttons = [
                   {'text': 'Добавить упражнение', 'command': self.add_exercise},
                   {'text': 'Назад', 'command': lambda: navigate('menu')},
                   {'text': 'Сохранить'}
]
        self.setup_ui()
        self.create_calendar()
        self.create_table()
    
    def add_exercise(self):
        TrainingForm = ctk.CTkToplevel()
        TrainingForm.title('Упражнение')
        TrainingForm.geometry('250x200')
        self.spinbox = CTkSpinbox(TrainingForm, step_value=2.5, font=('Russo One', 25))
        self.spinbox.grid()
        for buttons in self.columns:
            ctk.CTkLabel(TrainingForm, text=buttons, font=FONT_LARGE).grid()


    def setup_ui(self):
        for i, btn_data in enumerate(self.buttons, start=1):
            ctk.CTkButton(self, **btn_data, font=FONT_LARGE).grid(row=i, pady=15)
        ctk.CTkLabel(self, text='Дата:', font=('Russo One', 25)).grid(row=0, column=0)

    def create_calendar(self):
        self.calendar = CTkDatePicker(self)
        self.calendar.set_localization("ru_RU.UTF-8")
        self.calendar.grid(row=0, column=1)

    def create_table(self):
        self.table = CTkTable(self, row=2, font=('Russo One', 25), header_color = '#1f538d', values=[self.columns])
        self.table.grid()


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