from interface.repository import IRepository

class PlusService:
    repo: IRepository
    def __init__(self, repo: IRepository):
        self.repo = repo
    def execute(self, num) -> str:
        a = int(self.repo.find())
        return str(int(num)+a)
