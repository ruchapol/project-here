from interface.repository import IRepository

class TrafficRepo(IRepository):
    data: int = 999
    def find(self):
        return self.data

    def findAll(self):
        return [self.data]

    def save(self, data):
        self.data = data