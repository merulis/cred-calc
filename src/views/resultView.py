import tkinter as tk
from tkinter import ttk

COLUMNS = (
    "debit_date",
    "debit_amount",
    "due_date",
    "credit_date",
    "paid",
    "unpaid",
    "overdue_days",
    "penalty_base",
    "penalty_additional",
    "penalty_percent",
)

HEADERS = {
    "debit_date": "Дата дебета",
    "debit_amount": "Сумма дебета",
    "due_date": "Срок оплаты",
    "credit_date": "Дата оплаты",
    "paid": "Оплачено",
    "unpaid": "Остаток от платежа",
    "overdue_days": "Дней просрочки",
    "penalty_base": "Баз. неустойка",
    "penalty_additional": "Штрафная неустойка",
    "penalty_percent": "Проценты (317.1)",
}


class ResultView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Результаты расчета")
        self.geometry("600x400")

        self._create_table()
        self._create_save_button()

    def _create_table(self):
        self.table = ttk.Treeview(
            self,
            columns=COLUMNS,
            show="headings",
        )

        for col in COLUMNS:
            self.table.heading(col, text=HEADERS[col])
            self.table.column(col, width=120, anchor="center")

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
