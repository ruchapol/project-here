
from interface.graph import IGraph, INode
from model.ID import ID
from typing import Dict, List


class GraphMock(IGraph):

    nodes: Dict[ID, INode]

    def __init__(self, nodes: Dict[ID, INode]):
        self.nodes = nodes

    def addNode(self, id: ID, node: INode):
        self.nodes[id] = node

    def getNodeByID(self, id: ID) -> INode:
        return self.nodes[id]

class NodeMock(INode):
    def __init__(self):
        pass

    def addOutboundNode(self, node: INode):
        return super().addOutboundNode(node)

    def addInboundNode(self, node: INode):
        return super().addInboundNode(node)

    def getNeighbourNodes(self) -> List[INode]:
        return []