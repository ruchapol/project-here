from __future__ import annotations
from typing import List, Tuple
from model.ID import ID

class IGraph:
    def addNode(self, node: INode):
        raise NotImplementedError
    
    def getNodeByID(self, id: ID) -> INode:
        raise NotImplementedError

class INode:
    def setID(self,id: ID) -> ID:
        raise NotImplementedError

    def getID(self) -> ID:
        raise NotImplementedError

    def getRoadName(self) -> str:
        raise NotImplementedError

    def getSegmentName(self) -> str:
        raise NotImplementedError
    
    def getLatLong(self) -> Tuple[float,float]:
        raise NotImplementedError

    def addInboundNode(self, node: INode):
        raise NotImplementedError

    def addOutboundNode(self, node: INode):
        raise NotImplementedError

    def getInboundNodes(self) -> List[INode]:
        raise NotImplementedError

    def getOutboundNodes(self) -> List[INode]:
        raise NotImplementedError

    def getNeighbourNodes(self) -> List[INode]:
        raise NotImplementedError
