import untangle
# /home/ruchapol/Desktop/code/sP/round2sP/project-here/data/data.xml
# data/data.xml
doc = untangle.parse('/home/ruchapol/Desktop/code/sP/round2sP/project-here/data/data.xml')
print(doc.TRAFFICML_REALTIME.RWS)#.FIS[0].TMC['DE'])
for child in doc.TRAFFICML_REALTIME.RWS:
    print(child['DE'])
