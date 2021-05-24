from re import L
from typing import Dict, List
from interface.repository import IRepository
from pony.orm import db_session, select, get
from pony import orm
from model.database.roadSegment import RoadSegmentDTO, createRoadSegmentDAO, createOutboundDAO
from model.ID import ID

class RoadSegmentRepo(IRepository):
    roadSegmentDAO = None
    outboundDAO = None
    db: orm.Database
    def __init__(self, db: orm.Database):
        self.db = db
        self.roadSegmentDAO = createRoadSegmentDAO(db, orm)
        self.outboundDAO = createOutboundDAO(db, orm, self.roadSegmentDAO)
        self.db.generate_mapping(create_tables=True)


    @db_session
    def find(self, id: ID) -> RoadSegmentDTO:
        dao = self.roadSegmentDAO[id.RoadID, id.SegmentID]
        roadSegmentDTO: RoadSegmentDTO = dao
        toTmp = [t.To for t in dao.From]
        roadSegmentDTO.To = [ID(x.RoadID,x.RoadSegmentID) for x in toTmp]
        return roadSegmentDTO

    # @db_session
    # def findAll(self) -> List[RoadSegmentDTO]:
    #     roadSegmentsDAO = select(x for x in self.roadSegmentDAO)
    #     roadSegments :List[RoadSegmentDTO] = []
    #     for segment in roadSegmentsDAO:
    #         newRoadSegment = RoadSegmentDTO()
    #         newRoadSegment.RoadID = segment.RoadID
    #         newRoadSegment.RoadSegmentID = segment.RoadSegmentID
    #         newRoadSegment.RoadDescription = segment.RoadDescription
    #         newRoadSegment.RoadSegmentDescription = segment.RoadSegmentDescription
    #         newRoadSegment.LatLong = segment.LatLong
    #         toTmp = [t.To for t in segment.From]
    #         newRoadSegment.To = [ID(x.RoadID,x.RoadSegmentID) for x in toTmp]
    #         roadSegments.append(newRoadSegment)
    #     return roadSegments
    
    @db_session
    def findAll(self) -> Dict[ID, RoadSegmentDTO]:
        roadSegmentsDAO = select(x for x in self.roadSegmentDAO)
        roadSegments :Dict[ID, RoadSegmentDTO] = {}
        for segment in roadSegmentsDAO:
            newRoadSegment = RoadSegmentDTO()
            newRoadSegment.RoadID = segment.RoadID
            newRoadSegment.RoadSegmentID = segment.RoadSegmentID
            newRoadSegment.RoadDescription = segment.RoadDescription
            newRoadSegment.RoadSegmentDescription = segment.RoadSegmentDescription
            newRoadSegment.LatLong = segment.LatLong
            toTmp = [t.To for t in segment.From]
            newRoadSegment.To = [ID(x.RoadID,x.RoadSegmentID) for x in toTmp]
            roadSegments[ID(segment.RoadID, segment.RoadSegmentID)] = newRoadSegment
        return roadSegments

    def save(self, data):
        super().save(self)
