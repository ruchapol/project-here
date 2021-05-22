from datetime import datetime
from dateutil import tz
from xml.dom import minidom
import xml.etree.ElementTree as ET
from model.featureExtraction.input import APIInput

class TfXmlPraser:
    def __init__(self):
        pass

# seave 121324

    def getTime(timeStamp):
        from_zone = tz.gettz('UTC')
        utc = datetime.strptime(timeStamp, '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=from_zone)
        to_zone = tz.gettz('Asia/Bangkok')
        thai_dt = utc.astimezone(to_zone)
        return(thai_dt)


    def parseFile(self, xml):
        tree = ET.parse(xml)
        root = tree.getroot()

        traffic_dict = {}
        for road in root[0]:
            li = road.attrib['LI']
            for node in road[0]:
                to_zone = tz.gettz('Asia/Bangkok')
                timeStamp = root.attrib['CREATED_TIMESTAMP']
                pc = node[0].attrib['PC']
                jf = node[1].attrib['JF']
                su = node[1].attrib['SU']
                confident =  node[1].attrib['CN']

                traffic_dict[(li, pc)] = {"datetime": timeStamp,
                                          "su": su,
                                          "jf": jf,
                                          "confident": confident}

        return traffic_dict

    def praseStr(self, xml_str):
        root = ET.fromstring(xml_str)
        traffic_dict = {}

        for road in root[0]:
            li = road.attrib['LI']
            for node in road[0]:
                to_zone = tz.gettz('Asia/Bangkok')
                timeStamp = root.attrib['CREATED_TIMESTAMP']
                pc = node[0].attrib['PC']
                jf = node[1].attrib['JF']
                su = node[1].attrib['SU']
                confident =  node[1].attrib['CN']
                traffic_dict[(li, pc)] = {"datetime": timeStamp,
                                          "su": su,
                                          "jf": jf,
                                          "confident": confident}

        return traffic_dict

if(__name__ == "__main__"):
    xmlPraser = TfXmlPraser()
    tf_dict = xmlPraser.parseFile(r'C:\Users\ak74b\Desktop\work\4_1\sP\python\traffic_collect\traffic_sample.txt')
    for li, pc in tf_dict:
        print(li, pc, ":", tf_dict[(li, pc)])
