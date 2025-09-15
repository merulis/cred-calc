from enum import StrEnum, IntEnum


class XlsColumns(StrEnum):
    NUMBER = "Номер"
    DATE = "Дата"
    NAME = "Имя"
    DEBIT = "Дебет"
    CREDIT = "Кредит"

class ActConfig(IntEnum):
    HEADERS = 9
    START_COLUMN = 1
    END_COLUMN = 8