from model.database.model import createModelDAO
from utils.path import getPath
from playground.play_untangle import run
from pony import orm
from model.database.roadSegment import *
from model.database.dataset import *
from pony.orm import db_session, select, get
from typing import Dict, List
from model.ID import ID
from geopy.distance import geodesic
import csv

roadSegmentPath = [".", "data", "geo_with_ajacant.csv"]

NONE_CONSTANT = 'none'
NONE_SEGMENT_DICT = {
    'RoadID': NONE_CONSTANT,
    'RoadSegmentID': NONE_CONSTANT,
    'RoadDescription': 'Unknown Road',
    'SegmentDescription': 'Unknown Description',
    'LatLong': NONE_CONSTANT,
}


@db_session
def createOrGetSegment(roadSegmentDAO, data: Dict):
    latlong = data["LatLong"]
    if not latlong:
        latlong = NONE_CONSTANT
    o = roadSegmentDAO.get(RoadID=data['RoadID'], RoadSegmentID=data['RoadSegmentID'])
    if o:
        return o
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
    if a.LatLong != NONE_CONSTANT and b.LatLong != NONE_CONSTANT:
        (aLat, aLong) = a.LatLong.split(',')
        (bLat, bLong) = b.LatLong.split(',')
        o(From=a, To=b, Distance=geodesic((aLat, aLong), (bLat, bLong)).kilometers)
    else:
        o(From=a, To=b)


@db_session
def query(roadSegmentDAO):
    # q = select((p.RoadID, p.From) for p in roadSegmentDAO)
    # for i in q:
    #     print(i)
    # print("hi")
    t = select(x for x in roadSegmentDAO)
    r :List[RoadSegmentDTO] = []
    for a in t:
        new_r = RoadSegmentDTO()
        new_r.RoadID = a.RoadID
        new_r.RoadSegmentID = a.RoadSegmentID
        new_r.RoadDescription = a.RoadDescription
        new_r.RoadSegmentDescription = a.RoadSegmentDescription
        new_r.LatLong = a.LatLong
        toTmp = [t.To for t in a.From]
        new_r.To = [ID(x.RoadID,x.RoadSegmentID) for x in toTmp]
        r.append(new_r)
    # print("original: ", t)    
    # a = [x.To for x in t.From]
    # a = [(x.RoadID,x.RoadSegmentID) for x in a]
    # print(a)
    return r


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
    noneLocation = createOrGetSegment(roadSegmentDAO, NONE_SEGMENT_DICT)
    roadMap: Dict = {(NONE_CONSTANT, NONE_CONSTANT): noneLocation}
    remainOutbound: Dict = {}
    with open(getPath(roadSegmentPath), encoding='utf-8-sig') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            currentRoad = (row['RoadID'], row['RoadSegmentID'])
            if currentRoad in roadMap:
                continue
            roadMap[currentRoad] = createOrGetSegment(roadSegmentDAO, row)

            if currentRoad in remainOutbound: # add outbound to added road
                for from_s in remainOutbound[currentRoad]:
                    addOutbound(outboundDAO, from_s, roadMap[currentRoad])

            for i in range(1, 5):
                outbound = row['Outbound'+str(i)]
                pc = row['PC'+str(i)]
                countEmptyColumn = countEmpty(outbound, pc)
                if countEmptyColumn == 1:
                    outbound = NONE_CONSTANT
                    pc = NONE_CONSTANT

                outboundRoad = (outbound, pc)
                if outboundRoad in roadMap:
                    addOutbound(outboundDAO, roadMap[currentRoad],
                                roadMap[outboundRoad])
                else:
                    if outboundRoad in remainOutbound:
                        remainOutbound[outboundRoad].append(roadMap[currentRoad])
                    else:
                        remainOutbound[outboundRoad] = [roadMap[currentRoad]]


def migrate(db: orm.Database):
    roadSegmentDAO = createRoadSegmentDAO(db, orm)
    outboundDAO = createOutboundDAO(db, orm, roadSegmentDAO)
    datasetDAO = createDatasetDAO(db, orm, roadSegmentDAO)
    modelDAO = createModelDAO(db, orm, roadSegmentDAO)
    db.generate_mapping(create_tables=True)

    # read file and put to db
    # insert_database(roadSegmentDAO, outboundDAO)
    # t=query(roadSegmentDAO)
    # for a in t:
    #     print(a.RoadID,a.RoadSegmentID, a.To)
