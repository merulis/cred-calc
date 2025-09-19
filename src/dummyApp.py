import tkinter as tk

from src.views.dummyView import DummyView
from src.controllers.dummyController import DummyController


class DummyTkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cred Calc")

        self.view = DummyView(self.root)
        self.controller = DummyController(self.view)

    def run(self):
        self.root.mainloop()
