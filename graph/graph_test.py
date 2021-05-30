from interface.graph import IGraph, INode
from graph.graph import Graph, Node
from model.ID import ID
from typing import List
from repository.roadSegment_mock import RoadSegmentRepoMock
import unittest


class TestGraph(unittest.TestCase):
    graph: IGraph

    def setUp(self):
        graph = Graph(RoadSegmentRepoMock({}))
        node1 = Node(ID("roadA", "segmentA"), "ROAD A", "segmentA")
        node2 = Node(ID("roadA", "segmentB"), "ROAD A", "segmentB")
        node3 = Node(ID("roadZ", "segmentC"), "ROAD Z", "segmentC")

        graph.addNode(node1)
        graph.addNode(node2)
        graph.addNode(node3)

        self.graph = graph

    def test_getNodeByID(self):
        nodeOne = self.graph.getNodeByID(ID("roadA", "segmentA"))
        self.assertEqual(nodeOne.getID().RoadID, "roadA")
        self.assertEqual(nodeOne.getID().SegmentID, "segmentA")


class TestNode(unittest.TestCase):
    nodes: List[Node]
    node1: Node
    node2: Node
    node3: Node

    def initialNodes(self):
        node1 = Node(ID("roadA", "segmentA"), "ROAD A", "segmentA")
        node2 = Node(ID("roadA", "segmentB"), "ROAD A", "segmentB")
        node3 = Node(ID("roadZ", "segmentC"), "ROAD Z", "segmentC")
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.nodes = [node1, node2, node3]

    def setUp(self):
        self.initialNodes()

    def tearDown(self):
        del self.node1
        del self.node2
        del self.node3
        del self.nodes

    def test_addInboudNode(self):
        self.node2.addInboundNode(self.node1)
        self.assertEqual(self.node2.inboundNodes[0].getID(),
                         self.node1.getID())
        self.assertEqual(self.node1.outboundNodes[0].getID(),
                         self.node2.getID())

    def test_addOutboundNode(self):
        self.node1.addOutboundNode(self.node2)
        self.assertEqual(self.node1.outboundNodes[0].getID(),
                         self.node2.getID())
        self.assertEqual(self.node2.inboundNodes[0].getID(),
                         self.node1.getID())

    def test_addInboudNode_should_not_add_same_node(self):
        self.node1.addOutboundNode(self.node2)
        self.node1.addOutboundNode(self.node2)
        self.assertEqual(len(self.node1.getOutboundNodes()), 1)

    def test_getNeighbourNodes(self):
        self.node1.addInboundNode(self.node2)
        self.node1.addInboundNode(self.node3)
        self.node1.addInboundNode(self.node3)
        self.assertEqual(len(self.node1.getNeighbourNodes()), 2)


if __name__ == '__main__':
    unittest.main()
