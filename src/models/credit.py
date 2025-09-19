from dataclasses import dataclass

from decimal import Decimal
from datetime import datetime


@dataclass
class Credit:
    """
    Структура описываюшая кредит.

    Атрибуты:
        name (str): Имя документа, где описан дебет (платежное поручение);
        date (datetime): Дата в физическом документе;
        amount (Decimal): Сумма полученная по документам;
    """
    name: str
    date: datetime
    amount: Decimal

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))

        if not isinstance(self.date, datetime):
            self.date = datetime.strptime(self.date, "%d.%m.%y")
