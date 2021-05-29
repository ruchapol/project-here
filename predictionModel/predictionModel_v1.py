from datetime import datetime
from interface.predictionModel import IPredictionModel
from typing import Dict, List, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression
from model.database.dataset import DataSetDTO
from interface.repository import IRepository

# class LinearRegWithInitTheta(LinearRegression):

#     def __init__(self, *, theta, fit_intercept=fit_intercept, normalize=normalize, copy_X, n_jobs, positive):
#         super().__init__(fit_intercept, normalize, copy_X, n_jobs, positive)

class PredictionModelV1(IPredictionModel):
    linearRegression: Dict[str, LinearRegression] 
    numOfFeatures: int
    times = ["5","15","30","45","60"]

    def __init__(self, thetas:List[float] = []):
        self.linearRegression = {}
        for time in self.times:
            self.linearRegression[time] = LinearRegression()
        self.numOfFeatures = None

    def _parseRFCtimeToDatetime(self, dateStr: str) -> datetime:
        # 2021-05-09T05:56:31Z
        date_object = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
        return date_object

    def train(self, x:List, y:List[float], timeStamp: List[str]):
        # X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        # y = np.dot(X, np.array([1, 2])) + 3
        # reg = LinearRegression().fit(X, y)
        np_x = np.array(x)
        self.linearRegression.fit(np_x, y)
        self.numOfFeatures = np_x.shape[1]

        # print(reg.score(X, y))
        # print(reg.predict(np.array([[3, 5]])))

    
        # [[x...], [x...], [x...], ...], [y, y, y, ...]]

    def predict(self, x:List) -> Dict[str, List[float]]:
        result = {}
        for time in self.times:
            result[time] = self.linearRegression[time].predict(x)
        return result

    def getTheta(self) -> List[float]:
        return [self.linearRegression.intercept_, *self.linearRegression.coef_]

    def getNumberOfFeature(self) -> int:
        return self.numOfFeatures


