import customtkinter as ctk


class MainMenu(ctk.CTkFrame):
    def __init__(self, master, new_frame, **kwargs,):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text='Мои тренировки')

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20)
        self.tabview.add('Тренировки')
        self.tabview.add('Статистика')
        self.tabview.add('Профиль')
        self.tabview.add('Настройки')
        self.tabview.add('Помощь')

        ctk.CTkButton(master=self.tabview.tab('Тренировки'),text='Добавить тренировку',command=new_frame).grid(row=2, column=0)
        ctk.CTkButton(master=self.tabview.tab('Тренировки'),text='Мои тренировки').grid(row=2, column=2)
        ctk.CTkButton(master=self.tabview.tab('Тренировки'),text='Мои цели').grid(row=2, column=3)


class AddTraning(ctk.CTkFrame):
    def __init__(self, master, new_fragme, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text='В разработке...')
        self.label.grid(row=0, column=0, padx=20)
        ctk.CTkButton(master=self, text='Назад',command=new_fragme).grid(row=2, column=0)



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_menu = MainMenu(master=self, new_frame=self.new_framee)
        self.add_traning = AddTraning(master=self, new_fragme=self.new_fragmef)
        self.main_menu.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.add_traning.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_menu.tkraise()

    def new_framee(self):
        self.add_traning.tkraise()

    def new_fragmef(self):
        self.main_menu.tkraise()



app = App()
app.title('Дневник тренировок')
app.geometry('500x200')
app.resizable(False, False)
app.mainloop()