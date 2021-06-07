from pony import orm
from pony.orm.core import Database
from model.ID import ID
import json

class ModelDTO:
    Model_5: bytes
    Model_15: bytes
    Model_30: bytes
    Model_45: bytes
    Model_60: bytes

    def setModel(self, modelDAO) -> 'ModelDTO':
        self.Model_5 = modelDAO.Model_5
        self.Model_15 = modelDAO.Model_15
        self.Model_30 = modelDAO.Model_30
        self.Model_45 = modelDAO.Model_45
        self.Model_60 = modelDAO.Model_60
        return self

def createModelDAO(db: Database, orm: orm, RoadSegmentDAO):
    class Model(db.Entity):
        _table_ = 'Model'
        ThetaID: int = orm.PrimaryKey(int, auto=True)
        RoadSegment = orm.Required(RoadSegmentDAO, reverse = 'Model')
        Model_5: bytes = orm.Required(bytes)
        Model_15: bytes = orm.Required(bytes)
        Model_30: bytes = orm.Required(bytes)
        Model_45: bytes = orm.Required(bytes)
        Model_60: bytes = orm.Required(bytes)

    return Model

