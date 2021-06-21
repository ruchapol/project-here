from interface.repository import IRepository
from model.ID import ID
from model.database.model import ModelDTO


class ModelRepoMock(IRepository):
    def find(self, id: ID) -> ModelDTO:
        return ModelDTO()

    def save(self, id: ID, model: ModelDTO):
        print("[ModelRepoMock] save")
