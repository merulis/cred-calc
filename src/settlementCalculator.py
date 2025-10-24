from datetime import timedelta
from decimal import Decimal
from collections import deque

from src.models import Debit, Credit, MatchedPayment


class SettlementCalculator:
    @classmethod
    def make_settlement(
        cls,
        debits: deque[Debit],
        credits: list[Credit],
        deadline_days: int,
        bank_rate: Decimal,
        base_rate: Decimal,
    ) -> list[MatchedPayment]:
        result = []
        for credit in credits:
            while credit.amount > 0 and debits:
                debit = debits[0]

                matched_amount = cls._match_payment(debit, credit)

                due_date = debit.date + timedelta(days=deadline_days)
                overdue_days = max((credit.date - due_date).days, 0)

                base_p = cls._calculate_base_penalty(
                    matched_amount, overdue_days, base_rate
                )
                additionaly_p = cls._calculate_additionaly_penalty(
                    matched_amount,
                )
                percent_p = cls._calculate_percent_penalty(
                    matched_amount, overdue_days, bank_rate
                )

                record = MatchedPayment(
                    debit_date=debit.date,
                    debit_amount=matched_amount,
                    due_date=due_date,
                    credit_date=credit.date,
                    paid=matched_amount,
                    unpaid=credit.amount,
                    overdue_days=overdue_days,
                    penalty_base=base_p,
                    penalty_additional=additionaly_p,
                    penalty_percent=percent_p,
                )

                result.append(record)

                if debit.amount == 0:
                    debits.popleft()

        return result

    @staticmethod
    def _match_payment(debit: Debit, credit: Credit) -> Decimal:
        matched_amount = min(debit.amount, credit.amount)
        debit.amount -= matched_amount
        credit.amount -= matched_amount
        return matched_amount

    @staticmethod
    def _calculate_base_penalty(
        amount: Decimal,
        overdue_days: int,
        penalty_rate: Decimal,
    ) -> Decimal:
        return amount * (Decimal(penalty_rate) / Decimal(100)) * Decimal(overdue_days)

    @staticmethod
    def _calculate_additionaly_penalty(
        amount: Decimal,
        penalty_rate=90,
    ) -> Decimal:
        return amount * (Decimal(penalty_rate) / Decimal(100))

    @staticmethod
    def _calculate_percent_penalty(
        amount: Decimal,
        overdue_days: int,
        bank_rate: Decimal,
    ) -> Decimal:
        return (
            amount
            * (Decimal(bank_rate) / Decimal(100))
            * Decimal(overdue_days)
            / Decimal(365)
        )
