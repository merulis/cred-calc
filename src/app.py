import tkinter as tk
import pandas as pd

from src.dataImporter import DataImporter
from src.soureActExtractor import SoureActExtractor, XlsColumns

from pathlib import Path
from tkinter import filedialog, ttk
from collections import deque
from datetime import datetime, timedelta


class App:
    def __init__(self, settings = None):
        self.window = self.build_window()

    def build_window(self):
        root = tk.Tk()
        root.title("App")
        root.geometry("600x500")
        return root

    def start_app(self):
        self.build_ui()
        self.window.mainloop()

    def build_ui(self):
        self.button_load_xls = self.build_button_source_xls_load()
        self.table_source_view = self.build_table_source_file_view()

    def build_button_source_xls_load(self):
        button = tk.Button(
            self.window,
            text="Load file",
            command=self.load_table_from_source
            )
        button.pack(pady=10)

        return button
    
    def build_table_source_file_view(self):
        table = ttk.Treeview(self.window)
        table.pack(expand=True, fill="both", padx=10, pady=10)

        return table

    def load_table_from_source(self):
        filepath = self.get_filepath()
        raw_data = DataImporter.load_xls(filepath)
        data = SoureActExtractor.standartize_input(raw_data)
        self.fill_table(data)
        self.calculate_debts(data)

    def get_filepath(self):
        return filedialog.askopenfilename(
            title="Choose file",
            initialdir=Path.home(),
            filetypes=[("Excel", ("*.xls")), ("All types", "*")]
        )

    def fill_table(self, data: pd.DataFrame):
        self.table_source_view.delete(*self.table_source_view.get_children())

        table_columns = list(data.columns)

        self.table_source_view["columns"] = table_columns
        self.table_source_view["show"] = "headings"

        self.table_source_view.tag_configure('oddrow', background='#E8E8E8')
        self.table_source_view.tag_configure('evenrow', background='#FFFFFF')

        for col in data.columns:
            self.table_source_view.heading(col, text=col)
            self.table_source_view.column(col, anchor="center", width=100)

        for i, (_, row) in enumerate(data.iterrows()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.table_source_view.insert("", tk.END, values=list(row), tags=(tag,))
