from typing import List, Tuple
from model.featureExtraction.feature import Feature
from model.ID import ID

class IFeatureExtraction:

    def processInput(self, x: List):
        raise NotImplementedError

    def saveToDB(self, id: ID, feature: List, su: float):
        raise NotImplementedError
