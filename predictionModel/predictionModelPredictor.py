from model.database.model import ModelDTO
from model.database.dataset import DataSetDTO
from repository.dataSet import QueryOption
from model.database.roadSegment import RoadSegmentDTO
from model.ID import ID
from typing import Dict, List, Tuple
from interface.repository import IRepository
from interface.predictionModel import IPredictionModel
import statistics
from utils.date import parseRFCtimeToDatetime
import pickle
class PredictionModelPredictor:
    modelRepo: IRepository
    datasetRepo: IRepository
    predictionModel :IPredictionModel
    def __init__(self, modelRepo: IRepository,datasetRepo: IRepository, predictionModel: IPredictionModel):
        self.modelRepo = modelRepo
        self.datasetRepo = datasetRepo
        self.predictionModel = predictionModel

    def predictFromNow(self, roadID: ID, minuteAhead: str) -> float:
        pass
            
            
