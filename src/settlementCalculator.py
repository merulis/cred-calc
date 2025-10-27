from datetime import timedelta
from decimal import Decimal
from collections import deque

from src.models import CashFlow, MatchedPayment


class SettlementCalculator:
    def __init__(
        self,
        deadline_days: timedelta.days,
        base_penalty_rate: Decimal,
        bank_rate: Decimal,
    ):
        self.deadline_days = deadline_days
        self.base_penalty_rate = base_penalty_rate
        self.bank_rate = bank_rate

    def make_settlement(
        self,
        debits: deque[CashFlow],
        credits: list[CashFlow],
    ) -> list[MatchedPayment]:
        settlement = []
        for credit in credits:
            while credit.amount > 0 and debits:
                debit = debits[0]

                matched_amount = self.amount_matching(debit, credit)

                due_date = debit.date + timedelta(days=self.deadline_days)
                overdue_days = max((credit.date - due_date).days, 0)

                payment = MatchedPayment()

                settlement.append(payment)

                if debit.amount == 0:
                    debits.popleft()

        return settlement
