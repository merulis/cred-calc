from collections import deque
from decimal import Decimal
from datetime import datetime

from src.settlementCalculator import SettlementCalculator
from src.models import Debit, CashFlow, MatchedPayment


def make_debit(name: str, date: str, amount: str) -> Debit:
    return Debit(
        name=name,
        date=datetime.strptime(date, "%d.%m.%y"),
        amount=Decimal(amount),
    )


def make_credit(name: str, date: str, amount: str) -> CashFlow:
    return CashFlow(
        name=name,
        date=datetime.strptime(date, "%d.%m.%y"),
        amount=Decimal(amount),
    )


def test_full_payment_no_overdue():
    debits = deque([make_debit("Реализация", "01.01.24", "1000")])
    credits = [make_credit("Оплата", "05.01.24", "1000")]

    results = SettlementCalculator.make_settlement(
        debits=debits,
        credits=credits,
        deadline_days=7,
        bank_rate=Decimal("16"),
    )

    assert len(results) == 1
    payment = results[0]
    assert isinstance(payment, MatchedPayment)
    assert payment.debit_amount == Decimal("1000")
    assert payment.paid == Decimal("1000")
    assert payment.unpaid == Decimal("0")
    assert payment.overdue_days == 0
    assert payment.penalty_base == Decimal("0")
    assert payment.penalty_additional == Decimal("900")  # 1000 * 0.9
    assert payment.penalty_percent == Decimal("0")


def test_partial_payment():
    debits = deque([make_debit("Реализация", "01.01.24", "1500")])
    credits = [make_credit("Оплата", "05.01.24", "1000")]

    results = SettlementCalculator.make_settlement(
        debits=debits,
        credits=credits,
        deadline_days=7,
        bank_rate=Decimal("16"),
    )

    assert len(results) == 1
    payment = results[0]
    assert payment.debit_amount == Decimal("1000")
    assert payment.paid == Decimal("1000")
    assert payment.unpaid == Decimal("0")  # кредит закрыт
    # остаток дебета должен быть 500
    assert debits[0].amount == Decimal("500")


def test_with_overdue_days():
    debits = deque([make_debit("Реализация", "01.01.24", "1000")])
    # кредит только 20 января → просрочка 12 дней
    credits = [make_credit("Оплата", "20.01.24", "1000")]

    results = SettlementCalculator.make_settlement(
        debits=debits,
        credits=credits,
        deadline_days=7,
        bank_rate=Decimal("16"),
    )

    payment = results[0]
    assert payment.overdue_days > 0
    assert payment.penalty_base > 0
    assert payment.penalty_percent > 0


def test_decimal_precision():
    debits = deque([make_debit("Реализация", "01.01.24", "1234.56")])
    credits = [make_credit("Оплата", "05.01.24", "1234.56")]

    results = SettlementCalculator.make_settlement(
        debits=debits,
        credits=credits,
        deadline_days=7,
        bank_rate=Decimal("16"),
    )

    payment = results[0]
    assert isinstance(payment.debit_amount, Decimal)
    assert isinstance(payment.paid, Decimal)
    assert isinstance(payment.penalty_base, Decimal)
    assert isinstance(payment.penalty_percent, Decimal)
