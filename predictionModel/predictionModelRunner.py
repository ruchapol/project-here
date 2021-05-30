from model.database.dataset import DataSetDTO
from repository.dataSet import QueryOption
from model.database.roadSegment import RoadSegmentDTO
from model.ID import ID
from typing import Dict, List, Tuple
from interface.repository import IRepository
from interface.predictionModel import IPredictionModel
import statistics
from utils.date import parseRFCtimeToDatetime

class PredictionModelRunner:
    roadSegmentRepo: IRepository
    datasetRepo: IRepository
    thetaRepo: IRepository
    predictionModel :IPredictionModel
    def __init__(self, roadSegmentRepo: IRepository, datasetRepo: IRepository, predictionModel: IPredictionModel):
        self.roadSegmentRepo = roadSegmentRepo
        self.datasetRepo = datasetRepo
        self.predictionModel = predictionModel

    def train(self):
        roadSegments: Dict[ID, RoadSegmentDTO] = self.roadSegmentRepo.findAll()
        c = 0
        for roadId in roadSegments:
            print(roadId)
            datasets: List[DataSetDTO] = self.datasetRepo.find(roadId)
            (x,y,t) = self._dataSetDTOListToXY(datasets)
            self._fillAverageIfNone((x,y))
            if len(x) == 0:
                continue
            self.predictionModel.train(x, y, t)
            print(self.predictionModel.predict(x[:1]))
            c+=1
            if c==2:
                break

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
        
    def _dataSetDTOListToXY(self, datasets: List[DataSetDTO]) -> Tuple[List,List]:
        xy = ([],[],[])
        for dataset in datasets:
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
            xy[0].append(x)
            xy[1].append(dataset.SpeedUncut)
            xy[2].append(parseRFCtimeToDatetime(dataset.TimeStamp))
        return xy    

    def saveToDB(self):
        pass