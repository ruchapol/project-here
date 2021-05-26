from pony.orm.core import db_session, desc, select
from script.collector import runXML
from typing import List
from pony import orm
from script.migrateTable import migrate
from graph.graph import Graph
from repository.roadSegment import RoadSegmentRepo
from model.database.roadSegment import createRoadSegmentDAO, createOutboundDAO
from model.database.dataset import createDatasetDAO

@db_session
def query(roadSegmentDAO):
    t = roadSegmentDAO["219-00566","40504"]
    for f in t.Features:
        print(f.SpeedUncut)

@db_session
def queryWithRoadSegment(roadSegmentDAO):
    features = select(x for x in roadSegmentDAO["219-00566","40504"].Features).order_by(lambda: desc(x.TimeStamp))
    for f in features:
        print(f.SpeedUncut)


@db_session
def queryDataset(datasetDAO):
    sorted_t = select(x for x in datasetDAO).order_by(lambda: desc(x.TimeStamp))
    for f in sorted_t:
        print(f.SpeedUncut)
        break

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
    # queryWithRoadSegment(roadSegmentDAO)
    # queryDataset(datasetDAO)





   