class RoadSegment:
    RowID: int
    RoadID: str
    RoadSegmentID: str
    RoadDescription: str
    RoadSegmentDescription: str
    LatLong: str


class Outbound:
    RoadSegmentID: int # point to RowID
    OutboundSegmentID: int # point to RowID

