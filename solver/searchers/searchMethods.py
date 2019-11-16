from typing import List, ClassVar, Dict, Optional
import enum

from ..grids import gridShape
from ..matches import matchEntry


class subType(enum.Enum):
    any = "any"
    single = "single"
    drop = "drop"
    text = "text"
    none = "none"

class searchParameter:
    def __init__(self, name: str, subParmType: subType,
                 subParameters: Optional[List['searchParameter']] = None,
                 dropOptions: Optional[List[str]] = None):
        self.name = name
        self.subParmType = subParmType
        self.subParameters = subParameters
        self.dropOptions = dropOptions
        if subParmType == subType.any or subParmType == subType.single:
            if not subParameters:
                raise ValueError("Requested any or single, but gave no options for it!")
        elif subParmType == "drop":
            if not self.dropOptions:
                raise ValueError("Requested a drop down list with no entries!")

class searchMethod:
    parameters: ClassVar[List[searchParameter]] = []

    def __init__(self):
        self.name = self.__class__.__name__

    def findMatches(self, grid: gridShape, params: Dict[str, Dict]) -> List[matchEntry]:
        raise NotImplementedError


allSearches: Dict[str, searchMethod] = {}
