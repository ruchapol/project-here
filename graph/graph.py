from __future__ import annotations
from model.database.roadSegment import RoadSegmentDTO
from interface.repository import IRepository
from typing import List, Dict, Tuple
from interface.graph import IGraph, INode
from model.ID import ID

class Graph(IGraph):
    nodes: Dict[ID, INode]
    roadSegmentRepo: IRepository

    def __init__(self, repo: IRepository) -> Graph:
        self.nodes = {}
        self.roadSegmentRepo = repo
        self._buildGraph()

    def _buildGraph(self):
        roadSegments: Dict[ID, RoadSegmentDTO] = self.roadSegmentRepo.findAll()
        for ID in roadSegments:
            OutboundIDS: List[ID] = roadSegments[ID].To
            node = self.getNodeOrCreate(ID, roadSegments[ID])

            for OID in OutboundIDS:
                node.addOutboundNode(
                    self.getNodeOrCreate(OID, roadSegments[OID]))

    def getNodeOrCreate(self, id: ID, roadSegment: RoadSegmentDTO) -> INode:
        node = self.getNodeByID(id)
        if node is not None:
            return node
        RoadDescription = roadSegment.RoadDescription
        RoadSegmentDescription = roadSegment.RoadSegmentDescription
        node = Node(id, RoadDescription, RoadSegmentDescription, roadSegment.LatLong)
        self.addNode(node)
        return node

    def addNode(self, node: INode) -> INode:
        self.nodes[node.getID()] = node

    def getNodeByID(self, id: ID) -> INode:
        if id in self.nodes:
            return self.nodes[id]
        return None

    def getNodes(self) -> Dict[ID, INode]:
        return self.nodes

class Node(INode):
    id: ID
    roadName: str
    segmentName: str
    latLong: str
    inboundNodes: List[Node]
    outboundNodes: List[Node]

    def __init__(self, id: ID, roadName: str, segmentName: str, latLong: str = "") -> Node:
        self.id = id
        self.roadName = roadName
        self.segmentName = segmentName
        self.latLong = latLong
        self.inboundNodes = []
        self.outboundNodes = []

    def setID(self, id: ID) -> ID:
        self.id = id

    def getID(self) -> ID:
        return self.id

    def getRoadName(self) -> str:
        return self.roadName

    def getSegmentName(self) -> str:
        return self.segmentName

    def getLatLong(self) -> Tuple[float,float]:
        if self.latLong == 'none':
            return [None,None]
        return [float(x) for x in self.latLong.split(",")]

    def addInboundNode(self, node: Node):
        if node not in self.inboundNodes:
            self.inboundNodes.append(node)
            if self not in node.getOutboundNodes():
                node.addOutboundNode(self)

    def addOutboundNode(self, node: Node):
        if node not in self.outboundNodes:
            self.outboundNodes.append(node)
            if self not in node.getInboundNodes():
                node.addInboundNode(self)

    def getNeighbourNodes(self) -> List[Node]:
        return list(set(self.inboundNodes).union(self.outboundNodes))

    def getInboundNodes(self) -> List[Node]:
        return self.inboundNodes

    def getOutboundNodes(self) -> List[Node]:
        return self.outboundNodes
