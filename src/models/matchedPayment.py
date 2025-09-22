from dataclasses import dataclass, field, fields
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


@dataclass
class MatchedPayment:
    debit_date: datetime = field(metadata={"title": "Дата дебета"})
    debit_amount: Decimal = field(metadata={"title": "Сумма дебета"})
    due_date: datetime = field(metadata={"title": "Срок оплаты"})
    credit_date: datetime = field(metadata={"title": "Дата оплаты"})
    paid: Decimal = field(metadata={"title": "Оплачено"})
    unpaid: Decimal = field(metadata={"title": "Остаток"})
    overdue_days: int = field(metadata={"title": "Дней просрочки"})
    penalty_base: Decimal = field(metadata={"title": "Неустойка"})
    penalty_additional: Decimal = field(metadata={"title": "Штрафная неустойка"})
    penalty_percent: Decimal = field(metadata={"title": "Проценты (317.1)"})

    def to_list(self) -> list:
        def q(val: Decimal) -> str:
            if isinstance(val, Decimal):
                return str(val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            return str(val)

        return [
            self.debit_date.strftime("%d.%m.%Y") if self.debit_date else None,
            q(self.debit_amount),
            self.due_date.strftime("%d.%m.%Y") if self.due_date else None,
            self.credit_date.strftime("%d.%m.%Y") if self.credit_date else None,
            q(self.paid),
            q(self.unpaid),
            self.overdue_days,
            q(self.penalty_base),
            q(self.penalty_additional),
            q(self.penalty_percent),
        ]

    @classmethod
    def headers(cls) -> list[str]:
        return [f.metadata.get("title", f.name) for f in fields(cls)]
    
    @classmethod
    def names(cls) -> list[str]:
        return [f.name for f in fields(cls)]
    
    @classmethod
    def fields_map(cls) -> dict:
        return {f.name: f.metadata.get("title", f.name) for f in fields(cls)}
