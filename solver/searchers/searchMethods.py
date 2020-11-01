from typing import List
from django.http import QueryDict

from ..grids import gridShape
from ..matches import matchEntry

class _inputMethod:
    """ Base class for search and filters, don't use directly """
    def __init__(self, requestName: str):
        """requestName: The key added to the user request by selecting this search method in input.html"""
        self.name = self.__class__.__name__
        self.requestName = requestName

class searchMethod(_inputMethod):
    """ This class is for searching each line and diagonal on the grid and returning a list of found 
          words and their locations.
        Create an instance of this class and add it to the allSearches list.
        Overload the findMatches function to do the actual search.
    """
    def findMatches(self, grid: gridShape, params: QueryDict) -> List[matchEntry]:
        raise NotImplementedError

class filterMethod(_inputMethod):
    """ This class is for applying a filter to the words already found by the other search methods.

        Create an instance of this class and add it to the postFilters list.
        Overload filterMatches function to return which of the matches pass the filter.
    """
    def filterMatches(self, matches: List[matchEntry], params: QueryDict) -> List[matchEntry]:
        raise NotImplementedError

allSearches: List[searchMethod] = []
postFilters: List[filterMethod] = []