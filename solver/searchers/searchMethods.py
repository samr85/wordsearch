from typing import List
from django.http import QueryDict

from ..grids import gridShape
from ..matches import matchEntry

class searchMethod:

    def __init__(self):
        self.name = self.__class__.__name__

    def findMatches(self, grid: gridShape, params: QueryDict) -> List[matchEntry]:
        raise NotImplementedError


allSearches: List[searchMethod] = []
