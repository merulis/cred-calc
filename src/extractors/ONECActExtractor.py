import pandas as pd

from src.models.enum.ONECActConfig import ONECActConfig

from src.extractors.baseActExtractor import BaseActExtractor


class ONECActExtractor(BaseActExtractor):
    def _normalize(self, df) -> pd.DataFrame:
        headers = ONECActConfig.HEADERS
        diff = ONECActConfig.DIFF_FROM_BLANK_TARGET
        start = ONECActConfig.START_COLUMN
        end = ONECActConfig.END_COLUMN

        df = df.iloc[headers:]

        blank_row_index = (
            df[df.isnull().all(axis=1)].index[0] - diff
        )
        df = df.iloc[:blank_row_index, start:end]
        df = df.dropna(axis=1, how="all").fillna(0)

        standart_columns = self.COLUMNS.to_dict()
        old_columns = list(df.columns)
        rename_columns = {}

        for k, v in standart_columns.items():
            rename_columns.update({old_columns[k]: v})

        df.rename(
            columns=self.COLUMNS.to_dict(),
            inplace=True
        )

        return df
