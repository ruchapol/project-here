import os
from typing import List

def getPath(arrayPath: List[str]):
    return os.path.join(*arrayPath) # spread array
