from typing import List


class IGraph:
    def getNodeByID(self, id:Tuple[RoadID:str, SegmentID:str]) -> INode:
        raise NotImplementedError

class INode:
    def inboundNodes(self) -> List[INode]:
        raise NotImplementedError

    def outboundNodes(self) -> List[INode]:
        raise NotImplementedError

    def getNeighbourNodes(self) -> List[INode]:
        raise NotImplementedError
