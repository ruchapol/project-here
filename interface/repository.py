class IRepository:
    def find(self):
        raise NotImplementedError

    def findAll(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError