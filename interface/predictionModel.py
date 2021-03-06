from typing import Dict, List

class IPredictionModel:
    
    # x is list of dataclass or object, y is list of result(float)
    def train(self, x:List, y:List[float], timestamp:List[str]):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def predict(self, x:List) -> Dict[str, List[float]]:
        raise NotImplementedError

    def getTheta(self) -> List[float]:
        raise NotImplementedError

    def getNumberOfFeature(self) -> int:
        raise NotImplementedError

    def getModel(self) -> any:
        raise NotImplementedError
