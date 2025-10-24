from src.models.enum.actFileType import ActFileType

from src.extractors.baseActExtractor import BaseActExtractor
from src.extractors.ONECActExtractor import ONECActExtractor
from src.extractors.preparedActExtractor import PreparedActExtractor


class ActExtractorFactory:
    def create_extractor(self, file_type: ActFileType) -> BaseActExtractor:
        if file_type == ActFileType.ONEC:
            return ONECActExtractor()
        elif file_type == ActFileType.PREPARED:
            return PreparedActExtractor()
        else:
            raise ValueError(f"Incorrect file type: {file_type}")
