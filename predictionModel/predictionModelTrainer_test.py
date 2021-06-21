from interface.modelDTOMapper import IModelDTOMapper
from repository.model_mock import ModelRepoMock
import unittest
from predictionModel.predictionModelTrainer import PredictionModelTrainer
from interface.repository import IRepository
from interface.predictionModel import IPredictionModel
from typing import Tuple, List
from repository.roadSegment_mock import RoadSegmentRepoMock
from repository.dataSet_mock import DataSetRepoMock
from model.ID import ID
from model.database.dataset import DataSetDTO
from utils.date import parseRFCtimeToDatetime

class PredictionModelForTest(PredictionModelTrainer):

    def __init__(self, roadSegmentRepo: IRepository, datasetRepo: IRepository, modelRepo: IRepository, predictionModel: IPredictionModel, mapper: IModelDTOMapper):
        super().__init__(roadSegmentRepo, datasetRepo, modelRepo, predictionModel, mapper)

    def fillAverageIfNone(self, xy: Tuple[List,List]):
        return self._fillAverageIfNone(xy)

    def dataSetDTOListToXY(self, datasets: List[DataSetDTO]):
        return self._dataSetDTOListToXY(datasets)

class TestPredictionModelTrainer(unittest.TestCase):

    p: PredictionModelForTest
    def setUp(self):
        # self.p = PredictionModelForTest(RoadSegmentRepoMock({}), DataSetRepoMock({}), None)
        self.p = PredictionModelForTest(None, None, None, None, None) 

    def tearDown(self):
        del self.p

    def test_fillAverageIfNone(self):

        xy = ([[0, 10, 20], 
               [0, 10, 20], 
               [None, None, None], 
               [10, 20, 30], 
               [10, 20, 30]], 
               [1, 2, 3, 4, 5])
        
        filledXY = self.p.fillAverageIfNone(xy)
        expectedFilledXY = ([[0, 10, 20], 
                             [0, 10, 20], 
                             [5, 15, 25], 
                             [10, 20, 30], 
                             [10, 20, 30]], 
                             [1, 2, 3, 4, 5])

        self.assertEqual(expectedFilledXY, filledXY)
        self.assertEqual(expectedFilledXY, xy)

    def test_dataSetDTOListToXY(self):
        datasets = [DataSetDTO().setAllFeature(1, 2, 3, 4, 5, 6, 7, 8, 9).setSpeedUncut(10).setTimestamp("2021-05-09T05:56:31Z"),
                    DataSetDTO().setAllFeature(2, 4, 6, 8, 10, 12, 14, 16, 18).setSpeedUncut(20).setTimestamp("2021-05-09T05:47:31Z")]

        xy = self.p.dataSetDTOListToXY(datasets)

        expectedXY = ([[1, 2, 3, 4, 5, 6, 7, 8, 9], [2, 4, 6, 8, 10, 12, 14, 16, 18]], 
                      [10, 20], 
                      [parseRFCtimeToDatetime("2021-05-09T05:56:31Z"), parseRFCtimeToDatetime("2021-05-09T05:47:31Z")])
        
        self.assertEqual(expectedXY, xy)