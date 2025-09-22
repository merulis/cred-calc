import pandas as pd

from src.models import MatchedPayment

class XlsExporter:
    def export_to_xls(result: list, filepath: str):
        df = pd.DataFrame([r.to_list() for r in result], columns=MatchedPayment.headers())
        df.to_excel(filepath, index=False)