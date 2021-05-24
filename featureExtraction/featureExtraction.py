from model.HereApiResult import HereApiResult
from interface.repository import IRepository
from interface.graph import IGraph
from interface.featureExtraction import IFeatureExtraction, ID
from model.featureExtraction.input import APIInput
from model.featureExtraction.feature import Feature
from typing import List, Tuple


class FeatureExtraction(IFeatureExtraction):
    data: List[APIInput]
    repo: IRepository
    graph: IGraph
    def __init__(self, data: List[APIInput], repo: IRepository, graph: IGraph):
        self.data = data
        self.repo = repo
        self.graph = graph

    def processInput(self, x: List[APIInput]):


        return 1

    def saveToDB(self, id: ID, features: List[Feature], su: List[float]):
        self.repo.save(features)

#   def _calJamFactorDuration(self, id:ID, ) -> float:

#   def _calDeltaJamFactor(self, id:ID, ) -> float:

#   def _calNeightbourJamFactor(self, id:ID, ) -> float:
#       use graph dependency

#   def _calNeightbourJamFactorDuration(self, id:ID) -> float:
#       may be call _calNeightbourJamFactor()
#       use graph dependency


    # DayOfWeek: int
    # Day: int
    # Hour: int
    # Minute: int
    # JamFactor: float
    # JamFactorDuration: int
    # DeltaJamFactor: int
    # NeightbourJamFactor: float
    # NeightbourJamFactorDuration: int
    # TimeStamp: str
