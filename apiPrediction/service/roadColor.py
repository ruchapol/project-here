from model.database.roadSegment import RoadSegmentDTO
from typing import Dict
from model.database.dataset import DataSetDTO
from repository.dataSet import QueryOption
from interface.repository import IRepository
from re import I
from travelTimeCalculator.travelTimeCalculator import TravelTimeCalculator
from predictionModel.predictionModelPredictor import PredictionModelPredictor
from model.ID import ID
from datetime import timedelta
import numpy as np


class RoadColorService:
    datasetRepo: IRepository
    roadSegmentRepo: IRepository

    def __init__(self, datasetRepo: IRepository, roadSegmentRepo: IRepository):
        self.datasetRepo = datasetRepo
        self.roadSegmentRepo = roadSegmentRepo

    def execute(self) -> str:
        colors = {}
        try:
            roadSegments: Dict[ID, RoadSegmentDTO] = self.roadSegmentRepo.findAll()
            for id,val in roadSegments.items():
                queryOption: QueryOption = QueryOption()
                queryOption.setOption(QueryOption.Latest, "true")
                latestDataSet: DataSetDTO = self.datasetRepo.find(id, queryOption)[0]
                if latestDataSet is None:
                    continue
                if id.RoadID in colors:
                    colors[id.RoadID][id.SegmentID] = self.getColorByJamFactor(latestDataSet.JamFactor)
                else:
                    colors[id.RoadID] = {id.SegmentID: self.getColorByJamFactor(latestDataSet.JamFactor)}

        except KeyError as ke:
            print("keyEror",ke)
            return {"status": 500, "color": colors, "error": "KeyError"}
        # second
        return {"status": 200, "color": colors}

    def getColorByJamFactor(self, jf:float) -> str:
        jf_color = "Green"
        if (jf < 4):
            jf_color = "Green"
        if (jf >= 4 and jf < 8):
            jf_color = "Yellow"
        if (jf >= 8 and jf < 10):
            jf_color = "Red"
        if (jf >= 10.0):
            jf_color = "Black"
        return jf_color
