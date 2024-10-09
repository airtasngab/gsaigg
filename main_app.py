import sys
import os
import tkinter as tk
from tkinter import ttk
from home_page import HomePageApp
from wxrev import WxrevMenu
from prakgel import PrakgelMenu
from pdce3h import Pdce3hMenu
from PageNotFound import PageNotFound

def resource_path(relative_path):
    """ Dapatkan path absolut untuk file dalam resource (jika dibundle menggunakan PyInstaller) """
    try:
        base_path = sys._MEIPASS  # pylint: disable=W0212,E1101
    except Exception:
        base_path = os.path.abspath(".")  # untuk jalur file saat development

    return os.path.join(base_path, relative_path)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GSA IGG")
        icon_path = resource_path("assets//logo.ico")
        self.iconbitmap(icon_path)
        self.geometry("1400x750")

        self.frames = {}
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (HomePageApp, WxrevMenu, PrakgelMenu, Pdce3hMenu, PageNotFound):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePageApp")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
