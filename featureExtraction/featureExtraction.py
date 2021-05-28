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
    jamFactorDuration: Dict[ID, float]

    def __init__(self, data: Dict[ID, APIInput], repo: IRepository, graph: IGraph):
        self.APIInputs = data
        self.featureRepo = repo
        self.graph = graph
        self.jamFactorDuration = {}

    def processInput(self) -> List[DataSetDTO]:
        datasets: List[DataSetDTO] = []
        for id, apiInput in self.APIInputs.items():
            if self.graph.getNodeByID(id) is None:
                continue
            dataset: DataSetDTO = DataSetDTO() 
            dataset.ID = id
            dataset.Day = apiInput.getDay()
            dataset.DayOfWeek = apiInput.getDayOfWeek()
            dataset.DeltaJamFactor = self.calDeltaJamFactor(id)
            dataset.Hour = apiInput.getHour()
            dataset.Minute = apiInput.getMinute()
            dataset.JamFactor = apiInput.JamFactor
            dataset.JamFactorDuration = self.calJamFactorDuration(id)
            dataset.NeightbourJamFactor = self.calNeightbourJamFactor(id)
            dataset.NeightbourJamFactorDuration = self.calNeightbourJamFactorDuration(id)
            dataset.SpeedUncut = apiInput.SpeedUncut
            dataset.TimeStamp = apiInput.DateTime
            datasets.append(dataset)
        return datasets

    def saveToDB(self, dataSet: List[DataSetDTO]):
        self.featureRepo.save(dataSet)

    def calJamFactorDuration(self, id:ID) -> float:
        if id in self.jamFactorDuration:
            return self.jamFactorDuration[id]
        if id not in self.APIInputs:
            return None

        apiInput: APIInput = self.APIInputs[id]
        queryOption: QueryOption = QueryOption()
        queryOption.setOption(QueryOption.Latest, "true")
        latestDataSet: DataSetDTO = self.featureRepo.find(id, queryOption)[0]
        if latestDataSet is None or latestDataSet.JamFactorDuration is None:
            return None
        currentDate = self._praseRFCtimeToDatetime(apiInput.DateTime)
        latestDate = self._praseRFCtimeToDatetime(latestDataSet.TimeStamp)

        jamFactorDuration = None
        if self._getMinuteDelta(currentDate, latestDate) <= 10:
            if self._isJamFactorExceedThreshold(latestDataSet.JamFactor, apiInput.JamFactor):
                jamFactorDuration = 0
            else:
                jamFactorDuration = self._getMinuteDelta(currentDate, latestDate) + latestDataSet.JamFactorDuration
        self.jamFactorDuration[id] = jamFactorDuration
        return jamFactorDuration

    def _praseRFCtimeToDatetime(self, dateStr: str) -> datetime:
        # dateStr = "21 June, 2018"
        # 2021-05-09T05:56:31Z
        # %Y-%d-%mT%H:%M:%SZ
        date_object = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
        return date_object

    def _getMinuteDelta(self, currentTime: datetime, prevTime: datetime) -> int:
        return (currentTime - prevTime).total_seconds() / 60

    def _isJamFactorExceedThreshold(self, prevJF, currentJF) -> bool:
        prevJFState = int(prevJF)
        upperBound = prevJFState + 1.15
        lowerBound = prevJFState - .15
        return currentJF > upperBound or currentJF < lowerBound

    def calDeltaJamFactor(self, id:ID, ) -> float:
        apiInput: APIInput = self.APIInputs[id]
        queryOption: QueryOption = QueryOption()
        queryOption.setOption(QueryOption.Latest, "true")
        latestDataSet: DataSetDTO = self.featureRepo.find(id, queryOption)[0]
        if latestDataSet is None:
            return None
        currentJF = apiInput.JamFactor
        prevJF = latestDataSet.JamFactor
        return currentJF - prevJF


    def calNeightbourJamFactor(self, id:ID) -> float:
        v = 0
        node = self.graph.getNodeByID(id)
        if node is None:
            raise Exception('node calNeightbourJamFactor ' + str(id))
        neighbours = node.getNeighbourNodes()
        countValidNeighbour = 0
        for neightbour in neighbours:
            if neightbour.getID() in self.APIInputs:
                countValidNeighbour += 1
                v += self.APIInputs[neightbour.getID()].JamFactor
        if countValidNeighbour == 0:
            return None
        return v / countValidNeighbour

    def calNeightbourJamFactorDuration(self, id:ID) -> float:
        v = 0
        node = self.graph.getNodeByID(id)
        if node is None:
            raise Exception('node calNeightbourJamFactorDuration ' + str(id))
        neighbours = node.getNeighbourNodes()
        countValidNeighbour = 0
        for neightbour in neighbours:
            jamFactorDuration = self.calJamFactorDuration(neightbour.getID())
            if jamFactorDuration is not None:
                countValidNeighbour += 1
                v += jamFactorDuration
        if countValidNeighbour == 0:
            return None
        return v / countValidNeighbour


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
