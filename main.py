import customtkinter as ctk

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.add('Тренировки')
        self.add('Статистика')
        self.add('Профиль')
        self.add('Настройки')
        self.add('Помощь')

        self.label = ctk.CTkLabel(self)

        def add_traning():
            self.label.grid(row=0, column=0)


        self.button = ctk.CTkButton(master=self.tab('Тренировки'),text='Добавить тренировку',command=add_traning).grid(row=2, column=0)
        self.button = ctk.CTkButton(master=self.tab('Тренировки'),text='Мои тренировки').grid(row=2, column=2)
        self.button = ctk.CTkButton(master=self.tab('Тренировки'),text='Мои цели').grid(row=2, column=3)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.title('Дневник тренировок')
ctk.set_appearance_mode('Dark')
app.mainloop()