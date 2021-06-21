from predictionModel.predictionModel_v1 import PredictionModelV1
from interface.modelDTOMapper import IModelDTOMapper
from interface.predictionModel import IPredictionModel
from model.database.model import ModelDTO



class ModelDTOToLinearRegressionMock(IModelDTOMapper):
    def __init__(self, modelDTO: ModelDTO, predictionModel: IPredictionModel) -> None:
        self.modelDTO = modelDTO
        self.predictionModel = predictionModel

    def classToModelDTO(self, classes: IPredictionModel) -> ModelDTO:
        return self.modelDTO

    def modelDTOToClass(self, modelDTO: ModelDTO) -> IPredictionModel:
        return self.predictionModel
