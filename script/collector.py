import requests
import json
import os
from model.HereApiResult import HereApiResult
from collections import namedtuple
from script.xml_read import TfXmlPraser
from typing import List


jsonPATH = [".","data","data.json"]
xmlPATH = [".","data","data.xml"]

def writeFileJSON():
    parameters = {"app_id": "wwcWhGYZ5l7CgKOMisYT", "app_code": "IdjdLPBAG-tfDKm2J35YxA",
                "bbox": "13.828159,100.513832;13.818719,100.528063"}
    response = requests.get("http://traffic.cit.api.here.com/traffic/6.3/flow.json", params=parameters)
    data = response.content.decode('utf-8')
    # Parse JSON into an object with attributes corresponding to dict keys.
    print(data)
    with open('data.json', 'w', encoding='utf-8') as f_out:
        f_out.write(data)

def decoder(hereApiDict):
    return namedtuple('Wow', hereApiDict.keys())(*hereApiDict.values())

def getPath(arrayPath: List[str]):
    return os.path.join(*arrayPath) # spread array

def runJSON():
    x: HereApiResult = None
    y: HereApiResult = None
    with open(getPath(jsonPATH), 'r', encoding='utf-8') as f:
        x = json.loads(f.read(), object_hook=decoder)
    with open('./data/data1.json', 'r', encoding='utf-8') as f:
        y = json.loads(f.read(), object_hook=decoder)
    print(x.RWS[0].RW[0].FIS[0].FI[0].TMC.DE)
    print(y.RWS[0].RW[0].FIS[0].FI[0].CF[0].CN)


def runXML():
    xmlPraser = TfXmlPraser()
    tf_dict = xmlPraser.parseFile(getPath(xmlPATH))
    for li, pc in tf_dict:
        print(li, pc, ":", tf_dict[(li, pc)])
