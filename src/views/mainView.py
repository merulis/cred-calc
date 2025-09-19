import tkinter as tk
from tkinter import filedialog, messagebox, ttk

MAIN_VIEW_COLUMNS: tuple[str, ...] = ("date", "name", "amount")

MAIN_VIEW_HEADERS: dict[str, str] = {
    "date": "Дата",
    "name": "Документ",
    "amount": "Сумма",
}


class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.on_load = None
        self.on_calculate = None

        self._create_top_panel()
        self._create_table()
        self._create_settings_frame()
        self._create_calc_button()

    def _create_top_panel(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=5)

        self.load_button = tk.Button(
            top_frame, text="Загрузить Excel", command=self._handle_load
        )
        self.load_button.pack(side="left")

    def _create_table(self):
        self.table = ttk.Treeview(
            self,
            columns=MAIN_VIEW_COLUMNS,
            show="headings",
        )

        for col in MAIN_VIEW_COLUMNS:
            self.table.heading(col, text=MAIN_VIEW_HEADERS[col])
            self.table.column(col, width=150, anchor="center")

        self.table.pack(fill="both", expand=True, pady=10)

    def _create_settings_frame(self):
        settings_frame = tk.LabelFrame(self, text="Настройки расчета")
        settings_frame.pack(fill="x", pady=5)

        tk.Label(settings_frame, text="Ставка ЦБ (%):").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.rate_var = tk.StringVar(value="16")
        tk.Entry(settings_frame, textvariable=self.rate_var, width=10).grid(
            row=0, column=1, padx=5, pady=2
        )

        tk.Label(settings_frame, text="Срок оплаты (дней):").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.deadline_var = tk.StringVar(value="7")
        tk.Entry(
            settings_frame,
            textvariable=self.deadline_var,
            width=10,
        ).grid(row=1, column=1, padx=5, pady=2)

        return settings_frame

    def _create_calc_button(self):
        self.calc_button = tk.Button(
            self, text="Рассчитать", command=self._handle_calculate
        )
        self.calc_button.pack(pady=10)

    def _handle_load(self):
        if self.on_load:
            filename = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            if filename:
                self.on_load(filename)

    def _handle_calculate(self):
        if self.on_calculate:
            try:
                rate = float(self.rate_var.get())
                deadline = int(self.deadline_var.get())
            except ValueError:
                tk.messagebox.showerror(
                    "Ошибка", "Введите корректные значения в настройках"
                )
                return
            self.on_calculate(rate, deadline)

    def insert_row(self, values: tuple):
        """Добавление строки в таблицу Excel"""
        self.table.insert("", "end", values=values)

    def show_message(self, text: str, title: str = "Информация"):
        messagebox.showinfo(title, text)
