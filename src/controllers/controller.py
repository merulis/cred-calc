import pandas

from decimal import Decimal

from src.views.mainView import MainView
from src.views.resultView import ResultView

from src.actValidator import ActValidator
from src.settlementCalculator import SettlementCalculator

from src.exporter.xlsExporter import XlsExporter
from src.extractors.actExtractorFactory import ActExtractorFactory


class Controller:
    def __init__(self, root):
        self.main_view = MainView(root)
        self.main_view.on_load = self.load_data
        self.main_view.on_calculate = self.run_calculations

        self.act_validator = ActValidator()
        self.extractor_factory = ActExtractorFactory()

        self.calc = SettlementCalculator()

        self.debits = None
        self.credits = None

    def clean_controller(self) -> None:
        if self.debits:
            self.debits = None
        if self.credits:
            self.credits = None

    def load_data(self) -> None:
        filename = self.main_view.ask_load_path()
        df = pandas.read_excel(filename)

        act_type = self.act_validator.validate(df)
        extractor = self.extractor_factory.create_extractor(act_type)
        
        self.debits, self.credits = extractor.extract(df)
        self.render_table()

    def render_table(self) -> None:
        self.main_view.clean_tables()

        for d in self.debits:
            self.main_view.insert_debit(
                (d.date.strftime("%d.%m.%Y"), d.name, str(d.amount))
            )
        for c in self.credits:
            self.main_view.insert_credit(
                (c.date.strftime("%d.%m.%Y"), c.name, str(c.amount))
            )

    def run_calculations(self, bank_rate: Decimal, deadline: int) -> None:
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
        self.clean_controller()

    def save_results(self, results):
        filepath = self.result_view.ask_save_path()
        if filepath:
            XlsExporter.export_to_xls(results, filepath)

        self.main_view.show_message(f"Файл сохранен: {filepath}")
