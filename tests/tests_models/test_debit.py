from decimal import Decimal
from datetime import datetime

from src.models import Debit


def test_struct_debit_with_int_amount_and_str_date():
    d = Debit(name="Документ", date="01.01.25", amount=1245.02)

    assert isinstance(d.date, datetime)
    assert isinstance(d.amount, Decimal)


def test_struct_debit_with_decimal_amount_and_datetime_date():
    d = Debit(
        name="Документ",
        date=datetime(year=2025, month=1, day=1),
        amount=Decimal("1000.5"),
    )

    assert isinstance(d.date, datetime)
    assert isinstance(d.amount, Decimal)
    assert Decimal("1000.5") == d.amount
    assert datetime(year=2025, month=1, day=1) == d.date
