from interface.repository import IRepository
from model.database.dataset import DataSetDTO
from model.ID import ID
from typing import Dict, List
from repository.dataSet import QueryOption
class DataSetRepoMock(IRepository):
    data: Dict[ID, List[DataSetDTO]]
    def __init__(self, data: Dict[ID, List[DataSetDTO]]):
        self.data = data

    def find(self,id: ID, options: QueryOption):
        if id not in self.data:
            return [None]
        if options.wantLastest(): # sorted with dsc 
            return self.data[id][:1]
        return self.data[id]

        
    
    def findAll(self):
        return [self.data]

    def save(self, data):
        self.data = data