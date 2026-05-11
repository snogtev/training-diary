import webbrowser

import customtkinter as ctk

from constants import *


class About(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0) 

        self.setup_ui()
    
    def setup_ui(self):
        view = ctk.CTkTextbox(self, font=FONT_LARGE, fg_color='transparent', 
                              width=800, height=450, wrap='word')
        
        view._textbox.tag_configure('center', justify='center')
        view._textbox.tag_configure('link', foreground=LIGHT_BLUE_COLOR, underline=True)

        view.insert('1.0', TEXT_ABOUT, 'center')
        view.insert('end', 'GitHub', ('link', 'center'))
        view.insert('end', '.', 'center')

        view.configure(state='disabled')
        view._textbox.bind('<B1-Motion>', lambda _: 'break')
        
        view._textbox.tag_bind('link', '<Button-1>', self.open_repository)
        view._textbox.tag_bind('link', '<Enter>', lambda _: view.configure(cursor='hand2'))
        view._textbox.tag_bind('link', '<Leave>', lambda _: view.configure(cursor=''))

        view.grid(row=0, column=0)

        footer = ctk.CTkLabel(self, text='Новосибирск, 2026', font=FONT_LARGE)
        footer.grid(row=1, column=0, sticky='s', pady=20)

    def open_repository(self, _):
        webbrowser.open_new_tab(REPO_URL)