from travelTimeCalculator.travelTimeCalculator import TravelTimeCalculator
from model.database.roadSegment import OutboundDTO
from repository.outbound_mock import OutboundRepoMock
from interface.graph import IGraph, INode
from graph.graph import Graph, Node
from model.ID import ID
from typing import List
from repository.outbound_mock import OutboundRepoMock
import unittest


class TestTravelTimeCalculator(unittest.TestCase):

    def setUp(self):
        pass

    def test_calculateTravelTime(self):
        # arrange
        idA = ID("A","A01")
        idB = ID("B","B01")
        outboundRepo = OutboundRepoMock({
            (idA, idB): OutboundDTO().setDistanceKM(15)
            })

        # act
        travelTimeCalculator = TravelTimeCalculator(outboundRepo)
        timeTravel = travelTimeCalculator.calculateTravelTime(idA,idB,10,20)

        # assert
        self.assertEqual(1.125 ,timeTravel)



if __name__ == '__main__':
    unittest.main()
