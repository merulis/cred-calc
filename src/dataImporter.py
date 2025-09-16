import pandas as pd


class DataImporter:
    @staticmethod
    def xls_to_df(xls_filepath):
        df = pd.read_excel(xls_filepath, header=None)
        return df
