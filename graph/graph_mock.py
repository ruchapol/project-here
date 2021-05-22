
from interface.graph import IGraph, INode
from model.ID import ID
from typing import Dict, List


class GraphMock(IGraph):

    nodes: Dict[ID, INode]

    def __init__(self):
        self.nodes = {}

    def addNode(self, id: ID, node: INode):
        self.nodes[id] = node

    def getNodeByID(self, id: ID) -> INode:
        return self.nodes[id]
