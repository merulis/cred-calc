import tkinter as tk
from tkinter import ttk

from src.models import MatchedPayment

class ResultView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Результаты расчета")
        self.geometry("600x400")

        self._create_table()
        self._create_save_button()

    def _create_table(self):
        map = MatchedPayment.fields_map()

        self.table = ttk.Treeview(
            self,
            columns=list(map.keys()),
            show="headings",
        )

        for key, title in map.items():
            self.table.heading(key, text=title)
            self.table.column(key, width=120, anchor="center")

        self.table.pack(fill="both", expand=True, pady=10)

        self.table.tag_configure("oddrow", background="#e0e0e0")  # светло-серый
        self.table.tag_configure("evenrow", background="#ffffff")  # белый

    def _create_save_button(self):
        self.save_button = tk.Button(self, text="Сохранить в файл")
        self.save_button.pack(pady=10)

    def insert_row(self, values: list | tuple):
        index = len(self.table.get_children())
        tag = "evenrow" if index % 2 == 0 else "oddrow"
        self.table.insert("", "end", values=values, tags=(tag,))
