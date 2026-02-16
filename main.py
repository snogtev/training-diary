import customtkinter as ctk

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.add('Тренировки')
        self.add('Статистика')
        self.add('Профиль')
        self.add('Настройки')
        self.add('Помощь')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.title('Дневник тренировок')
app.mainloop()