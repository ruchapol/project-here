from __future__ import annotations
from datetime import datetime 

# 219+57424 57431 : {'datetime': '2021-05-09T05:56:31Z', 'su': '80.83', 'jf': '0.0', 'confident': '0.81'}
class APIInput:
    RoadID: str
    SegmentID: str
    DateTime: str
    SpeedUncut: float
    JamFactor: float
    Confident: float

    def setSpeedUncut(self,su: float) -> APIInput:
        self.SpeedUncut = su
        return self
        
    def setJamFactor(self,jf: float) -> APIInput:
        self.JamFactor = jf
        return self

    def setDateTime(self, time: str) -> APIInput:
        self.DateTime = time
        return self

    def _praseRFCtimeToDatetime(self, dateStr: str) -> datetime:
        # dateStr = "21 June, 2018"
        # 2021-05-09T05:56:31Z
        # %Y-%d-%mT%H:%M:%SZ
        date_object = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
        return date_object

    def getDay(self) -> int:
        return self._praseRFCtimeToDatetime(self.DateTime).day

    def getDayOfWeek(self) -> int:
        return self._praseRFCtimeToDatetime(self.DateTime).weekday()

    def getHour(self) -> int:
        return self._praseRFCtimeToDatetime(self.DateTime).hour

    def getMinute(self) -> int:
        return self._praseRFCtimeToDatetime(self.DateTime).minute