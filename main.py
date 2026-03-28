import customtkinter as ctk
from CTkTable import CTkTable
from CTkDatePicker import CTkDatePicker
from ctkspinbox import CTkSpinbox


ctk.FontManager.load_font('Russo One.ttf')

FONT_LARGE = ('Russo One', 25)
FONT_MEDIUM = ('Russo One', 22)
FONT_SMALL = ('Russo One', 18)


class MainMenu(ctk.CTkFrame):
    def __init__(self, new_frame, **kwargs,):
        tabs = ('Тренировки',
                'Статистика',
                'Профиль',
                'Настройки',
                'Помощь')
        buttons = [{'text': 'Добавить тренировку', 'command': new_frame},
                   {'text': 'Мои тренировки'},
                   {'text': 'Мои цели'}]
        
        
        super().__init__(**kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tabview = ctk.CTkTabview(self, width=700, height=550)
        self.tabview.grid(row=0, column=0, padx=20, pady=20)
        for tab in tabs:
            self.tabview.add(tab)
        self.tabview._segmented_button.configure(font=FONT_MEDIUM)

        self.tabview.tab('Тренировки').grid_columnconfigure(0, weight=1)
        for btn_data in buttons:
            ctk.CTkButton(self.tabview.tab('Тренировки'), **btn_data, font=FONT_LARGE).grid()


class AddTraining(ctk.CTkFrame):
    def __init__(self, master, new_fragme, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = ('Упражнение',
                        'Вес',
                        'Подходы',
                        'Повторения')
        self.new_fragme = new_fragme
        
        self.setup_ui()
        self.create_calendar()
        self.create_table()
    
    def add_exercise(self):
        dd = ctk.CTkToplevel()
        dd.title('Упражнение')
        dd.geometry('250x200')
        self.spinbox = CTkSpinbox(dd, step_value=2.5, font=('Russo One', 25)).grid()
        ctk.CTkLabel(dd, text='Вес:', font=('Russo One', 25)).grid()
        ctk.CTkLabel(dd, text='Подходы:', font=('Russo One', 25)).grid()
        ctk.CTkLabel(dd, text='Повторения:', font=('Russo One', 25)).grid()

    def setup_ui(self):
        ctk.CTkLabel(self, text='Дата:', font=('Russo One', 25)).grid(row=0, column=0)
        ctk.CTkButton(self, text='Назад', command=self.new_fragme, font=('Russo One', 25)).grid(row=2, column=0, pady=10)
        ctk.CTkButton(self, text='Добавить упражнение', command=self.add_exercise, font=('Russo One', 25)).grid(row=6, column=0, pady=10)
        ctk.CTkButton(self, text='Сохранить', font=('Russo One', 25)).grid(row=10, column=0, pady=10)

    def create_calendar(self):
        self.calendar = CTkDatePicker(self)
        self.calendar.set_localization("ru_RU.UTF-8")
        self.calendar.grid()

    def create_table(self):
        self.table = CTkTable(self, row=2, font=('Russo One', 25), header_color = '#1f538d', values=[self.columns])
        self.table.grid()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_menu = MainMenu(master=self, new_frame=self.new_framee)
        self.add_traning = AddTraining(master=self, new_fragme=self.new_fragmef)
        self.main_menu.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.add_traning.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_menu.tkraise()

    def new_framee(self):
        self.add_traning.tkraise()

    def new_fragmef(self):
        self.main_menu.tkraise()

app = App()
app.title('Дневник тренировок')
app.geometry('800x600')
ctk.set_appearance_mode('Dark')
app.resizable(False, False)
app.mainloop()