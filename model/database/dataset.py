from pony import orm
from pony.orm.core import Database
from model.ID import ID
import json

class DataSetDTO:
    ID: ID
    DayOfWeek: int
    Day: int
    Hour: int
    Minute: int
    JamFactor: float
    JamFactorDuration: int
    DeltaJamFactor: int
    NeightbourJamFactor: float
    NeightbourJamFactorDuration: int
    TimeStamp: str
    SpeedUncut: float

    def setTimestamp(self, timestamp: str) -> 'DataSetDTO':
        self.TimeStamp = timestamp
        return self

    def setJamFactorDuration(self, jamfactorDuration: int) -> 'DataSetDTO':
        self.JamFactorDuration = jamfactorDuration
        return self

    def setJamFactor(self, jamFactor: float) -> 'DataSetDTO':
        self.JamFactor = jamFactor
        return self

    def setAllFeature(self, DayOfWeek: int, Day: int, Hour: int, Minute: int,
                      JamFactor: float, JamFactorDuration: int, DeltaJamFactor: int, 
                      NeightbourJamFactor: float, NeightbourJamFactorDuration: int) -> 'DataSetDTO':
        self.DayOfWeek = DayOfWeek
        self.Day = Day
        self.Hour = Hour
        self.Minute = Minute
        self.JamFactor = JamFactor
        self.JamFactorDuration = JamFactorDuration
        self.DeltaJamFactor = DeltaJamFactor
        self.NeightbourJamFactor = NeightbourJamFactor
        self.NeightbourJamFactorDuration = NeightbourJamFactorDuration
        return self

    def setSpeedUncut(self, speedUncut: float) -> 'DataSetDTO':
        self.SpeedUncut = speedUncut
        return self

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def createDatasetDAO(db: Database, orm: orm, RoadSegmentDAO):
    class DataSet(db.Entity):
        _table_ = 'DataSet'
        DataID: int = orm.PrimaryKey(int, auto=True)
        RoadSegment = orm.Required(RoadSegmentDAO, reverse = 'Features')
        DayOfWeek: int = orm.Required(int)
        Day: int = orm.Required(int)
        Hour: int = orm.Required(int)
        Minute: int = orm.Required(int)
        JamFactor: float = orm.Required(float)
        JamFactorDuration: int = orm.Optional(int)
        DeltaJamFactor: int = orm.Optional(int)
        NeightbourJamFactor: float = orm.Optional(float)
        NeightbourJamFactorDuration: int = orm.Optional(float)
        TimeStamp: str = orm.Required(str, index=True)
        SpeedUncut: float = orm.Required(float)
    return DataSet
