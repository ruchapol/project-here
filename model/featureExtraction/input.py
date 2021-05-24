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

    def speedUncut(self,su: float) -> APIInput:
        self.SpeedUncut = su
        return self
        
    def jamFactor(self,jf: float) -> APIInput:
        self.JamFactor = jf
        return self
