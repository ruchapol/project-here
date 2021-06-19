from interface.predictionModel import IPredictionModel
from typing import Any
from model.database.model import ModelDTO


class IModelDTOMapper:
    def modelDTOToClass(self, model: ModelDTO) -> IPredictionModel:
        raise NotImplementedError

    def classToModelDTO(self, classes: IPredictionModel) -> ModelDTO:
        raise NotImplementedError
