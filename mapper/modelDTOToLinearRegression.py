from interface.modelDTOMapper import IModelDTOMapper
from interface.predictionModel import IPredictionModel
from typing import Any, Dict
from model.database.model import ModelDTO
import pickle
from sklearn.linear_model import LinearRegression


class ModelDTOToLinearRegression(IModelDTOMapper):

    def _linearRegressionToModelDTO(self, predictionModel :IPredictionModel) -> ModelDTO:
        modelDTO = ModelDTO()
        modelDTO.Model_5 = pickle.dumps(predictionModel.getModel("5"))
        modelDTO.Model_15 = pickle.dumps(predictionModel.getModel("15"))
        modelDTO.Model_30 = pickle.dumps(predictionModel.getModel("30"))
        modelDTO.Model_45 = pickle.dumps(predictionModel.getModel("45"))
        modelDTO.Model_60 = pickle.dumps(predictionModel.getModel("60"))     
        return modelDTO

    def classToModelDTO(self, classes: IPredictionModel) -> ModelDTO:
        return self._linearRegressionToModelDTO(classes)

    def _modelDTOToLinearRegression(self, modelDTO: ModelDTO) -> IPredictionModel:
        linearRegression = {} # TODO: fix to IPredictionModel so predictionModelPredictor and predictionModelTrainer can use this.
        linearRegression["5"] = pickle.loads(modelDTO.Model_5)
        linearRegression["15"] = pickle.loads(modelDTO.Model_15)
        linearRegression["30"] = pickle.loads(modelDTO.Model_30)
        linearRegression["45"] = pickle.loads(modelDTO.Model_45)
        linearRegression["60"] = pickle.loads(modelDTO.Model_60)
        return linearRegression

    def modelDTOToClass(self, modelDTO: ModelDTO) -> IPredictionModel:
        return self._modelDTOToLinearRegression(modelDTO)
