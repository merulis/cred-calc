from abc import ABC, abstractmethod
from collections import deque

import pandas as pd

from src.models import Debit, Credit, ActColumns


class BaseXlsActExtractor(ABC):
    COLUMNS = ActColumns()

    @classmethod
    def unpack(
        cls,
        filepath,
    ) -> tuple[deque[Debit], list[Credit]]:
        """
        Template Method:
        share algorithm of unpacking xls act
        """
        debits_df, credits_df = cls._split_df(cls._normalize(filepath))
        return (
            cls._unpack_debits(debits_df),
            cls._unpack_credits(credits_df),
        )

    @classmethod
    @abstractmethod
    def _normalize(cls, filepath) -> pd.DataFrame:
        """
            Абстрактный шаг — зависит от конкретного формата акта.

            К сожалению, в нем нужно привести имена столбцов к стандартому
            из атрибута cls.COLUMN.

            Нужно будет немного отрефакторить этот момент.
            Убрать нормализацию в общие методы.
            Парсинг сделать абстрактным шагом.
        """
        pass

    @classmethod
    def _split_df(
        cls,
        data: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        return: tuple(debits: DataFrame, credits: DataFrame)
        """
        debits_df = data[(data[cls.COLUMNS.debit] > 0)].copy()
        debits_df = debits_df.drop(columns=[cls.COLUMNS.credit])
        debits_df[cls.COLUMNS.date] = pd.to_datetime(
            debits_df[cls.COLUMNS.date], format="%d.%m.%y"
        )

        credits_df = data[(data[cls.COLUMNS.credit] > 0)].copy()
        credits_df = credits_df.drop(columns=[cls.COLUMNS.debit])

        return (debits_df, credits_df)

    @classmethod
    def _unpack_credits(cls, credits_df) -> list[Credit]:
        credits = []
        for _, row in credits_df.iterrows():
            credit = Credit(
                name=row.get(cls.COLUMNS.name),
                date=row.get(cls.COLUMNS.date),
                amount=row.get(cls.COLUMNS.credit),
            )
            credits.append(credit)
        return credits

    @classmethod
    def _unpack_debits(cls, debits_df: pd.DataFrame) -> deque[Debit]:
        debits_dq = deque()
        for _, row in debits_df.iterrows():
            debit = row.to_dict()
            debits_dq.append(
                Debit(
                    name=debit.get(cls.COLUMNS.name),
                    date=debit.get(cls.COLUMNS.date),
                    amount=debit.get(cls.COLUMNS.debit),
                )
            )
        return debits_dq
