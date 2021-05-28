from re import L
from typing import Dict, List
from interface.repository import IRepository
from pony.orm import db_session, select, get, desc
from pony.orm.core import ObjectNotFound
from pony import orm
from model.database.dataset import DataSetDTO
from model.ID import ID

class QueryOption:
    Latest: str = 'latest'
    Limit: str = 'limit'
    queryOption: Dict
    def __init__(self):
        self.queryOption = {}

    def setOption(self, key:str, value:str):
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
    def __init__(self, roadSegmentDAO, datasetDAO):
        self.datasetDAO = datasetDAO
        self.roadSegmentDAO = roadSegmentDAO


    @db_session
    def find(self, id: ID, options: QueryOption) -> DataSetDTO:
        try:
            if options.wantLastest(): # sorted with dsc 
                latest = select(x for x in self.roadSegmentDAO[id.RoadID,id.SegmentID].Features).order_by(lambda: desc(x.TimeStamp))
                if len(latest) == 0:
                    return [None]
                return latest[:1]
            return self.datasetDAO[id.RoadID,id.SegmentID]
        except ObjectNotFound:
            return [None]
        
    @db_session
    def findAll(self) -> Dict[ID, DataSetDTO]:
        pass

    @db_session
    def save(self, datasets: List[DataSetDTO]):
        print("data len = ",len(datasets))
        for dataset in datasets:
            self.datasetDAO(
            RoadSegment = self.roadSegmentDAO[dataset.ID.RoadID, dataset.ID.SegmentID],
            DayOfWeek = dataset.DayOfWeek,
            Day = dataset.Day,
            Hour = dataset.Hour,
            Minute = dataset.Minute,
            JamFactor = dataset.JamFactor,
            JamFactorDuration = dataset.JamFactorDuration,
            DeltaJamFactor = dataset.DeltaJamFactor,
            NeightbourJamFactor = dataset.NeightbourJamFactor,
            NeightbourJamFactorDuration = dataset.NeightbourJamFactorDuration,
            TimeStamp = dataset.TimeStamp,
            SpeedUncut = dataset.SpeedUncut,
            )
