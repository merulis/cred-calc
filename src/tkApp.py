import tkinter as tk

from src.controllers.controller import Controller


class TkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cred Calc")

        self.controller = Controller(self.root)

    def run(self):
        self.root.mainloop()
