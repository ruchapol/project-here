from model.database.dataset import DataSetDTO
import unittest
from featureExtraction.featureExtraction import FeatureExtraction
from model.ID import ID
from typing import Dict, List
from interface.repository import IRepository
from interface.graph import IGraph, INode
from model.featureExtraction.input import APIInput
from graph.graph_mock import GraphMock
from graph.graph import Node
from repository.dataSet_mock import DataSetRepoMock


class TestFeatureExtraction(unittest.TestCase):
    featureExtraction: FeatureExtraction

    def _createABCNodes(self) -> Dict[ID, INode]:
        # A --> B --> C
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

    def _prepareRepo(self) -> Dict[ID, List[DataSetDTO]]:
        datasets  = {
            ID("B", "B1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactorDuration(10).setJamFactor(3),
                DataSetDTO().setTimestamp("2021-05-09T05:47:31Z").setJamFactorDuration(20)
            ]
        }
        repo: DataSetRepoMock = DataSetRepoMock(datasets)
        return repo

    def _prepareAPIInput(self) -> Dict[ID, APIInput]:
        apiInputs: Dict[ID, APIInput] = {
            ID("A", "A1"): APIInput().setSpeedUncut(10).setJamFactor(1),
            ID("B", "B1"): APIInput().setSpeedUncut(20).setJamFactor(2),
            ID("C", "C1"): APIInput().setSpeedUncut(30).setJamFactor(3),
        }
        return apiInputs 

    def _prepareAPIInput_for_calNeightbourJamFactor(self) -> Dict[ID, APIInput]:
        apiInputs: Dict[ID, APIInput] = {
            ID("A", "A1"): APIInput().setSpeedUncut(10).setJamFactor(1),
            ID("B", "B1"): APIInput().setSpeedUncut(20).setJamFactor(2),
            ID("C", "C1"): APIInput().setSpeedUncut(30).setJamFactor(3),
        }
        return apiInputs

    def _prepareAPIInput_for_calJamFactorDuration(self, jf: float, dateTime: str) -> Dict[ID, APIInput]:
        apiInputs: Dict[ID, APIInput] = {
            ID("A", "A1"): APIInput().setSpeedUncut(10).setJamFactor(1),
            ID("B", "B1"): APIInput().setSpeedUncut(20).setJamFactor(jf).setDateTime(dateTime),
            ID("C", "C1"): APIInput().setSpeedUncut(30).setJamFactor(3),
        }
        return apiInputs

    def setUp(self):
        # A --> B --> C
        pass

    def tearDown(self):
        pass

    def test_calNeightbourJamFactor(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = self._prepareAPIInput_for_calNeightbourJamFactor()
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, self._prepareRepo(), graph)

        # execute
        neightbourJFActual = self.featureExtraction.calNeightbourJamFactor(
            ID("B", "B1"))

        # assertion
        self.assertEqual(neightbourJFActual, 2)

    def test_calJamFactorDuration(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = self._prepareAPIInput_for_calJamFactorDuration(2.85, "2021-05-09T05:59:31Z")
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, self._prepareRepo(), graph)

        # execute
        jamFactorDuration = self.featureExtraction.calJamFactorDuration(
            ID("B", "B1"))

        # assertion
        self.assertEqual(jamFactorDuration, 13)

    def test_calJamFactorDuration_case1(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = self._prepareAPIInput_for_calJamFactorDuration(3.11643, "2019-03-31T18:29:19Z")
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, DataSetRepoMock({
            ID("B", "B1"): [
                DataSetDTO().setTimestamp("2019-03-31T18:24:18Z").setJamFactorDuration(0).setJamFactor(3.11643),
                DataSetDTO().setTimestamp("2019-03-09T05:47:31Z").setJamFactorDuration(20)
            ]
        }), graph)

        # execute
        jamFactorDuration = self.featureExtraction.calJamFactorDuration(
            ID("B", "B1"))

        # assertion
        self.assertEqual(jamFactorDuration, 5)
    
    def test_calJamFactorDuration_timeExceed(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = self._prepareAPIInput_for_calJamFactorDuration(2.85, "2021-05-09T06:20:31Z")
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, self._prepareRepo(), graph)

        # execute
        jamFactorDuration = self.featureExtraction.calJamFactorDuration(
            ID("B", "B1"))

        # assertion
        self.assertEqual(jamFactorDuration, None)

    def test_calJamFactorDuration_thresholdExceed(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = self._prepareAPIInput_for_calJamFactorDuration(2.5, "2021-05-09T05:59:31Z")
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, self._prepareRepo(), graph)

        # execute
        jamFactorDuration = self.featureExtraction.calJamFactorDuration(
            ID("B", "B1"))

        # assertion
        self.assertEqual(jamFactorDuration, 0)

    def test_calJamFactorDuration_emptyData(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = self._prepareAPIInput_for_calJamFactorDuration(2.5, "2021-05-09T05:59:31Z")
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, DataSetRepoMock({}), graph)

        # execute
        jamFactorDuration = self.featureExtraction.calJamFactorDuration(
            ID("B", "B1"))

        # assertion
        self.assertEqual(jamFactorDuration, None)

    def test_calDeltaJamFactor(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = {
            ID("B", "B1"): APIInput().setSpeedUncut(20).setJamFactor(2)
        }
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, DataSetRepoMock({
            ID("B", "B1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactorDuration(10).setJamFactor(10),
                DataSetDTO().setTimestamp("2021-05-09T05:47:31Z").setJamFactorDuration(20)
            ]
        }), graph)

        # execute
        deltaJamFactor = self.featureExtraction.calDeltaJamFactor(ID("B", "B1"))

        # assertion
        self.assertEqual(deltaJamFactor, -8)

    def test_calDeltaJamFactor_emptyData(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = {
            ID("B", "B1"): APIInput().setSpeedUncut(20).setJamFactor(2)
        }
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, DataSetRepoMock({}), graph)

        # execute
        deltaJamFactor = self.featureExtraction.calDeltaJamFactor(ID("B", "B1"))

        # assertion
        self.assertEqual(deltaJamFactor, None)

    def test_calNeightbourJamFactorDuration(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = {
            ID("A", "A1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(1),
            ID("B", "B1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(2),
            ID("C", "C1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(3),
        }
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, DataSetRepoMock({
            ID("A", "A1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(1).setJamFactorDuration(10),
            ],
            ID("B", "B1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(2).setJamFactorDuration(20),
            ],
            ID("C", "C1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(3).setJamFactorDuration(30),
            ],
        }), graph)

        # execute
        deltaJamFactor = self.featureExtraction.calNeightbourJamFactorDuration(ID("B", "B1"))

        # assertion
        self.assertEqual(deltaJamFactor, 23)

    def test_calNeightbourJamFactorDuration_oneNeighbourIsExceedThreshold(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = {
            ID("A", "A1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(2.3),
            ID("B", "B1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(2),
            ID("C", "C1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(3),
        }
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, DataSetRepoMock({
            ID("A", "A1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(1).setJamFactorDuration(10),
            ],
            ID("B", "B1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(2).setJamFactorDuration(20),
            ],
            ID("C", "C1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(3).setJamFactorDuration(30),
            ],
        }), graph)

        # execute
        deltaJamFactor = self.featureExtraction.calNeightbourJamFactorDuration(ID("B", "B1"))

        # assertion
        self.assertEqual(deltaJamFactor, 16.5)

    def test_calNeightbourJamFactorDuration_oneNeighbourIsNone(self):
        # prepare data
        apiInputs: Dict[ID, APIInput] = {
            ID("A", "A1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(2.3),
            ID("B", "B1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(2),
            ID("C", "C1"): APIInput().setDateTime("2021-05-09T05:59:31Z").setJamFactor(3),
        }
        nodes = self._createABCNodes()
        graph: IGraph = GraphMock(nodes)
        self.featureExtraction = FeatureExtraction(
            apiInputs, DataSetRepoMock({
            ID("A", "A1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(1).setJamFactorDuration(None),
            ],
            ID("B", "B1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(2).setJamFactorDuration(20),
            ],
            ID("C", "C1"): [
                DataSetDTO().setTimestamp("2021-05-09T05:56:31Z").setJamFactor(3).setJamFactorDuration(30),
            ],
        }), graph)

        # execute
        deltaJamFactor = self.featureExtraction.calNeightbourJamFactorDuration(ID("B", "B1"))

        # assertion
        self.assertEqual(deltaJamFactor, 16.5)


