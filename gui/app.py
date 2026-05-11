import customtkinter as ctk
from ctksidebar import CTkSidebarNavigation

from constants import *
from gui import About, AddTraining, MyTrainings

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.nav = CTkSidebarNavigation(self, width=250)
        self.nav.grid(sticky='nsew')

        self.setup_sidebar()
        self.setup_pages()

        self.nav.set('add')

    def create_container(self, container_id):
        container = self.nav.view(container_id)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        return container

    def setup_sidebar(self):
        side = self.nav.sidebar
        
        header = ctk.CTkLabel(side, text=' Дневник\n тренировок',
                              font=FONT_LARGE, image=ICONS['weights'],
                              compound='left', height=70)
        
        side.add_frame(header, pady=(10, 0))
        side.add_spacing(height=10)

        for item in SIDEBAR_MENU:
            icon = ICONS[item['icon']]
            side.add_item(id=item['id'],
                          text=item['text'], 
                          icon=(icon, icon), 
                          override_icon_x=10)

    def setup_pages(self):
        self.history_page = MyTrainings(self.create_container('history'))
        self.add_page = AddTraining(self.create_container('add'), 
                                    history_page=self.history_page)
        self.about_page = About(self.create_container('info'))

        self.history_page.grid(row=0, column=0, sticky='nsew')
        self.add_page.grid(row=0, column=0, sticky='nsew')
        self.about_page.grid(row=0, column=0, sticky='nsew')