from apiPrediction.service.roadColor import RoadColorService
from travelTimeCalculator.travelTimeCalculator import TravelTimeCalculator
from predictionModel.predictionModelPredictor import PredictionModelPredictor
from mapper.modelDTOToLinearRegression import ModelDTOToLinearRegression
from interface.predictionModel import IPredictionModel
from repository.roadSegment import RoadSegmentRepo
from repository.outbound import OutboundRepo
from repository.model import ModelRepo
from repository.dataSet import DataSetRepo
from model.database.model import createModelDAO
from model.database.dataset import createDatasetDAO
from pony import orm
from model.database.roadSegment import createOutboundDAO, createRoadSegmentDAO
from flask import Flask
from apiPrediction.service.predictTime import PredictTravelTimeService
from apiPrediction.controller.predictTime import getBlueprint as getBlueprintPredictTime
from apiPrediction.controller.roadColor import getBlueprint as getBlueprintRoadColor
from api.controller.health import health_blueprint

app = Flask(__name__)

# db init
db = orm.Database()
db.bind(provider='sqlite', filename='database.db', create_db=True)
roadsegmentDAO = createRoadSegmentDAO(db, orm)
outboundDAO = createOutboundDAO(db, orm, roadsegmentDAO)
datasetDAO = createDatasetDAO(db, orm, roadsegmentDAO)
modelDAO = createModelDAO(db, orm, roadsegmentDAO)
db.generate_mapping(create_tables=True)


def getPredictTravelTimeService():
    # prepare Model
    predictionModel = IPredictionModel()
    # prepare dependencies
    mapper = ModelDTOToLinearRegression()
    travelTimeCalculator = TravelTimeCalculator(
        outboundRepo, roadsegmentRepo)
    predictionModelPredictor = PredictionModelPredictor(
        modelRepo, datasetRepo, predictionModel, mapper)
    return PredictTravelTimeService(predictionModelPredictor, travelTimeCalculator)

# Repo
datasetRepo = DataSetRepo(roadsegmentDAO, datasetDAO)
modelRepo = ModelRepo(roadsegmentDAO, modelDAO)
outboundRepo = OutboundRepo(roadsegmentDAO, outboundDAO)
roadsegmentRepo = RoadSegmentRepo(roadsegmentDAO, outboundDAO)
# Service
predictTravelTimeService = getPredictTravelTimeService()
roadColorService = RoadColorService(datasetRepo, roadsegmentRepo)
# Route
app.register_blueprint(getBlueprintPredictTime(predictTravelTimeService))
app.register_blueprint(getBlueprintRoadColor(roadColorService))
app.register_blueprint(health_blueprint)

if __name__ == "__main__":
    app.run(host="127.0.0.1")
