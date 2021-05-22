import untangle
# /home/ruchapol/Desktop/code/sP/round2sP/project-here/data/data.xml
# data/data.xml
def run():
    doc = untangle.parse('./data/data.xml')
    print(doc.TRAFFICML_REALTIME.RWS.children[0].FIS.children[0].TMC['DE'])
    # for child in doc.TRAFFICML_REALTIME.RWS.children:
    #     print(child['DE'])
