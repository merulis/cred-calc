from enum import IntEnum


class ONECActConfig(IntEnum):
    """
        В очереди на выпил
    """
    HEADERS = 9
    START_COLUMN = 1
    END_COLUMN = 8
    DIFF_FROM_BLANK_TARGET = 11
