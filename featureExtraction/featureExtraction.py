from model.HereApiResult import HereApiResult
from interface.repository import IRepository
from interface.featureExtraction import IFeatureExtraction
from model.featureExtraction.input import Input
from model.featureExtraction.feature import Feature
from typing import List, Tuple


class FeatureExtraction(IFeatureExtraction):
    def __init__(self, data: Input, repo: IRepository, graph):
        self.data = data
        self.repo = repo

    def processInput(self, x):
        return 1

    def saveToDB(self, id: Tuple[RoadID:str, SegmentID:str], features: List[Feature], su: List[float]):
        self.repo.save(features)
