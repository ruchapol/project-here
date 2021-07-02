from re import I
from travelTimeCalculator.travelTimeCalculator import TravelTimeCalculator
from predictionModel.predictionModelPredictor import PredictionModelPredictor
from model.ID import ID
from datetime import timedelta
import numpy as np


class PredictTravelTimeService:
    predictor: PredictionModelPredictor
    travelTimeCalculator: TravelTimeCalculator

    def __init__(self, predictor: PredictionModelPredictor, travelTimeCalculator: TravelTimeCalculator):
        self.predictor = predictor
        self.travelTimeCalculator = travelTimeCalculator

    def execute(self, source: str, destination: str, miniteAhead: str = "5") -> str:
        paths = self.shortest_path(source, destination)
        i = 0
        timeTravel = 0
        while i < len(paths) - 1:
            idA = paths[i]
            idB = paths[i+1]
            speedA = self.predictor.predictSpeedUncutFromNow(idA, miniteAhead)
            speedB = self.predictor.predictSpeedUncutFromNow(idB, miniteAhead)
            timeTravelAToB = self.travelTimeCalculator.calculateTravelTimeNoOutbound(
                idA, idB, speedA, speedB)
            timeTravel += timeTravelAToB
            i += 1
        return timedelta(hours=np.float64(timeTravel)).total_seconds() # second

    def shortest_path(self, start_point="พระจอม", dest_point="วงศ์สว่าง"):
        # marker_n = ["พระจอม", "วงศ์สว่าง", "กระทรวง", "บางโพ"]
        if(start_point == "พระจอม" and dest_point == "วงศ์สว่าง"):
            route_seg = [ID('219-02960', '47760'), ID('219+00639', '22033'),
                         ID('219+00639', '22024'), ID('219+00639', '22023'),
                         ID('219+00639', '22022'), ID('219-02600', '46771'),
                         ID('219-02600', '46772')]
        elif(start_point == "พระจอม" and dest_point == "กระทรวง"):
            route_seg = [ID('219+57505', '57506'), ID('219-02628', '46846'),
                         ID('219+57500', '57504'), ID('219+57500', '57503'),
                         ID('219+57500', '57502'), ID('219+02600', '46774'),
                         ID('219+02600', '46773'), ID('219+02600', '46772'),
                         ID('219+02600', '46771')]
        elif(start_point == "พระจอม" and dest_point == "บางโพ"):
            route_seg = [ID('219-00661', '35516'), ID('219-00661', '35517'),
                         ID('219-00661', '35518'), ID('219-02600', '46771'),
                         ID('219-02600', '46772')]
        else:
            route_seg = []

        return route_seg
