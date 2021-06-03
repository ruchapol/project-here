from datetime import datetime

def parseRFCtimeToDatetime(dateStr: str) -> datetime:
        # 2021-05-09T05:56:31Z
        date_object = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
        return date_object