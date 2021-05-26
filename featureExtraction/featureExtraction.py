from model.database.dataset import DataSetDTO
from model.HereApiResult import HereApiResult
from interface.repository import IRepository
from interface.graph import IGraph
from interface.featureExtraction import IFeatureExtraction, ID
from model.featureExtraction.input import APIInput
from model.featureExtraction.feature import Feature
from typing import List, Tuple, Dict
from repository.dataSet import QueryOption
from datetime import datetime

class FeatureExtraction(IFeatureExtraction):
    APIInputs: Dict[ID, APIInput]
    featureRepo: IRepository
    graph: IGraph
    def __init__(self, data: Dict[ID, APIInput], repo: IRepository, graph: IGraph):
        self.APIInputs = data
        self.featureRepo = repo
        self.graph = graph

    def processInput(self, x: List[APIInput]):


        return 1

    def saveToDB(self, id: ID, features: List[Feature], su: List[float]):
        self.featureRepo.save(features)

    def calJamFactorDuration(self, id:ID) -> float:
        jamFactorDuration = 0
        apiInput: APIInput = self.APIInputs[id]
        queryOption: QueryOption = QueryOption()
        queryOption.setOption(QueryOption.Latest, "true")
        latestDataSet: DataSetDTO = self.featureRepo.find(id, queryOption)[0]
        currentDate = self._praseRFCtimeToDatetime(apiInput.DateTime)
        latestDate = self._praseRFCtimeToDatetime(latestDataSet.TimeStamp)

        if self._getMinuteDelta(currentDate, latestDate) <= 10:
            if self._isJamFactorExceedThreshold(latestDataSet.JamFactor, apiInput.JamFactor):
                jamFactorDuration = 0
            else:
                jamFactorDuration = self._getMinuteDelta(currentDate, latestDate) + latestDataSet.JamFactorDuration
        else:
            jamFactorDuration = None

        return jamFactorDuration

    def _praseRFCtimeToDatetime(self, dateStr: str) -> datetime:
        
    
        # dateStr = "21 June, 2018"
        # 2021-05-09T05:56:31Z
        # %Y-%d-%mT%H:%M:%SZ
        date_object = datetime.strptime(dateStr, "%Y-%d-%mT%H:%M:%SZ")
        return date_object

    def _getMinuteDelta(self, currentTime: datetime, prevTime: datetime) -> int:
        return (currentTime - prevTime).total_seconds() / 60

    def _isJamFactorExceedThreshold(self, prevJF, currentJF) -> bool:
        prevJFState = int(prevJF)
        upperBound = prevJFState + 1.15
        lowerBound = prevJFState - .15
        return currentJF > upperBound or currentJF < lowerBound

#   def _calDeltaJamFactor(self, id:ID, ) -> float:

    def calNeightbourJamFactor(self, id:ID) -> float:
        v = 0
        neighbours = self.graph.getNodeByID(id).getNeighbourNodes()
        for neightbour in neighbours:
            v += self.APIInputs[neightbour.getID()].JamFactor
        return v / len(neighbours)

#   def _calNeightbourJamFactorDuration(self, id:ID) -> float:
#       may be call _calNeightbourJamFactor()
#       use graph dependency


    # DayOfWeek: int
    # Day: int
    # Hour: int
    # Minute: int
    # JamFactor: float
    # JamFactorDuration: int
    # DeltaJamFactor: int
    # NeightbourJamFactor: float
    # NeightbourJamFactorDuration: int
    # TimeStamp: str
