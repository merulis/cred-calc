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
                