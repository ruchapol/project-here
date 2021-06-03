from datetime import datetime, timedelta
import unittest
from interface.predictionModel import IPredictionModel
from typing import Dict, List, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression
from predictionModel.predictionModel_v1 import PredictionModelV1


class TestPredictionModelV1(unittest.TestCase):
    times = ["5","15","30","45","60"]


    def test_getShiftAmount(self):
        # prepare
        testcase = {
            "5": 1,
            "15": 3,
            "30": 6,
            "45": 9,
            "60": 12,
        }
        # execute
        p = PredictionModelV1()
        for arg, expectedVal in testcase.items():
            got = p.getShiftAmount(arg)

            # assert
            self.assertEqual(got, expectedVal)

    def test_isTimestampInRange(self):
        # prepare
        time_0 = datetime.strptime("2019-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        testcase = {
            (time_0, time_0 + timedelta(minutes=1)): True,
            (time_0, time_0 + timedelta(minutes=6)): False,
            (time_0, time_0 + timedelta(minutes=-6)): False,
        }
        # execute
        p = PredictionModelV1()
        for args, expectedVal in testcase.items():
            got = p.isTimestampInRange(args[0], args[1])

            # assert
            self.assertEqual(got, expectedVal)
        
    def test_shiftYByTime_case_5_minute(self):
        # prepare
        time_0 = datetime.strptime("2019-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        timestamp = [time_0 + timedelta(minutes=x) for x in range(0, 60, 5)]
        # execute
        p = PredictionModelV1()
        got = p.shiftYByTime(y, timestamp, "5")

        # assert
        self.assertEqual(got, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, None])
        
    def test_shiftYByTime_case_5_minute_withLoss(self):
        # prepare
        time_0 = datetime.strptime("2019-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        y = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12] # 5 is lost
        timestamp = [
            time_0 + timedelta(minutes=0),
            time_0 + timedelta(minutes=5),
            time_0 + timedelta(minutes=10),
            time_0 + timedelta(minutes=15),
            # time_0 + timedelta(minutes=20), dataset at 20th min lost 
            time_0 + timedelta(minutes=25),
            time_0 + timedelta(minutes=30),
            time_0 + timedelta(minutes=35),
            time_0 + timedelta(minutes=40),
            time_0 + timedelta(minutes=45),
            time_0 + timedelta(minutes=50),
            time_0 + timedelta(minutes=55),
        ] 
        
        # execute
        p = PredictionModelV1()
        got = p.shiftYByTime(y, timestamp, "5")

        # assert
        self.assertEqual(got, [2, 3, 4, None, 7, 8, 9, 10, 11, 12, None])
        

    def test_shiftYByTime_case_15_minute(self):
        # prepare
        time_0 = datetime.strptime("2019-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        timestamp = [time_0 + timedelta(minutes=x) for x in range(0, 60, 5)]
        # execute
        p = PredictionModelV1()
        got = p.shiftYByTime(y, timestamp, "15")

        # assert
        self.assertEqual(got, [4, 5, 6, 7, 8, 9, 10, 11, 12, None, None, None])
    
    def test_shiftYByTime_case_30_minute(self):
        # prepare
        time_0 = datetime.strptime("2019-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        timestamp = [time_0 + timedelta(minutes=x) for x in range(0, 60, 5)]
        # execute
        p = PredictionModelV1()
        got = p.shiftYByTime(y, timestamp, "30")

        # assert
        self.assertEqual(got, [7, 8, 9, 10, 11, 12, None, None, None, None, None, None])
    

    def test_removeByNoneInY(self):
        # prepare
        x = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
        y = [1, 2, None, 4, 5, 6, None, 8, 9, 10]

        #execute
        p = PredictionModelV1()
        newX, newY = p.removeByNoneInY(x, y)

        # assert
        self.assertEqual(newX, [[1], [2], [4], [5], [6], [8], [9], [10]])
        self.assertEqual(newY, [1, 2, 4, 5, 6, 8, 9, 10])

    def test_removeByNoneInY_caseXY_is_numpy(self):
        # prepare
        x = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
        y = np.array([1, 2, None, 4, 5, 6, None, 8, 9, 10])

        #execute
        p = PredictionModelV1()
        newX, newY = p.removeByNoneInY(x, y)

        # assert
        self.assertTrue((newX == np.array([[1], [2], [4], [5], [6], [8], [9], [10]])).all())
        self.assertTrue((newY == np.array([1, 2, 4, 5, 6, 8, 9, 10])).all())

    def test_shiftLeft(self):
        # prepare
        a = [1,2,3,4,5,6,7]
        predictModel = PredictionModelV1()

        # assert
        self.assertEqual([4,5,6,7,None,None,None], predictModel.shiftLeft(a, 3))
        self.assertEqual([3,4,5,6,7,None,None], predictModel.shiftLeft(a, 2))
        # case already shift
        a = predictModel.shiftLeft(a, 2)
        self.assertEqual([5,6,7,None,None,None,None], predictModel.shiftLeft(a, 2))
        
        
        

    # def train(self, x:List, y:List[float], timeStamp: List[str]):
    #     # X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    #     # y = np.dot(X, np.array([1, 2])) + 3
    #     # reg = LinearRegression().fit(X, y)
    #     np_x = np.array(x)
    #     self.numOfFeatures = np_x.shape[1]
    #     for minuteAhead, linearRegression in self.linearRegression.items():
    #         y = self._shiftY(y, timeStamp, minuteAhead)
    #         linearRegression.fit(np_x, y)

    
    # def predict(self, x:List) -> Dict[str, List[float]]:
    #     result = {}
    #     for time in self.times:
    #         result[time] = self.linearRegression[time].predict(x)
    #     return result

    # def getTheta(self) -> List[float]:
    #     return [self.linearRegression.intercept_, *self.linearRegression.coef_]

    # def getNumberOfFeature(self) -> int:
    #     return self.numOfFeatures


