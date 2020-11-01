from typing import List
from django.http import QueryDict

from .grids import gridShape, allGrids
from .searchers import allSearches, postFilters
from .matches import matchLine, matchEntry
from .exceptions import badInput

def parseGridSettings(grid, responseDict: QueryDict) -> List[matchEntry]:
    thisGrid = allGrids["gridRectangle"]()
    if "gridType" in responseDict:
        try:
            thisGrid = allGrids[responseDict["gridType"]]()
        except KeyError:
            raise badInput("Invalid gridType: %s"%(responseDict["gridType"]))
    thisGrid.generateLineViews(grid)

    matchTypes: List[List[matchEntry]] = []
    for searchMethod in allSearches:
        if searchMethod.requestName in responseDict:
            matchTypes.append(searchMethod.findMatches(thisGrid, responseDict))

    if len(matchTypes) == 0:
        raise badInput("No search method selected")
    if len(matchTypes) == 1:
        matches = matchTypes[0]
    else:
        matches = [match for match in matchTypes[0] if all(match in matchTypesList for matchTypesList in matchTypes[1:])]
    if not matches:
        return []

    for filterMethod in postFilters:
        if filterMethod.requestName in responseDict:
            matches = filterMethod.filterMatches(matches, responseDict)

    return matches

