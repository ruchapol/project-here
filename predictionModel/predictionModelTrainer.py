from model.database.model import ModelDTO
from model.database.dataset import DataSetDTO
from repository.dataSet import QueryOption
from model.database.roadSegment import RoadSegmentDTO
from model.ID import ID
from typing import Dict, List, Tuple
from interface.repository import IRepository
from interface.predictionModel import IPredictionModel
from interface.modelDTOMapper import IModelDTOMapper
import statistics
from utils.date import parseRFCtimeToDatetime
import pickle
class PredictionModelTrainer:
    roadSegmentRepo: IRepository
    datasetRepo: IRepository
    modelRepo: IRepository
    predictionModel :IPredictionModel
    modelDTOMapper :IModelDTOMapper
    def __init__(self, roadSegmentRepo: IRepository, datasetRepo: IRepository, 
                 modelRepo: IRepository, predictionModel: IPredictionModel,
                 modelDTOMapper: IModelDTOMapper):
        self.roadSegmentRepo = roadSegmentRepo
        self.datasetRepo = datasetRepo
        self.modelRepo = modelRepo
        self.predictionModel = predictionModel
        self.modelDTOMapper = modelDTOMapper

    def train(self):
        roadSegments: Dict[ID, RoadSegmentDTO] = self.roadSegmentRepo.findAll()
        for roadID in roadSegments:
            # print(roadId)
            datasets: List[DataSetDTO] = self.datasetRepo.find(roadID)
            (x,y,t) = self._dataSetDTOListToXY(datasets)
            self._fillAverageIfNone((x,y))
            if len(x) == 0:
                continue
            self.predictionModel.train(x, y, t)
            modelDTO = self.modelDTOMapper.classToModelDTO(self.predictionModel)
            self.saveToDB(roadID, modelDTO)

    def _fillAverageIfNone(self, xy: Tuple[List,List]):
        x = xy[0]
        if len(x) == 0:
            return None
        mean = [0]*len(x[0])
        featureNum = len(x[0])
        rowNum = len(x)
        for f in range(featureNum):
            featureValues = [x[n][f] for n in range(rowNum) if x[n][f] != None]
            mean[f] = statistics.mean(featureValues) if len(featureValues) > 0 else 0
        for n in range(rowNum):
            x[n] = [x[n][f] if x[n][f] is not None else mean[f] for f in range(featureNum)]
        return xy
        
    def _dataSetDTOListToXY(self, datasets: List[DataSetDTO]) -> Tuple[List,List,List]:
        xyt = ([],[],[])
        for dataset in datasets:
            x = []
            x.append(dataset.DayOfWeek)
            x.append(dataset.Day)
            x.append(dataset.Hour)
            x.append(dataset.Minute)
            x.append(dataset.JamFactor)
            x.append(dataset.JamFactorDuration)
            x.append(dataset.DeltaJamFactor)
            x.append(dataset.NeightbourJamFactor)
            x.append(dataset.NeightbourJamFactorDuration)
            xyt[0].append(x)
            xyt[1].append(dataset.SpeedUncut)
            xyt[2].append(parseRFCtimeToDatetime(dataset.TimeStamp))
        return xyt    

    def saveToDB(self,id: ID, model: ModelDTO):
        self.modelRepo.save(id, model)