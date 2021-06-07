from pony.orm.core import get
from interface.repository import IRepository
from model.ID import ID
from pony.orm import db_session
from model.database.model import ModelDTO


class ModelRepo(IRepository):
    modelDAO = None
    roadSegmentDAO = None

    def __init__(self, roadSegmentDAO, modelDAO):
        self.modelDAO = modelDAO
        self.roadSegmentDAO = roadSegmentDAO

    @db_session
    def find(self, id: ID) -> ModelDTO:
        # access Model_DAO of ID
        ModelDAO = get(self.roadSegmentDAO[id.RoadID, id.SegmentID].Model)
        return ModelDTO().setModel(ModelDAO)

    @db_session
    def save(self, id: ID, model: ModelDTO):
        modelDAO = self.modelDAO.get(
            RoadSegment=self.roadSegmentDAO[id.RoadID, id.SegmentID])
        if modelDAO:
            modelDAO.set(
                RoadSegment=self.roadSegmentDAO[id.RoadID,
                                                id.SegmentID],
                Model_5=model.Model_5,
                Model_15=model.Model_15,
                Model_30=model.Model_30,
                Model_45=model.Model_45,
                Model_60=model.Model_60,
            )
            return
        self.modelDAO(
            RoadSegment=self.roadSegmentDAO[id.RoadID,
                                            id.SegmentID],
            Model_5=model.Model_5,
            Model_15=model.Model_15,
            Model_30=model.Model_30,
            Model_45=model.Model_45,
            Model_60=model.Model_60,
        )
