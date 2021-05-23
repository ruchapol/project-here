from utils.path import getPath
from playground.play_untangle import run
from pony import orm
from model.database.roadSegment import *
from pony.orm import db_session, select, get
from typing import Dict, List
import csv

roadSegmentPath = [".", "data", "geo_with_ajacant.csv"]

NONE = 'none'
NONE_SEGMENT_DICT = {
    'RoadID': NONE,
    'RoadSegmentID': NONE,
    'RoadDescription': 'Unknown Road',
    'SegmentDescription': 'Unknown Description',
    'LatLong': NONE,
}


@db_session
def createSegment(roadSegmentDAO, data: Dict):
    latlong = data["LatLong"]
    if not latlong:
        latlong = NONE
    r = roadSegmentDAO(RoadID=data['RoadID'], RoadSegmentID=data['RoadSegmentID'],
                       RoadDescription=data['RoadDescription'],
                       RoadSegmentDescription=data['SegmentDescription'], LatLong=latlong)
    return r


@db_session
def createOutbound(roadSegmentDAO, outboundDAO):
    road1 = get(p for p in roadSegmentDAO if p.RoadID == "1")
    road2 = get(p for p in roadSegmentDAO if p.RoadID == "2800")
    road3 = get(p for p in roadSegmentDAO if p.RoadID == "2900")
    outboundDAO(From=road1, To=road2)


@db_session
def addOutbound(o, a, b):
    o(From=a, To=b)


@db_session
def query(roadSegmentDAO):
    # q = select((p.RoadID, p.From) for p in roadSegmentDAO)
    # for i in q:
    #     print(i)
    # print("hi")
    t= roadSegmentDAO["219+57496","57499"]
    print("original: ", t)    
    for x in t.From:
        print(x.From, x.To)
    print("------------")
    for x in t.To:
        print(x)
    return t


@db_session
def queryOut(outbound):
    q = select((p.FromID.RoadDescription, p.ToID.RoadDescription)
               for p in outbound)
    for i in q:
        print(i)


def countEmpty(*list: List[str]) -> int:
    c = 0
    emptyList = ['', 'out']
    for i in list:
        if i in emptyList:
            c += 1
    return c


@db_session
def insert_database(roadSegmentDAO, outboundDAO):
    noneLocation = createSegment(roadSegmentDAO, NONE_SEGMENT_DICT)
    roadMap: Dict = {(NONE, NONE): noneLocation}
    remainOutbound: Dict = {}
    with open(getPath(roadSegmentPath), encoding='utf-8-sig') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            currentRoad = (row['RoadID'], row['RoadSegmentID'])
            if currentRoad in roadMap:
                continue
            roadMap[currentRoad] = createSegment(roadSegmentDAO, row)

            if currentRoad in remainOutbound:
                for from_s in remainOutbound[currentRoad]:
                    addOutbound(outboundDAO, from_s, roadMap[currentRoad])

            for i in range(1, 5):
                outbound = row['Outbound'+str(i)]
                pc = row['PC'+str(i)]
                countEmptyColumn = countEmpty(outbound, pc)
                if countEmptyColumn == 1:
                    outbound = NONE
                    pc = NONE

                outboundRoad = (outbound, pc)
                if outboundRoad in roadMap:
                    addOutbound(outboundDAO, currentRoad,
                                roadMap[outboundRoad])
                else:
                    if outboundRoad in remainOutbound:
                        remainOutbound[outboundRoad].append(currentRoad)
                    else:
                        remainOutbound[outboundRoad] = [currentRoad]


def migrate():
    # create db
    db = orm.Database()
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    roadSegmentDAO = roadSegment_DAO(db, orm)
    outboundDAO = outbound_DAO(db, orm, roadSegmentDAO)
    db.generate_mapping(create_tables=True)

    # read file and put to db
    # insert_database(roadSegmentDAO, outboundDAO)
    query(roadSegmentDAO)

