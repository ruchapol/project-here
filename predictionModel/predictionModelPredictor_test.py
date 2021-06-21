from predictionModel.predictionModel_v1 import PredictionModelV1
from model.database.model import ModelDTO
from repository.model_mock import ModelRepoMock
from model.ID import ID
from model.database.dataset import DataSetDTO
from repository.dataSet_mock import DataSetRepoMock
from mapper.modelDTOToLinearRegression_mock import ModelDTOToLinearRegressionMock
from predictionModel.predictionModelPredictor import PredictionModelPredictor
import unittest
from sklearn.linear_model import LinearRegression
import numpy as np


class TestPredictionModelPredictor(unittest.TestCase):
    def setUp(self):
        self.modelRepoMock = None

    def _get_FixedOutPutLinearRegressionModel(self, featureNumber: int = 1, fixedOutput:float = 9.0) -> LinearRegression:
        rlg = LinearRegression()
        setOfX = [[1] * featureNumber for x in range(featureNumber)]
        setOfY = [fixedOutput for y in range(featureNumber)]
        # rlg.fit(np.array([[0] * featureNumber, [1] * featureNumber]), [0, 9])
        rlg.fit(np.array(setOfX), setOfY)
        return rlg

    def test_predictSpeedUncutFromNow(self):
        modelRepo = ModelRepoMock()
        datasets = {
            ID("B", "B1"): [DataSetDTO().setAllFeature(1, 2, 3, 4, 5, 6, 7, 8, 9).setSpeedUncut(10).setTimestamp("2021-05-09T05:56:31Z"),
                            DataSetDTO().setAllFeature(2, 4, 6, 8, 10, 12, 14, 16, 18).setSpeedUncut(20).setTimestamp("2021-05-09T05:47:31Z")]
        }  # 1, 2, 3, 4, 5, 6, 7, 8, 9
        dataSetRepoMock: DataSetRepoMock = DataSetRepoMock(datasets)
        predictionModel = None
        # prepare model
        predictionModel = PredictionModelV1()
        predictionModel.setLinearRegressionModel({
            "5": self._get_FixedOutPutLinearRegressionModel(9),
            "15": self._get_FixedOutPutLinearRegressionModel(9),
            "30": self._get_FixedOutPutLinearRegressionModel(9),
            "45": self._get_FixedOutPutLinearRegressionModel(9),
            "60": self._get_FixedOutPutLinearRegressionModel(9),
        })
        iModelDtoMapper = ModelDTOToLinearRegressionMock(
            ModelDTO(), predictionModel)
        p = PredictionModelPredictor(
            modelRepo, dataSetRepoMock, predictionModel, iModelDtoMapper)
        preductResult = p.predictSpeedUncutFromNow(ID("B", "B1"), "5")
        self.assertEqual(preductResult, 9)
