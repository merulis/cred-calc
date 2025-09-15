import pandas as pd

from collections import deque

from src.struct.debit import Debit
from src.struct.credit import Credit
from src.enum.xlsAct import ActConfig, XlsColumns


class SoureActExtractor:

    @staticmethod
    def standartize_input(raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_data = raw_data.iloc[ActConfig.HEADERS:]
        blank_row_index = raw_data[raw_data.isnull().all(axis=1)].index[0] - ActConfig.DIFF_FROM_BLANK_TARGET
        raw_data = raw_data.iloc[:blank_row_index, ActConfig.START_COLUMN:ActConfig.END_COLUMN]
        raw_data.insert(0, "N", range(1, len(raw_data) + 1))
        data = raw_data.dropna(axis=1, how="all").fillna(0)

        data.columns = list(XlsColumns)

        return data

    def build_calculation_base(
            data: pd.DataFrame
    ) -> tuple[deque[Debit], list[Credit]]:
        
        # FIXME: dont work
        
        debits = data[(data[XlsColumns.DEBIT] > 0)].copy()
        debits = debits.drop(columns=[XlsColumns.CREDIT])
        debits[XlsColumns.DATE] = pd.to_datetime(debits[XlsColumns.DATE], format="%d.%m.%y")
        debits_queue = deque(row._asdict() for row in debits.itertuples(index=False))

        credits = data[(data[XlsColumns.CREDIT] > 0)].copy()
        credits = credits.drop(columns=[XlsColumns.DEBIT])