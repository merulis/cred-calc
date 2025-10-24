from src.extractors.baseActExtractor import BaseActExtractor


class PreparedActExtractor(BaseActExtractor):
    def _normalize(self, df):
        return df
