from abc import ABC, abstractmethod
from collections import deque

import pandas as pd

from src.struct.debit import Debit
from src.struct.credit import Credit
from src.enum.xlsAct import XlsColumns


class BaseXlsActExtractor(ABC):
    @classmethod
    def unpack(
        cls,
        raw_data: pd.DataFrame,
    ) -> tuple[deque[Debit], list[Credit]]:
        """
        Template Method:
        share algorithm of unpacking xls act
        """
        debits_df, credits_df = cls._split_df(cls._normalize(raw_data))
        return (
            cls._unpack_debits(debits_df),
            cls._unpack_credits(credits_df),
        )

    @abstractmethod
    def _normalize(self, raw_data):
        """Абстрактный шаг — зависит от конкретного формата акта"""
        pass

    @staticmethod
    def _split_df(
        data: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        return: tuple(debits: DataFrame, credits: DataFrame)
        """
        debits_df = data[(data[XlsColumns.DEBIT_AMOUNT] > 0)].copy()
        debits_df = debits_df.drop(columns=[XlsColumns.CREDIT_AMOUNT])
        debits_df[XlsColumns.DATE] = pd.to_datetime(
            debits_df[XlsColumns.DATE], format="%d.%m.%y"
        )

        credits_df = data[(data[XlsColumns.CREDIT_AMOUNT] > 0)].copy()
        credits_df = credits_df.drop(columns=[XlsColumns.DEBIT_AMOUNT])

        return (debits_df, credits_df)

    @staticmethod
    def _unpack_credits(credits_df) -> list[Credit]:
        credits = []
        for _, row in credits_df.iterrows():
            credit = Credit(
                name=row.get(XlsColumns.NAME),
                date=row.get(XlsColumns.DATE),
                amount=row.get(XlsColumns.CREDIT_AMOUNT),
            )
            credits.append(credit)
        return credits

    @staticmethod
    def _unpack_debits(debits_df: pd.DataFrame) -> deque[Debit]:
        debits_dq = deque()
        for _, row in debits_df.iterrows():
            debit = row._as_dict()
            debits_dq.append(
                Debit(
                    name=debit.get(XlsColumns.NAME),
                    date=debit.get(XlsColumns.DATE),
                    amount=debit.get(XlsColumns.DEBIT_AMOUNT),
                )
            )
        return debits_dq
