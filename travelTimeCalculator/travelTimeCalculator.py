from interface.repository import IRepository
from model.ID import ID
from model.database.roadSegment import OutboundDTO


class TravelTimeCalculator:
    outboundRepo: IRepository

    def __init__(self, outboundRepo):
        self.outboundRepo = outboundRepo

    def calculateTravelTime(self, a: ID, b: ID, vA: float, vB: float):
        outboundAToB: OutboundDTO = self.outboundRepo.find(a, b)
        halfDistance = outboundAToB.DistanceKM / 2
        tAB = (halfDistance / vA) + (halfDistance / vB)
        return tAB # hour
