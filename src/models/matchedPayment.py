from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


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
