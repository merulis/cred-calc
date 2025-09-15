from datetime import timedelta
from decimal import Decimal
from collections import deque

from src.struct.debit import Debit
from src.struct.credit import Credit
from src.struct.matchedPayment import MatchedPayment


class SettlementCalculator:

    @staticmethod
    def make_settlement(
        debits: deque[Debit],
        credits: list[Credit],
        deadline_days: int,
    ) -> list:
        result = []
        for credit in credits:
            
            while credit > 0 and debits:
                debit = debits[0]
                credit_paid = credit.amount
                
                SettlementCalculator._match_payment(debit, credit)

                due_date = debit.date + timedelta(days=deadline_days)
                overdue_days = max((credit.date - due_date).days, 0)       

                penalties = SettlementCalculator._counting_of_penalties(
                    credit=credit_paid,
                    overdue_days=overdue_days
                )

                result.append(
                    MatchedPayment(
                        debit_date=debit.date,
                        debit_amount=debit.amount,
                        credit_date=credit.date,
                        paid=credit_paid,
                        unpaid=credit.amount,
                        overdue_days=overdue_days,
                        penalty_base=penalties[0],
                        penalty_additional=penalties[1],
                        penalty_percent=penalties[2]
                    )
                )

        return result

    @staticmethod
    def _match_payment(debit: Debit, credit: Credit):
        matched_amount = min(debit.amount, credit.amount)

        debit.amount -= matched_amount
        credit.amount -= matched_amount

    @staticmethod
    def _counting_of_penalties(
            credit: Credit, 
            overdue_days: int
    ):
        return (
            SettlementCalculator._calculate_base_penalty(credit, overdue_days),
            SettlementCalculator._calculate_additionaly_penalty(credit),
            SettlementCalculator._calculate_percent_penalty(credit, overdue_days),
        )

    @staticmethod
    def _calculate_base_penalty(
            credit_amount: Decimal, 
            overdue_days: int, 
            penalty_rate=0.5
    ) -> Decimal:
        return credit_amount * (penalty_rate / 100) * overdue_days 

    @staticmethod
    def _calculate_additionaly_penalty( 
            amount: Decimal, 
            penalty_rate=90
    ) -> Decimal:
        return amount * (penalty_rate / 100)

    @staticmethod
    def _calculate_percent_penalty(
            amount: Decimal, 
            overdue_days: int, 
            bank_rate: int = 16
    ) -> Decimal:
        return amount * (bank_rate / 100) * overdue_days / 365
