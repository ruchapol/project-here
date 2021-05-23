from pony.orm import Database
from pony import orm
from pony.orm.core import PrimaryKey
from typing import List
from model.ID import ID

class RoadSegmentDTO:
    RowID: int
    RoadID: str
    RoadSegmentID: str
    RoadDescription: str
    RoadSegmentDescription: str
    LatLong: str
    To: List[ID]

class OutboundDTO:
    OutboundID: int
    From: RoadSegmentDTO  # point to RowID
    To: RoadSegmentDTO  # point to RowID

def roadSegment_DAO(db: Database, orm: orm):
    class RoadSegment(db.Entity):
        _table_ = 'RoadSegment'
        # RowID: int = orm.PrimaryKey(int, auto=True)
        RoadID: str = orm.Required(str)
        RoadSegmentID: str = orm.Required(str)
        RoadDescription: str = orm.Required(str)
        RoadSegmentDescription: str = orm.Required(str)
        LatLong: str = orm.Required(str)
        From = orm.Set('Outbound', reverse='From')
        To = orm.Set('Outbound', reverse='To')
        RowID: orm.PrimaryKey(RoadID, RoadSegmentID)
    return RoadSegment


def outbound_DAO(db: Database, orm: orm, RoadSegment):
    class Outbound(db.Entity):
        _table_ = 'Outbound'
        OutboundID: int = orm.PrimaryKey(int, auto=True)
        From = orm.Required(RoadSegment, reverse = 'From')
        To = orm.Required(RoadSegment, reverse = 'To')
    return Outbound

