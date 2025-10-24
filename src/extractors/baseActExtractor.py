from abc import ABC, abstractmethod
from collections import deque

import pandas as pd

from src.models import Debit, Credit, ActColumns


class BaseActExtractor(ABC):
    COLUMNS = ActColumns()

    def extract(
        self,
        df,
    ) -> tuple[deque[Debit], list[Credit]]:
        """
        Template Method:
        share algorithm of unpacking xls act
        """
        if df is None:
            raise ValueError("Expect not NoneType object")

        normalize_df = self._normalize(df)
        renamed_df = self.rename_df(normalize_df)
        debits_df, credits_df = self._split_df(renamed_df)
        return (
            self._unpack_debits(debits_df),
            self._unpack_credits(credits_df),
        )

    def rename_df(self, df) -> pd.DataFrame:
        standart_columns = self.COLUMNS.to_dict()
        old_columns = list(df.columns)
        rename_columns = {}

        if len(standart_columns) != 4:
            raise ValueError(
                f"Expected count headers: {len(standart_columns)}, passed: {len(standart_columns)}"
            )

        for k, v in standart_columns.items():
            rename_columns.update({old_columns[k]: v})

        return df.rename(columns=rename_columns)

    @abstractmethod
    def _normalize(self, df) -> pd.DataFrame:
        """
        Абстрактный шаг — зависит от конкретного формата акта.

        К сожалению, в нем нужно привести имена столбцов к стандартому
        из атрибута cls.COLUMN.

        Нужно будет немного отрефакторить этот момент.
        Убрать нормализацию в общие методы.
        Парсинг сделать абстрактным шагом.
        """
        pass

    def _split_df(
        self,
        data: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        return: tuple(debits: DataFrame, credits: DataFrame)
        """
        debits_df = data[(data[self.COLUMNS.debit] > 0)].copy()
        debits_df = debits_df.drop(columns=[self.COLUMNS.credit])
        debits_df[self.COLUMNS.date] = pd.to_datetime(
            debits_df[self.COLUMNS.date], format="%d.%m.%y"
        )

        credits_df = data[(data[self.COLUMNS.credit] > 0)].copy()
        credits_df = credits_df.drop(columns=[self.COLUMNS.debit])

        return (debits_df, credits_df)

    def _unpack_credits(self, credits_df) -> list[Credit]:
        credits = []
        for _, row in credits_df.iterrows():
            credit = Credit(
                name=row.get(self.COLUMNS.name),
                date=row.get(self.COLUMNS.date),
                amount=row.get(self.COLUMNS.credit),
            )
            credits.append(credit)
        return credits

    def _unpack_debits(self, debits_df: pd.DataFrame) -> deque[Debit]:
        debits_dq = deque()
        for _, row in debits_df.iterrows():
            debit = row.to_dict()
            debits_dq.append(
                Debit(
                    name=debit.get(self.COLUMNS.name),
                    date=debit.get(self.COLUMNS.date),
                    amount=debit.get(self.COLUMNS.debit),
                )
            )
        return debits_dq
