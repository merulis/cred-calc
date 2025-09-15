import pandas as pd

from src.enum.xlsAct import ActConfig, XlsColumns
from src.extractors.BaseXlsActExtractor import BaseXlsActExtractor


class StandartActExtractor(BaseXlsActExtractor):
    @staticmethod
    def _normalize(raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_data = raw_data.iloc[ActConfig.HEADERS:]
        blank_row_index = (
            raw_data[raw_data.isnull().all(axis=1)].index[0]
            - ActConfig.DIFF_FROM_BLANK_TARGET
        )
        raw_data = raw_data.iloc[
            :blank_row_index, ActConfig.START_COLUMN:ActConfig.END_COLUMN
        ]
        data = raw_data.dropna(axis=1, how="all").fillna(0)

        data.columns = list(XlsColumns)

        return data
