from pony import orm
from script.migrateTable import migrate
from pony.orm.core import db_session, desc, select

@db_session
def query(roadSegmentDAO):
    t = roadSegmentDAO["219-00566","40504"]
    for f in t.Features:
        print(f.SpeedUncut)

@db_session
def queryWithRoadSegment(roadSegmentDAO):
    features = select(x for x in roadSegmentDAO["219-00566","405045"].Features).order_by(lambda: desc(x.TimeStamp))
    print("features = ",features)
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
    migrate(db)






   