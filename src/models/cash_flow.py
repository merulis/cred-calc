from dataclasses import dataclass

from decimal import Decimal
from datetime import datetime


@dataclass
class CashFlow:
    """
    Структура описываюшая поток средств (outflow и inflow).

    Атрибуты:
        name (str): Имя документа, описывающий поток;
        date (datetime): Дата в физическом документе;
        amount (Decimal): Сумма средств указанная в документе;
    """
    name: str
    date: datetime
    amount: Decimal

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))

        if not isinstance(self.date, datetime):
            self.date = datetime.strptime(self.date, "%d.%m.%y")
