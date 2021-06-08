from re import L
from typing import Dict, List
from interface.repository import IRepository
from pony.orm import db_session, select, get, desc, avg
from pony.orm.core import OrmError
from pony import orm
from model.database.dataset import DataSetDTO
from model.ID import ID


class QueryOption:
    Latest: str = 'latest'
    Limit: str = 'limit'
    queryOption: Dict

    def __init__(self):
        self.queryOption = {self.Latest: "false"}

    def setOption(self, key: str, value: str):
        self.queryOption[key] = value

    def wantLastest(self) -> bool:
        return self.queryOption[QueryOption.Latest] == "true"

    def limit(self) -> int:
        limit = self.queryOption[QueryOption.Limit]
        if type(limit) != int:
            return -1
        else:
            return limit


class DataSetRepo(IRepository):
    datasetDAO = None
    # cache: Dict[ID, DataSetDTO]

    def __init__(self, roadSegmentDAO, datasetDAO):
        self.datasetDAO = datasetDAO
        self.roadSegmentDAO = roadSegmentDAO
        # self.cache = {}

    @db_session
    def find(self, id: ID, options: QueryOption = QueryOption()) -> DataSetDTO:
        try:
            if options.wantLastest():  # sorted with dsc
                # if id in self.cache:
                #     return self.cache[id][:1]
                latestDataset = select(x for x in self.roadSegmentDAO[id.RoadID, id.SegmentID].Features).order_by(
                    lambda: desc(x.TimeStamp)).limit(1)
                if len(latestDataset) == 0:
                    return [None]
                # self.cache[id] = latest
                datasetsDTO: List[DataSetDTO] = []
                for dataset in latestDataset:
                    datasetsDTO.append(
                        self._datasetDAOToDTOWithFillAverage(id, dataset))
                return datasetsDTO
            datasetsDAO = select(
                x for x in self.roadSegmentDAO[id.RoadID, id.SegmentID].Features)
            datasetsDTO: List[DataSetDTO] = []
            for dataset in datasetsDAO:
                datasetsDTO.append(self._datasetDAOToDTO(id, dataset))
            return datasetsDTO
        except OrmError as e:
            print("OrmError:", e)
            return [None]

    @db_session
    def _findAvgJamFactorDuration(self, id: ID) -> float:
        print("_findAvgJamFactorDuration")
        avgVal = avg(
            x.JamFactorDuration for x in self.roadSegmentDAO[id.RoadID, id.SegmentID].Features)
        return self._ifNoneReturnZero(avgVal)

    @db_session
    def _findAvgDeltaJamFactor(self, id: ID) -> float:
        print("_findAvgDeltaJamFactor")
        avgVal = avg(
            x.DeltaJamFactor for x in self.roadSegmentDAO[id.RoadID, id.SegmentID].Features)
        return self._ifNoneReturnZero(avgVal)

    @db_session
    def _findAvgNeightbourJamFactor(self, id: ID) -> float:
        print("_findAvgNeightbourJamFactor")
        avgVal = avg(
            x.NeightbourJamFactor for x in self.roadSegmentDAO[id.RoadID, id.SegmentID].Features)
        return self._ifNoneReturnZero(avgVal)

    @db_session
    def _findAvgNeightbourJamFactorDuration(self, id: ID) -> float:
        print("_findAvgNeightbourJamFactorDuration")
        avgVal = avg(
            x.NeightbourJamFactorDuration for x in self.roadSegmentDAO[id.RoadID, id.SegmentID].Features)
        return self._ifNoneReturnZero(avgVal)

    def _ifNoneReturnZero(self, number: float) -> float:
        return 0 if number is None else number

    def _datasetDAOToDTOWithFillAverage(self, id: ID, dataSetDAO) -> DataSetDTO:
        d = DataSetDTO()
        d.ID = id
        d.DayOfWeek = dataSetDAO.DayOfWeek
        d.Day = dataSetDAO.Day
        d.Hour = dataSetDAO.Hour
        d.Minute = dataSetDAO.Minute
        d.JamFactor = dataSetDAO.JamFactor
        d.JamFactorDuration = dataSetDAO.JamFactorDuration if dataSetDAO.JamFactorDuration is not None else self._findAvgJamFactorDuration(
            id)
        d.DeltaJamFactor = dataSetDAO.DeltaJamFactor if dataSetDAO.DeltaJamFactor is not None else self._findAvgDeltaJamFactor(
            id)
        d.NeightbourJamFactor = dataSetDAO.NeightbourJamFactor if dataSetDAO.NeightbourJamFactor is not None else self._findAvgNeightbourJamFactor(
            id)
        d.NeightbourJamFactorDuration = dataSetDAO.NeightbourJamFactorDuration if dataSetDAO.NeightbourJamFactorDuration is not None else self._findAvgNeightbourJamFactorDuration(
            id)
        d.TimeStamp = dataSetDAO.TimeStamp
        d.SpeedUncut = dataSetDAO.SpeedUncut
        return d

    def _datasetDAOToDTO(self, id: ID, dataSetDAO) -> DataSetDTO:
        d = DataSetDTO()
        d.ID = id
        d.DayOfWeek = dataSetDAO.DayOfWeek
        d.Day = dataSetDAO.Day
        d.Hour = dataSetDAO.Hour
        d.Minute = dataSetDAO.Minute
        d.JamFactor = dataSetDAO.JamFactor
        d.JamFactorDuration = dataSetDAO.JamFactorDuration
        d.DeltaJamFactor = dataSetDAO.DeltaJamFactor
        d.NeightbourJamFactor = dataSetDAO.NeightbourJamFactor
        d.NeightbourJamFactorDuration = dataSetDAO.NeightbourJamFactorDuration
        d.TimeStamp = dataSetDAO.TimeStamp
        d.SpeedUncut = dataSetDAO.SpeedUncut
        return d

    @db_session
    def findAll(self) -> Dict[ID, DataSetDTO]:
        pass

    @db_session
    def save(self, datasets: List[DataSetDTO]):
        for dataset in datasets:
            self.datasetDAO(
                RoadSegment=self.roadSegmentDAO[dataset.ID.RoadID,
                                                dataset.ID.SegmentID],
                DayOfWeek=dataset.DayOfWeek,
                Day=dataset.Day,
                Hour=dataset.Hour,
                Minute=dataset.Minute,
                JamFactor=dataset.JamFactor,
                JamFactorDuration=dataset.JamFactorDuration,
                DeltaJamFactor=dataset.DeltaJamFactor,
                NeightbourJamFactor=dataset.NeightbourJamFactor,
                NeightbourJamFactorDuration=dataset.NeightbourJamFactorDuration,
                TimeStamp=dataset.TimeStamp,
                SpeedUncut=dataset.SpeedUncut,
            )
