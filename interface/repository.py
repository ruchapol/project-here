from typing import Dict
class IRepository:
    def find(self, args: Dict):
        raise NotImplementedError

    def findAll(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError