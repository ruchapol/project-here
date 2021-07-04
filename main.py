from apiPrediction.service import PredictTravelTimeService
from mapper.modelDTOToLinearRegression import ModelDTOToLinearRegression
from repository.outbound import OutboundRepo
from travelTimeCalculator.travelTimeCalculator import TravelTimeCalculator
from predictionModel.predictionModelPredictor import PredictionModelPredictor
from repository.model import ModelRepo
from model.database.model import createModelDAO
from script.migrateTable import migrate
from predictionModel.predictionModelTrainer import PredictionModelTrainer
from utils.path import getPath
from model.ID import ID
from model.featureExtraction.input import APIInput
from typing import Dict
from script.collector import getAPIInputsFromXML
from pony import orm
from graph.graph import Graph
from repository.roadSegment import RoadSegmentRepo
from repository.dataSet import DataSetRepo
from repository.dataSet_mock import DataSetRepoMock
from model.database.roadSegment import createRoadSegmentDAO, createOutboundDAO
from model.database.dataset import createDatasetDAO
from featureExtraction.featureExtraction import FeatureExtraction, timerBenchmark
from script.collector import writeFileXML
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from predictionModel.predictionModel_v1 import PredictionModelV1
import matplotlib.pyplot as plt


def runExtraction(db: orm.Database):
    # create repo
    roadsegmentRepo = RoadSegmentRepo(roadsegmentDAO, outboundDAO)
    datasetRepo = DataSetRepo(roadsegmentDAO, datasetDAO)

    # create graph
    graph = Graph(roadsegmentRepo)
    featureExtraction: FeatureExtraction = FeatureExtraction(
        {}, datasetRepo, graph)
    # apiInputs = getAPIInputsFromXML([".","data","data20212905_013807.xml"])
    # data = featureExtraction.processInput(apiInputs)
    # featureExtraction.saveToDB(data)

    tfPath = getPath([".", "data2month_current"])
    for day in tqdm(listdir(tfPath)):
        for hour in tqdm(listdir(join(tfPath, day))):
            for minute in listdir(join(tfPath, day, hour)):
                xmlPath = join(tfPath, day, hour, minute)
                apiInputs: Dict[ID, APIInput] = getAPIInputsFromXML(xmlPath) # change to getAPIInputs from here api
                featureExtraction.setAPIInputs(apiInputs)
                datasets = featureExtraction.processInput()
                featureExtraction.saveToDB(datasets)
    print(timerBenchmark)


def runTrainModel():
    # create repo
    roadsegmentRepo = RoadSegmentRepo(roadsegmentDAO, outboundDAO)
    datasetRepo = DataSetRepo(roadsegmentDAO, datasetDAO)
    modelRepo = ModelRepo(roadsegmentDAO, modelDAO)
    # prepare Model
    predictionModel = PredictionModelV1()
    # prepare mapper
    mapper = ModelDTOToLinearRegression()

    predictionModelRunner = PredictionModelTrainer(
        roadsegmentRepo, datasetRepo, modelRepo, predictionModel, mapper)
    predictionModelRunner.train()


def runPredictModel():
    # create repo
    datasetRepo = DataSetRepo(roadsegmentDAO, datasetDAO)
    modelRepo = ModelRepo(roadsegmentDAO, modelDAO)
    # prepare Model
    predictionModel = PredictionModelV1()
    # prepare mapper
    mapper = ModelDTOToLinearRegression()

    predictionModelPredictor = PredictionModelPredictor(
        modelRepo, datasetRepo, predictionModel, mapper)
    predictResult = predictionModelPredictor.predictSpeedUncutFromNow(
        ID(RoadID="219-00566", SegmentID="40504"), "15")
    print("predictResult=", predictResult)


def runTravelTimeCalculator():
    # create repo
    outboundRepo = OutboundRepo(roadsegmentDAO, outboundDAO)
    travelTimeCalculator = TravelTimeCalculator(outboundRepo)
    idA = ID("219-57496", "57499")
    idB = ID("219-57496", "57498")
    timeTravel = travelTimeCalculator.calculateTravelTime(
        idA, idB, 10, 20)  # 2.83436370955463
    print(timeTravel)


def runPredictionAPI():
    # create repo
    datasetRepo = DataSetRepo(roadsegmentDAO, datasetDAO)
    modelRepo = ModelRepo(roadsegmentDAO, modelDAO)
    outboundRepo = OutboundRepo(roadsegmentDAO, outboundDAO)
    roadsegmentRepo = RoadSegmentRepo(roadsegmentDAO, outboundDAO)
    # prepare Model
    predictionModel = PredictionModelV1()
    # prepare dependencies
    mapper = ModelDTOToLinearRegression()
    travelTimeCalculator = TravelTimeCalculator(outboundRepo, roadsegmentRepo)
    predictionModelPredictor = PredictionModelPredictor(
        modelRepo, datasetRepo, predictionModel, mapper)

    predictionAPI = PredictTravelTimeService(
        predictionModelPredictor, travelTimeCalculator)
    print(predictionAPI.execute("พระจอม", "บางโพ"))


def runMapPlot():
    roadsegmentRepo = RoadSegmentRepo(roadsegmentDAO, outboundDAO)
    graph = Graph(roadsegmentRepo)
    nodes = graph.getNodes()
    fig, ax = plt.subplots()
    plt.xlabel("longitude")
    plt.ylabel("latitude")

    for key, value in nodes.items():
        if key.RoadID == 'none':
            continue
        [xOrigin, yOrigin] = value.getLatLong()
        if xOrigin == None or yOrigin == None:
            continue
        plt.plot([yOrigin], [xOrigin], marker='o',
                 color='lightblue')  # 1 plot graph
        # ax.annotate(value.getRoadName() ,
        #         (yOrigin, xOrigin), color="red")
        for neighbour in value.getNeighbourNodes():
            [x, y] = neighbour.getLatLong()
            if x == None or y == None:
                continue
            plt.plot([yOrigin, y], [xOrigin, x],
                     color='lightblue', linewidth=3)
            # print([xOrigin, x],[yOrigin, y])

    # plot destination and source
    marker_n = ["KMUTNB", "WONGSAWANG", "KRASAUNG", "BANGPO"]
    marker_lat = [13.818851, 13.82972, 13.84858, 13.806172]
    marker_long = [100.5138, 100.5266, 100.5147, 100.5215]
    plt.scatter(marker_long, marker_lat)
    for i in range(len(marker_n)):
        ax.annotate(marker_n[i], (marker_long[i], marker_lat[i]))

    plt.show()


if __name__ == '__main__':
    # writeFileXML()

    db = orm.Database()
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    roadsegmentDAO = createRoadSegmentDAO(db, orm)
    outboundDAO = createOutboundDAO(db, orm, roadsegmentDAO)
    datasetDAO = createDatasetDAO(db, orm, roadsegmentDAO)
    modelDAO = createModelDAO(db, orm, roadsegmentDAO)
    db.generate_mapping(create_tables=True)
    # migrate(db)
    # runExtraction(db)
    # runTrainModel()
    # runPredictModel()
    # runTravelTimeCalculator()
    runPredictionAPI()
    # runMapPlot()
