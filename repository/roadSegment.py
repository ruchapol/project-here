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
        toTmp = [t.To for t in dao.From]
        roadSegmentDTO.To = [ID(x.RoadID,x.RoadSegmentID) for x in toTmp]
        return roadSegmentDTO

    @db_session
    def findAll(self) -> List[RoadSegmentDTO]:
        roadSegmentsDAO = select(x for x in self.roadSegmentDAO)
        roadSegments :List[RoadSegmentDTO] = []
        for segment in roadSegmentsDAO:
            newRoadSegment = RoadSegmentDTO()
            newRoadSegment.RoadID = segment.RoadID
            newRoadSegment.RoadSegmentID = segment.RoadSegmentID
            newRoadSegment.RoadDescription = segment.RoadDescription
            newRoadSegment.RoadSegmentDescription = segment.RoadSegmentDescription
            newRoadSegment.LatLong = segment.LatLong
            toTmp = [t.To for t in segment.From]
            newRoadSegment.To = [ID(x.RoadID,x.RoadSegmentID) for x in toTmp]
            roadSegments.append(newRoadSegment)
        return roadSegments

    def save(self, data):
        super().save(self)
