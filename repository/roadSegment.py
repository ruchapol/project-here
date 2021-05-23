from typing import Dict, List
from interface.repository import IRepository
from pony.orm import db_session, select, get
from pony import orm
from model.database.roadSegment import RoadSegmentDTO, roadSegment_DAO, outbound_DAO
from model.ID import ID

class RoadSegmentRepo(IRepository):
    db: orm.Database
    roadSegmentDAO = None
    outboundDAO = None

    def __init__(self, db: orm.Database):
        self.db = db
        self.roadSegmentDAO = roadSegment_DAO(db, orm)
        self.outboundDAO = outbound_DAO(db, orm, self.roadSegmentDAO)

    @db_session
    def find(self, id: ID) -> RoadSegmentDTO:
        dao = self.roadSegmentDAO[id.RoadID, id.SegmentID]
        roadSegmentDTO: RoadSegmentDTO = dao
        roadSegmentDTO.To = [t.To for t in dao.From]
        return roadSegmentDTO

    def findAll(self) -> List[RoadSegmentDTO]:
        return [self.data]

    def save(self, data):
        super().save(self)
