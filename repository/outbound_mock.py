from model.database.roadSegment import OutboundDTO
from model.database.dataset import DataSetDTO
from model.ID import ID
from typing import Dict, List, Tuple

class OutboundRepoMock(OutboundDTO):
    data: Dict[Tuple[ID,ID], OutboundDTO]
    def __init__(self, data: Dict[ID, List[DataSetDTO]]):
        self.data = data

    def find(self, a: ID, b: ID) -> OutboundDTO:
        return self.data[(a, b)]

    def findAll(self) -> Dict[ID, OutboundDTO]:
        return self.data.values()

    def save(self, data):
        self.data = data