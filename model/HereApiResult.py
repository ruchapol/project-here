from enum import Enum
from typing import List
from uuid import UUID
from datetime import datetime


class Ty(Enum):
    TR = "TR"


class CF_INFO:
    TY: Ty
    SP: float
    SU: float
    FF: float
    JF: float
    CN: float

    def __init__(self, ty: Ty, sp: float, su: float, ff: float, jf: float, cn: float) -> None:
        self.TY = ty
        self.SP = sp
        self.SU = su
        self.FF = ff
        self.JF = jf
        self.CN = cn


class Qd(Enum):
    EMPTY = "-"
    QD = "+"


class Tmc:
    PC: int
    DE: str
    QD: Qd
    LE: float

    def __init__(self, pc: int, de: str, qd: Qd, le: float) -> None:
        self.PC = pc
        self.DE = de
        self.QD = qd
        self.LE = le


class FiFi:
    TMC: Tmc
    CF: List[CF_INFO]

    def __init__(self, tmc: Tmc, cf: List[CF_INFO]) -> None:
        self.TMC = tmc
        self.CF = cf


class FisFi:
    FI: List[FiFi]

    def __init__(self, fi: List[FiFi]) -> None:
        self.FI = fi


class RwRw:
    FIS: List[FisFi]
    mid: UUID
    LI: str
    DE: str
    PBT: datetime

    def __init__(self, fis: List[FisFi], mid: UUID, li: str, de: str, pbt: datetime) -> None:
        self.FIS = fis
        self.mid = mid
        self.LI = li
        self.DE = de
        self.PBT = pbt


class RW:
    RW: List[RwRw]
    TY: str
    MAP_VERSION: int
    EBU_COUNTRY_CODE: int
    EXTENDED_COUNTRY_CODE: str
    TABLE_ID: int
    UNITS: str

    def __init__(self, rw: List[RwRw], ty: str, map_version: int, ebu_country_code: int, extended_country_code: str, table_id: int, units: str) -> None:
        self.RW = rw
        self.TY = ty
        self.MAP_VERSION = map_version
        self.EBU_COUNTRY_CODE = ebu_country_code
        self.EXTENDED_COUNTRY_CODE = extended_country_code
        self.TABLE_ID = table_id
        self.UNITS = units


class HereApiResult:
    RWS: List[RW]
    MAP_VERSION: str
    CREATED_TIMESTAMP: str
    VERSION: str
    UNITS: str

    def __init__(self, rws: List[RW], map_version: str, created_timestamp: str, version: str, units: str) -> None:
        self.RWS = rws
        self.MAP_VERSION = map_version
        self.CREATED_TIMESTAMP = created_timestamp
        self.VERSION = version
        self.UNITS = units
