from decimal import Decimal

from src.views.mainView import MainView
from src.views.resultView import ResultView

from src.settlementCalculator import SettlementCalculator

from src.extractors.preparedActExtractor import PreparedActExtractor
from src.exporter.xlsExporter import XlsExporter


class Controller:
    def __init__(self, root):
        self.main_view = MainView(root)
        self.main_view.on_load = self.load_excel
        self.main_view.on_calculate = self.run_calculations

        self.calc = SettlementCalculator()

        self.debits = None
        self.credits = None

    def load_excel(self, filepath: str):
        self.debits, self.credits = PreparedActExtractor.unpack(filepath)

        self.main_view.clean_tables()

        for d in self.debits:
            self.main_view.insert_debit(
                (d.date.strftime("%d.%m.%Y"), d.name, str(d.amount))
            )
        for c in self.credits:
            self.main_view.insert_credit(
                (c.date.strftime("%d.%m.%Y"), c.name, str(c.amount))
            )

    def run_calculations(self, bank_rate: Decimal, deadline: int):
        if not (self.debits and self.credits):
            self.main_view.show_message("Нет данных для расчёта")
            return

        results = self.calc.make_settlement(
            self.debits,
            self.credits,
            deadline,
            bank_rate,
        )

        self.result_view = ResultView(self.main_view)
        for r in results:
            self.result_view.insert_row(r.to_list())

        self.result_view.on_save = lambda: self.save_results(results)

    def save_results(self, results):
        filepath = self.result_view.ask_save_path()
        if filepath:
            XlsExporter.export_to_xls(results, filepath)

        self.main_view.show_message(f"Файл сохранен: {filepath}")