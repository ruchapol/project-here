from datetime import datetime, timedelta
import pickle
from model.database.model import ModelDTO
from interface.predictionModel import IPredictionModel
from typing import Dict, List, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression
from model.database.dataset import DataSetDTO
from interface.repository import IRepository
from utils.date import parseRFCtimeToDatetime
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


    def getShiftAmount(self, minuteAhead: str) -> int:
        return int(int(minuteAhead)/5) 

    def isTimestampInRange(self, expected_time:datetime, got_time:datetime, delta_minute:int=5) -> bool:
        return abs((expected_time - got_time).total_seconds()) / 60 <= delta_minute

    def shiftYByTime(self, y:List[float], timeStamp: List[datetime], minuteAhead: str) -> List[float]:
        shiftAmount = self.getShiftAmount(minuteAhead)
        newY = []
        for idx, time in enumerate(timeStamp):
            expected = time + timedelta(minutes=int(minuteAhead))
            currentIdx = idx + shiftAmount
            if currentIdx >= len(timeStamp):
                newY.append(None)
                continue
            while currentIdx > idx and not self.isTimestampInRange(expected, timeStamp[currentIdx], delta_minute=2.5):
                currentIdx -= 1
            if currentIdx == idx:
                newY.append(None)
            else:
                newY.append(y[currentIdx])
        return newY
    
    def removeByNoneInY(self, x:List[float], y:List[float]) -> Tuple[List[float],List[float]]:
        if len(x) != len(y):
            raise Exception("len y is not equal to x")
        newX = []
        newY = []
        for index, itemY in enumerate(y):
            if itemY is not None:
                newX.append(x[index])
                newY.append(itemY)
        return (newX,newY)

    # def shiftYByTime(self, y:List[float], timeStamp: List[datetime], minuteAhead: str) -> List[float]:
    #     shiftAmount = self.getShiftAmount(minuteAhead)
    #     expected = timeStamp[0] + timedelta(minutes=int(minuteAhead))
    #     if self.isTimestampInRange(expected, timeStamp[shiftAmount]):
    #         return self.shiftLeft(y, shiftAmount)
    #     # case Time is not in range
    #     while shiftAmount > 0 and not self.isTimestampInRange(expected, timeStamp[shiftAmount]):
    #         shiftAmount = shiftAmount - 1
    #     if shiftAmount == 0:
    #         return None
    #     return self.shiftLeft(y, shiftAmount)
        
    # [1,2,3] shiftLeft(1) --> [2,3,None]
    def shiftLeft(self, y:List, time: int) -> List[float]:
        return y[time:] + [None]*time

    def train(self, x:List, y:List[float], timeStamp: List[str]):
        # X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        # y = np.dot(X, np.array([1, 2])) + 3
        # reg = LinearRegression().fit(X, y)
        np_x = np.array(x)
        self.numOfFeatures = np_x.shape[1]
        for minuteAhead, linearRegression in self.linearRegression.items():
            newY = self.shiftYByTime(y, timeStamp, minuteAhead)
            newX, newY = self.removeByNoneInY(x, newY)
            if len(newX) == 0 or len(newY) == 0:
                raise Exception("len x or len y is zero")
            linearRegression.fit(newX, newY)


        # print(reg.score(X, y))
        # print(reg.predict(np.array([[3, 5]])))

    def load(self, model: ModelDTO):
        self.linearRegression["5"] = pickle.loads(model.Model_5)
        self.linearRegression["15"] = pickle.loads(model.Model_15)
        self.linearRegression["30"] = pickle.loads(model.Model_30)
        self.linearRegression["45"] = pickle.loads(model.Model_45)
        self.linearRegression["60"] = pickle.loads(model.Model_60)
    
    def setLinearRegressionModel(self, linear: Dict[str, LinearRegression]):
        self.linearRegression["5"] = linear["5"]
        self.linearRegression["15"] = linear["15"]
        self.linearRegression["30"] = linear["30"]
        self.linearRegression["45"] = linear["45"]
        self.linearRegression["60"] = linear["60"]

    def predict(self, x:List) -> Dict[str, List[float]]:
        result = {}
        for time in self.times:
            result[time] = self.linearRegression[time].predict(x)
        return result

    def getTheta(self) -> List[float]:
        return [self.linearRegression.intercept_, *self.linearRegression.coef_]

    def getModel(self, minutes: str) -> any:
        return self.linearRegression[minutes]

    def getNumberOfFeature(self) -> int:
        return self.numOfFeatures


