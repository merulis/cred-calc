from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class MatchedPayment:
    debit_date: datetime
    debit_amount: Decimal
    due_date: datetime
    credit_date: datetime
    paid: Decimal
    unpaid: Decimal
    overdue_days: int
    penalty_base: Decimal
    penalty_additional: Decimal
    penalty_percent: Decimal

    def to_list(self) -> list:
        return [
            self.debit_date.strftime("%d.%m.%Y") if self.debit_date else None,
            str(self.debit_amount),
            self.due_date.strftime("%d.%m.%Y") if self.due_date else None,
            self.credit_date.strftime("%d.%m.%Y") if self.credit_date else None,
            str(self.paid),
            str(self.unpaid),
            self.overdue_days,
            str(self.penalty_base),
            str(self.penalty_additional),
            str(self.penalty_percent),
        ]
