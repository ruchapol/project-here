import unittest
from predictionModel.predictionModelTrainer import PredictionModelTrainer
from interface.repository import IRepository
from interface.predictionModel import IPredictionModel

class PredictionModelForTest(PredictionModelTrainer):

    def __init__(self, roadSegmentRepo: IRepository, datasetRepo: IRepository, modelRepo: IRepository, predictionModel: IPredictionModel):
        super().__init__(roadSegmentRepo, datasetRepo, modelRepo, predictionModel)