from dataclasses import dataclass


@dataclass(frozen=True)
class ActColumns:
    date: str = "date"
    name: str = "name"
    debit: str = "debit"
    credit: str = "credit"

    def to_list(self):
        return [
            self.date,
            self.name,
            self.debit,
            self.credit,
        ]

    def to_dict(self):
        return {
            0: self.date,
            1: self.name,
            2: self.debit,
            3: self.credit,
        }
