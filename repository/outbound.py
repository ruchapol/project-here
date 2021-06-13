from re import L
from typing import Dict, List
from interface.repository import IRepository
from pony.orm import db_session, get
from pony import orm
from model.database.roadSegment import OutboundDTO
from model.ID import ID


class OutboundRepo(IRepository):
    roadSegmentDAO = None
    outboundDAO = None

    def __init__(self, roadSegmentDAO, outboundDAO):
        self.roadSegmentDAO = roadSegmentDAO
        self.outboundDAO = outboundDAO

    @db_session
    def find(self, fromID: ID, toID: ID) -> OutboundDTO:
        fromRoad = self.roadSegmentDAO[fromID.RoadID, fromID.SegmentID]
        toRoad = self.roadSegmentDAO[toID.RoadID, toID.SegmentID]
        selectedOutboundDAO = get(o for o in self.outboundDAO if o.From == fromRoad and o.To == toRoad)
        outboundDTO = OutboundDTO()
        outboundDTO.From = ID(selectedOutboundDAO.From.RoadID, selectedOutboundDAO.From.RoadSegmentID)
        outboundDTO.To = ID(selectedOutboundDAO.To.RoadID, selectedOutboundDAO.To.RoadSegmentID)
        outboundDTO.DistanceKM = selectedOutboundDAO.Distance
        return outboundDTO
