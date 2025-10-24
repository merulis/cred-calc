import pandas as pd

from src.models.enum.actFileType import ActFileType

class ActValidator:
    def validate(self, act_df: pd.DataFrame) -> ActFileType:
        if act_df.iat[0, 1] == "Акт сверки":
            return ActFileType.ONEC
        elif len(act_df.loc[0].to_list()) == 4:
            return ActFileType.PREPARED