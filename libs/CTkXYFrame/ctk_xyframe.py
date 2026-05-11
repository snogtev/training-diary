"""
Optimized CTkXYFrame
Fixed by Stepan Nogtev (Original by Akash Bora)
- Fixed RecursionError in destroy()
- Fixed Top-clipping bug for long lists
- Added Smart Centering
"""

import customtkinter
from tkinter import Canvas

class CTkXYFrame(customtkinter.CTkFrame):
    def __init__(self,
                 master: any,
                 width: int = 100,
                 height: int = 100,
                 scrollbar_width: int = 16,
                 scrollbar_fg_color = None,
                 scrollbar_button_color = None,
                 scrollbar_button_hover_color = None,
                 **kwargs):

        self.parent_frame = customtkinter.CTkFrame(master=master, **kwargs)
        self.bg_color = self.parent_frame.cget("fg_color")
        
        self.parent_frame.rowconfigure(0, weight=1)
        self.parent_frame.columnconfigure(0, weight=1)

        self.xy_canvas = Canvas(self.parent_frame, width=width, height=height,
                                bg=self.parent_frame._apply_appearance_mode(self.bg_color),
                                borderwidth=0, highlightthickness=0)
        
        super().__init__(master=self.xy_canvas, 
                         fg_color=self.parent_frame.cget("fg_color"),
                         bg_color=self.parent_frame.cget("fg_color"))
        
        self.window_id = self.xy_canvas.create_window((width/2, 0), window=self, anchor="n")
        
        self.vsb = customtkinter.CTkScrollbar(self.parent_frame, orientation="vertical", command=self.xy_canvas.yview,
                                              fg_color=scrollbar_fg_color, button_color=scrollbar_button_color,
                                              button_hover_color=scrollbar_button_hover_color, width=scrollbar_width)
        self.hsb = customtkinter.CTkScrollbar(self.parent_frame, orientation="horizontal", command=self.xy_canvas.xview,
                                              fg_color=scrollbar_fg_color, button_color=scrollbar_button_color,
                                              button_hover_color=scrollbar_button_hover_color, height=scrollbar_width)
        
        self.xy_canvas.configure(yscrollcommand=self.dynamic_scrollbar_vsb,
                                 xscrollcommand=self.dynamic_scrollbar_hsb)
        
        self.xy_canvas.grid(row=0, column=0, sticky="nsew", padx=(7,0), pady=(7,0))
        
        self.bind("<Configure>", lambda e: self.onFrameConfigure())
        self.xy_canvas.bind("<Configure>", lambda e: self.onFrameConfigure())
        
        self.xy_canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.xy_canvas.bind_all("<Button-4>", lambda e: self.xy_canvas.yview_scroll(-1, "units"), add="+")
        self.xy_canvas.bind_all("<Button-5>", lambda e: self.xy_canvas.yview_scroll(1, "units"), add="+")

    def onFrameConfigure(self):
        self.update_idletasks()
        
        bbox = self.xy_canvas.bbox("all")
        if not bbox: return
        
        padded_bbox = (bbox[0], bbox[1], bbox[2], bbox[3] + 20)
        self.xy_canvas.configure(scrollregion=padded_bbox)
        
        canvas_width = self.xy_canvas.winfo_width()
        canvas_height = self.xy_canvas.winfo_height()
        content_width = self.winfo_reqwidth()
        content_height = self.winfo_reqheight()

        x = max(canvas_width / 2, content_width / 2)

        if content_height < canvas_height:
            y = canvas_height / 2
            anchor = "center"
        else:
            y = 0
            anchor = "n"

        self.xy_canvas.itemconfig(self.window_id, anchor=anchor)
        self.xy_canvas.coords(self.window_id, x, y)

    def dynamic_scrollbar_vsb(self, x, y):
        if float(x) <= 0.0 and float(y) >= 1.0:
            self.vsb.grid_forget()
        else:
            self.vsb.grid(row=0, column=1, sticky="nse", pady=5)
        self.vsb.set(x, y)
        
    def dynamic_scrollbar_hsb(self, x, y):
        if float(x) <= 0.0 and float(y) >= 1.0:
            self.hsb.grid_forget()
        else:
            self.hsb.grid(row=1, column=0, sticky="new", padx=(5,0))
        self.hsb.set(x, y)

    def _on_mousewheel(self, event):
        if self.xy_canvas.winfo_exists():
            self.xy_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def grid(self, **kwargs): self.parent_frame.grid(**kwargs)
    def pack(self, **kwargs): self.parent_frame.pack(**kwargs)
    def place(self, **kwargs): self.parent_frame.place(**kwargs)
    def winfo_exists(self): return self.parent_frame.winfo_exists()