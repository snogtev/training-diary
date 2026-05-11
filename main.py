import customtkinter as ctk

from constants import *
from gui.app import App

ctk.FontManager.load_font('Russo One.ttf')

app = App()
app.title('Дневник тренировок')
app.geometry(MAIN_WINWOD_SIZE)
ctk.set_appearance_mode('Dark')
app.resizable(False, False)
app.mainloop()