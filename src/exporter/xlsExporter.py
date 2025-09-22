import pandas as pd

class XlsExporter:
    def export_to_xls(result: list, filepath: str):
        df = pd.DataFrame([r.to_list() for r in result], columns=)