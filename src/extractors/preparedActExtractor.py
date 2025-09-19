import pandas as pd

from src.extractors.baseXlsActExtractor import BaseXlsActExtractor


class PreparedActExtractor(BaseXlsActExtractor):
    @classmethod
    def _normalize(cls, filepath):
        df = pd.read_excel(filepath, header=None)
        df = df.rename(
            columns=cls.COLUMNS.to_dict(),
        )

        df["date"] = pd.to_datetime(
            df["date"],
            format="%d.%m.%y",
            errors="coerce",
        )

        return df
