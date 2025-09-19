import pandas as pd

from enum.actConfig import ActConfig

from src.extractors.baseXlsActExtractor import BaseXlsActExtractor


class StandartActExtractor(BaseXlsActExtractor):
    @classmethod
    def _normalize(cls, filepath) -> pd.DataFrame:
        df = pd.read_excel(filepath, header=None)
        df = df.iloc[ActConfig.HEADERS:]
        blank_row_index = (
            df[df.isnull().all(axis=1)].index[0] - ActConfig.DIFF_FROM_BLANK_TARGET
        )
        df = df.iloc[:blank_row_index, ActConfig.START_COLUMN:ActConfig.END_COLUMN]
        df = df.dropna(axis=1, how="all").fillna(0)

        df = df.rename(
            columns=cls.COLUMNS.to_dict(),
        )

        return df
