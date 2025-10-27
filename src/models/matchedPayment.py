from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta

from src.models import CashFlow

type DayCount = int

class MatchedPayment:
    def __init__(self, outflow: CashFlow, inflow: CashFlow, deadline: DayCount,):
        self.outflow = outflow
        self.inflow = inflow
        self.deadline = deadline

        self.due_date = self.outflow + timedelta(days=self.deadline)
        self.overdue_days = max((self.inflow.date - self.due_date).days, 0)

    def amount_matching(
        self,
    ) -> Decimal:
        matched_amount = min(self.outflow.amount, self.inflow.amount)
        self.outflow.amount -= matched_amount
        self.inflow.amount -= matched_amount
        return matched_amount

    def calculate_base_penalty(
        inflow_amount: Decimal,
        overdue_days: int,
        penalty_rate=0.5,
    ) -> Decimal:
        return inflow_amount * (Decimal(penalty_rate) / Decimal(100)) * Decimal(overdue_days)

    def calculate_additionaly_penalty(
        self,
        inflow_amount: Decimal,
        penalty_rate=10,
    ) -> Decimal:
        return inflow_amount * (Decimal(penalty_rate) / Decimal(100))

    def calculate_percent_penalty(
        self,
        inflow_amount: Decimal,
        overdue_days: int,
        bank_rate: Decimal,
    ) -> Decimal:
        return (
            inflow_amount
            * (Decimal(bank_rate) / Decimal(100))
            * Decimal(overdue_days)
            / Decimal(365)
        )

    def to_tuple(self):
        pass
