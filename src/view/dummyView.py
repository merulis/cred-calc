import tkinter as tk
from tkinter import ttk


class DummyView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_load = None
        self.on_calculate = None

        self.load_button = tk.Button(
            self,
            text="Загрузить",
            command=self._handle_load,
        )
        self.load_button.pack(pady=5)

        self.calc_button = tk.Button(
            self,
            text="Рассчитать",
            command=self._handle_calculate,
        )
        self.calc_button.pack(pady=5)

        self.table = ttk.Treeview(
            self, columns=("col1", "col2", "col3"), show="headings"
        )
        self.table.heading("col1", text="Колонка 1")
        self.table.heading("col2", text="Колонка 2")
        self.table.heading("col3", text="Колонка 3")
        self.table.pack(fill="both", expand=True, pady=10)

        self.log_box = tk.Text(self, height=5)
        self.log_box.pack(fill="x", pady=5)

    def _handle_load(self):
        if self.on_load:
            self.on_load()

    def _handle_calculate(self):
        if self.on_calculate:
            self.on_calculate()

    def show_message(self, msg: str):
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")

    def insert_row(self, values: tuple):
        self.table.insert("", "end", values=values)
