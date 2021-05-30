from model.database.roadSegment import RoadSegmentDTO
from model.database.dataset import DataSetDTO
from model.ID import ID
from typing import Dict, List

class RoadSegmentRepoMock(RoadSegmentDTO):
    data: Dict[ID, List[RoadSegmentDTO]]
    def __init__(self, data: Dict[ID, List[DataSetDTO]]):
        self.data = data

    def find(self, id: ID) -> RoadSegmentDTO:
        return self.data[id]

    def findAll(self) -> Dict[ID, RoadSegmentDTO]:
        return self.data.values()

    def save(self, data):
        self.data = data