from src.view.dummyView import DummyView


class DummyController:
    def __init__(self, view: DummyView):
        self.view = view
        self.view.on_load = self.on_load_file
        self.view.on_calculate = self.on_calculate

    def on_load_file(self):
        self.view.show_message("Нажата кнопка 'Загрузить'")
        self.view.insert_row(("A1", "B1", "C1"))

    def on_calculate(self):
        self.view.show_message("Нажата кнопка 'Рассчитать'")
        self.view.insert_row(("X1", "Y1", "Z1"))
