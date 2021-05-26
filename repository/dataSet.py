from re import L
from typing import Dict, List
from interface.repository import IRepository
from pony.orm import db_session, select, get
from pony import orm
from model.database.dataset import DataSetDTO
from model.ID import ID

class QueryOption:
    Latest: str = 'latest'
    Limit: str = 'limit'
    queryOption: Dict
    def __init__(self):
        self.queryOption = {}

    def setOption(self, key:str, value:str):
        self.queryOption[key] = value
        
    def wantLastest(self) -> bool:
        return self.queryOption[QueryOption.Latest] == "true"

    def limit(self) -> int:
        limit = self.queryOption[QueryOption.Limit]
        if type(limit) != int:
            return -1
        else:
            return limit

class DataSetRepo(IRepository):
    datasetDAO = None
    def __init__(self, datasetDAO):
        self.datasetDAO = datasetDAO

    @db_session
    def find(self, id: ID, options: QueryOption) -> DataSetDTO:
        pass
    
    @db_session
    def findAll(self) -> Dict[ID, DataSetDTO]:
        pass

    def save(self, data):
        super().save(self)
