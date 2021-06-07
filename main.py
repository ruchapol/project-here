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


def runExtraction(db: orm.Database):
    roadsegmentDAO = createRoadSegmentDAO(db, orm)
    outboundDAO = createOutboundDAO(db, orm, roadsegmentDAO)
    datasetDAO = createDatasetDAO(db, orm, roadsegmentDAO)
    db.generate_mapping(create_tables=True)
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
                apiInputs: Dict[ID, APIInput] = getAPIInputsFromXML(xmlPath)
                featureExtraction.setAPIInputs(apiInputs)
                datasets = featureExtraction.processInput()
                featureExtraction.saveToDB(datasets)
    print(timerBenchmark)


def runTrainModel():
    roadsegmentDAO = createRoadSegmentDAO(db, orm)
    outboundDAO = createOutboundDAO(db, orm, roadsegmentDAO)
    datasetDAO = createDatasetDAO(db, orm, roadsegmentDAO)
    modelDAO = createModelDAO(db, orm, roadsegmentDAO)
    db.generate_mapping(create_tables=True)
    # create repo
    roadsegmentRepo = RoadSegmentRepo(roadsegmentDAO, outboundDAO)
    datasetRepo = DataSetRepo(roadsegmentDAO, datasetDAO)
    modelRepo = ModelRepo(roadsegmentDAO, modelDAO)
    # prepare Model
    predictionModel = PredictionModelV1()

    predictionModelRunner = PredictionModelTrainer(
        roadsegmentRepo, datasetRepo, modelRepo, predictionModel)
    predictionModelRunner.train()


if __name__ == '__main__':
    # writeFileXML()

    db = orm.Database()
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    # runExtraction(db)
    # runTrainModel()
    # migrate(db)
