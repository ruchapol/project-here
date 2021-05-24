from model.HereApiResult import HereApiResult
from interface.repository import IRepository
from interface.graph import IGraph
from interface.featureExtraction import IFeatureExtraction, ID
from model.featureExtraction.input import APIInput
from model.featureExtraction.feature import Feature
from typing import List, Tuple, Dict


class FeatureExtraction(IFeatureExtraction):
    APIInputs: Dict[ID, APIInput]
    featureRepo: IRepository
    graph: IGraph
    def __init__(self, data: Dict[ID, APIInput], repo: IRepository, graph: IGraph):
        self.APIInputs = data
        self.featureRepo = repo
        self.graph = graph

    def processInput(self, x: List[APIInput]):


        return 1

    def saveToDB(self, id: ID, features: List[Feature], su: List[float]):
        self.featureRepo.save(features)

#   def _calJamFactorDuration(self, id:ID, ) -> float:

#   def _calDeltaJamFactor(self, id:ID, ) -> float:

    def calNeightbourJamFactor(self, id:ID) -> float:
        v = 0
        neighbours = self.graph.getNodeByID(id).getNeighbourNodes()
        for neightbour in neighbours:
            v += self.APIInputs[neightbour.getID()].JamFactor
        return v / len(neighbours)

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
