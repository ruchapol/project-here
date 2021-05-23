from __future__ import annotations
from interface.repository import IRepository
from typing import List, Dict
from interface.graph import IGraph, INode
from model.ID import ID

class Graph(IGraph):
    nodes: Dict[ID, INode]
    roadSegmentRepo: IRepository
    def __init__(self) -> Graph:
        self.nodes = {}
        self.buildGraph()

    def buildGraph():
        pass

    def addNode(self, node: INode) -> INode:
        self.nodes[node.getID()] = node

    def getNodeByID(self, id: ID) -> INode:
        return self.nodes[id]

class Node(INode):
    id: ID
    roadName: str
    segmentName: str
    latLong: str
    inboundNodes: List[Node]
    outboundNodes: List[Node]

    def __init__(self, id: ID, roadName: str, segmentName: str) -> Node:
        self.id = id
        self.roadName= roadName
        self.segmentName = segmentName
        self.inboundNodes = []
        self.outboundNodes = []
    
    def setID(self,id: ID) -> ID:
        self.id = id

    def getID(self) -> ID:
        return self.id

    def getRoadName(self) -> str:
        return self.roadName

    def getSegmentName(self) -> str:
        return self.segmentName

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
 
