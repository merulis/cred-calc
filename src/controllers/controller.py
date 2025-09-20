from decimal import Decimal

from src.views.mainView import MainView
from src.views.resultView import ResultView

from src.settlementCalculator import SettlementCalculator

from src.extractors.preparedActExtractor import PreparedActExtractor


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

        result_view = ResultView(self.main_view)
        for r in results:
            result_view.insert_row(r.to_list())

        result_view.save_button.config(
            command=lambda: self.save_results(results),
        )

    def save_results(self, results):
        print("Сохраняем результаты:", results)
