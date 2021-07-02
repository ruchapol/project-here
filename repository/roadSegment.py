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
    def __init__(self, roadSegmentDAO, outboundDAO):
        self.roadSegmentDAO = roadSegmentDAO
        self.outboundDAO = outboundDAO


    @db_session
    def find(self, id: ID) -> RoadSegmentDTO:
        dao = self.roadSegmentDAO[id.RoadID, id.SegmentID]
        roadSegmentDTO = RoadSegmentDTO()
        roadSegmentDTO.LatLong = dao.LatLong
        roadSegmentDTO.RoadID = dao.RoadID
        roadSegmentDTO.RoadSegmentID = dao.RoadSegmentID
        roadSegmentDTO.RoadDescription = dao.RoadDescription
        roadSegmentDTO.RoadSegmentDescription = dao.RoadSegmentDescription
        # roadSegmentDTO.RowID = dao.RowID
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
