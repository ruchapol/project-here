import unittest
from featureExtraction.featureExtraction import FeatureExtraction
from model.ID import ID
from typing import Dict
from interface.repository import IRepository
from interface.graph import IGraph, INode
from model.featureExtraction.input import APIInput
from graph.graph_mock import GraphMock 
from graph.graph import Node
from repository.dataSet_mock import DataSetRepoMock

class TestFeatureExtraction(unittest.TestCase):
    featureExtraction: FeatureExtraction

    def _createABCNodes(self) -> Dict[ID, INode]:
        node1 = Node(ID("A", "A1"), "ROAD A", "segmentA1")
        node2 = Node(ID("B", "B1"), "ROAD B", "segmentB1")
        node3 = Node(ID("C", "C1"), "ROAD C", "segmentC1")
        node1.addOutboundNode(node2)
        node2.addOutboundNode(node3)
        nodes: Dict[ID, INode] = {
            ID("A", "A1"): node1,
            ID("B", "B1"): node2,
            ID("C", "C1"): node3
        }
        return nodes

    
    def setUp(self):
        # A --> B --> C
        apiInputs: Dict[ID, APIInput] = {
            ID("A", "A1"): APIInput().speedUncut(10).jamFactor(1),
            ID("B", "B1"): APIInput().speedUncut(20).jamFactor(2),
            ID("C", "C1"): APIInput().speedUncut(30).jamFactor(3),
        }
        repo: IRepository = DataSetRepoMock()
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(apiInputs, repo, graph)

    def tearDown(self):
        pass

    def test_calNeightbourJamFactor(self):
        neightbourJFActual = self.featureExtraction.calNeightbourJamFactor(ID("B", "B1"))
        self.assertEqual(neightbourJFActual, 2)

    def test_calJamFactorDuration(self):
        pass

    def test_calDeltaJamFactor(self):
        pass


    def test_calNeightbourJamFactorDuration(self):
        pass
