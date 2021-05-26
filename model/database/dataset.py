from pony import orm
from pony.orm.core import Database
from model.ID import ID

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

    def timestamp(self, timestamp: str) -> 'DataSetDTO':
        self.TimeStamp = timestamp
        return self

    def jamFactorDuration(self, jamfactorDuration: int) -> 'DataSetDTO':
        self.JamFactorDuration = jamfactorDuration
        return self

    def jamFactor(self, jamFactor: float) -> 'DataSetDTO':
        self.JamFactor = jamFactor
        return self


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
        JamFactorDuration: int = orm.Required(int)
        DeltaJamFactor: int = orm.Required(int)
        NeightbourJamFactor: float = orm.Required(float)
        NeightbourJamFactorDuration: int = orm.Required(int)
        TimeStamp: str = orm.Required(str)
        SpeedUncut: float = orm.Required(float)
    return DataSet
