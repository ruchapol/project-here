from interface.repository import IRepository
from model.ID import ID
from model.database.roadSegment import OutboundDTO, RoadSegmentDTO
from geopy.distance import geodesic


class TravelTimeCalculator:
    outboundRepo: IRepository
    roadSegmentRepo: IRepository
    def __init__(self, outboundRepo, roadSegmentRepo=None):
        self.outboundRepo = outboundRepo
        self.roadSegmentRepo = roadSegmentRepo

    # time as hour(s)
    def calculateTravelTime(self, a: ID, b: ID, vA: float, vB: float):
        outboundAToB: OutboundDTO = self.outboundRepo.find(a, b)
        halfDistance = outboundAToB.DistanceKM / 2
        tAB = (halfDistance / vA) + (halfDistance / vB)
        return tAB # hour

    # time as hour(s)
    def calculateTravelTimeNoOutbound(self, a: ID, b: ID, vA: float, vB: float):
        segmentA: RoadSegmentDTO = self.roadSegmentRepo.find(a)
        segmentB: RoadSegmentDTO = self.roadSegmentRepo.find(b)
        halfDistance = geodesic(segmentA.getLatLong(), segmentB.getLatLong()).kilometers / 2
        tAB = (halfDistance / vA) + (halfDistance / vB)
        return tAB # hour
