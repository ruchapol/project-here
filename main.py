from script.collector import runXML
from typing import List
from pony import orm
from script.migrateTable import migrate
from graph.graph import Graph
from repository.roadSegment import RoadSegmentRepo
from model.database.roadSegment import createRoadSegmentDAO, createOutboundDAO
from model.database.feature import createDatasetDAO

if __name__ == '__main__':
    db = orm.Database()
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    roadSegmentDAO = createRoadSegmentDAO(db, orm)
    outboundDAO = createOutboundDAO(db, orm, roadSegmentDAO)
    datasetDAO = createDatasetDAO(db, orm, roadSegmentDAO)
    db.generate_mapping(create_tables=True)
    # migrate(db)
    # runXML([".","data","data.xml"])
    roadSegmentRepo = RoadSegmentRepo(roadSegmentDAO, outboundDAO)
    graph = Graph(roadSegmentRepo)





   