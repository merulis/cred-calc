import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from decimal import Decimal


class MainView(tk.Frame):
    colunms: tuple[str, ...] = ("date", "name", "amount")

    headers: dict[str, str] = {
        "date": "Дата",
        "name": "Документ",
        "amount": "Сумма",
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self._on_load = None
        self._on_calculate = None

        self._create_load_panel()
        self._create_tables_frame()
        self._create_attributes_frame()
        self._create_calc_button()

    @property
    def on_load(self):
        return self._on_load

    @property
    def on_calculate(self):
        return self._on_calculate

    @on_load.setter
    def on_load(self, callback):
        self._on_load = callback
        self.load_button.config(command=self._on_load)

    @on_calculate.setter
    def on_calculate(self, callback):
        self._on_calculate = callback
        self.calc_button.config(command=self._call_calculate)

    def _call_load(self):
        if self._on_load:
            self._on_load()
        else:
            messagebox.showwarning("Внимание", "Обработчик загрузки не установлен")

    def _call_calculate(self):
        attrs = self.get_attributes()
        if attrs is None:
            return
        if not self._on_calculate:
            messagebox.showwarning("Внимание", "Обработчик расчёта не установлен")
            return
        rate, deadline = attrs
        self._on_calculate(rate, deadline)

    def _create_load_panel(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=5)

        self.load_button = tk.Button(
            top_frame, text="Загрузить Excel", command=self._call_load
        )
        self.load_button.pack(side="left")

    def _create_tables_frame(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, pady=10)

        self.debit_table = ttk.Treeview(
            frame,
            columns=("date", "name", "amount"),
            show="headings",
            height=15,
        )

        for col in self.colunms:
            self.debit_table.heading(col, text=self.headers[col])
            self.debit_table.column(col, width=150, anchor="center")

        self.debit_table.tag_configure("oddrow", background="#e0e0e0")
        self.debit_table.tag_configure("evenrow", background="#ffffff")
        self.debit_table.pack(side="left", fill="both", expand=True, padx=5)

        self.credit_table = ttk.Treeview(
            frame,
            columns=("date", "name", "amount"),
            show="headings",
            height=15,
        )

        for col in self.colunms:
            self.credit_table.heading(col, text=self.headers[col])
            self.credit_table.column(col, width=150, anchor="center")

        self.credit_table.tag_configure("oddrow", background="#e0e0e0")
        self.credit_table.tag_configure("evenrow", background="#ffffff")
        self.credit_table.pack(side="right", fill="both", expand=True, padx=5)

    def _create_attributes_frame(self):
        attributes_frame = tk.LabelFrame(self, text="Настройки расчета")
        attributes_frame.pack(fill="x", pady=5)

        tk.Label(attributes_frame, text="Ставка ЦБ (%):").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.rate_var = tk.StringVar(value="16")
        tk.Entry(attributes_frame, textvariable=self.rate_var, width=10).grid(
            row=0, column=1, padx=5, pady=2
        )

        tk.Label(attributes_frame, text="Срок оплаты (дней):").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.deadline_var = tk.StringVar(value="7")
        tk.Entry(
            attributes_frame,
            textvariable=self.deadline_var,
            width=10,
        ).grid(row=1, column=1, padx=5, pady=2)

        return attributes_frame

    def _create_calc_button(self):
        self.calc_button = tk.Button(
            self, text="Рассчитать", command=self._call_calculate
        )
        self.calc_button.pack(pady=10)

    def ask_load_path(self) -> str:
        return filedialog.askopenfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xls *.xlsx")]
        )

    def get_attributes(self) -> tuple[Decimal, int]:
        try:
            rate = Decimal(self.rate_var.get())
            deadline = int(self.deadline_var.get())
        except ValueError:
            messagebox.showerror("Error", "Incorrect attributs value")
        return (rate, deadline)

    def clean_tables(self):
        for row in self.debit_table.get_children():
            self.debit_table.delete(row)

        for row in self.credit_table.get_children():
            self.credit_table.delete(row)

    def insert_debit(self, values: tuple):
        index = len(self.debit_table.get_children())
        tag = "evenrow" if index % 2 == 0 else "oddrow"
        self.debit_table.insert("", "end", values=values, tags=(tag,))

    def insert_credit(self, values: tuple):
        index = len(self.credit_table.get_children())
        tag = "evenrow" if index % 2 == 0 else "oddrow"
        self.credit_table.insert("", "end", values=values, tags=(tag,))

    def show_message(self, text: str, title: str = "Информация"):
        messagebox.showinfo(title, text)
