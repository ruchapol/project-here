from typing import List
from pony import orm
from script.migrateTable import migrate
from graph.graph import Graph
from repository.roadSegment import RoadSegmentRepo


if __name__ == '__main__':
    db = orm.Database()
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    migrate(db)
    # roadSegmentRepo = RoadSegmentRepo(db)
    # graph = Graph(roadSegmentRepo)





   