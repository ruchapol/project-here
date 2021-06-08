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

    def _datasetDTOtoX(self, dataset: DataSetDTO) -> List:
        x = []
        x.append(dataset.DayOfWeek)
        x.append(dataset.Day)
        x.append(dataset.Hour)
        x.append(dataset.Minute)
        x.append(dataset.JamFactor)
        x.append(dataset.NeightbourJamFactor)
        x.append(dataset.JamFactorDuration)
        x.append(dataset.DeltaJamFactor)
        x.append(dataset.NeightbourJamFactorDuration)
        return [x]

    def predictSpeedUncutFromNow(self, roadID: ID, minuteAhead: str) -> float:
        queryOption: QueryOption = QueryOption()
        queryOption.setOption(QueryOption.Latest, "true")
        latestDataSet: DataSetDTO = self.datasetRepo.find(roadID, queryOption)[0]
        predictionModelData: ModelDTO = self.modelRepo.find(roadID)
        self.predictionModel.load(predictionModelData)
        print(latestDataSet.toJSON())
        datasetX = self._datasetDTOtoX(latestDataSet)
        speedUncut = self.predictionModel.predict(datasetX)[minuteAhead]
        return speedUncut

            
            
