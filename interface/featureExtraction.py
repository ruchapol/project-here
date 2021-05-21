from model.featureExtraction.feature import Feature


class IFeatureExtraction:

    def processInput(self, x):
        raise NotImplementedError

    def saveToDB(self, id: Tuplu[RoadID:str, SegmentID:str], feature: List[Feature], su: float):
        raise NotImplementedError
