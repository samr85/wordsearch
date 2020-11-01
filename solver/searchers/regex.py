import typing
from typing import List

import django

import regex
from .searchMethods import searchMethod, filterMethod, allSearches, postFilters, QueryDict, gridShape
from ..exceptions import badInput
from ..matches import matchLine, matchEntry

def _getRegex(paramName: str, params: QueryDict) -> typing.Pattern:
    try:
        regexString = params[paramName]
    except django.utils.datastructures.MultiValueDictKeyError:
        raise badInput("couldn't parse %s"%(paramName))
    if not regexString:
        raise badInput("Requested a regex, but didn't give a match string")
    print("Using regex: %s", regexString)
    return regex.compile(regexString)

class regexSearch(searchMethod):
    def findMatches(self, grid: gridShape, params: QueryDict) -> List[matchEntry]:
        print("attempting to find regex")
        matches = []
        searchRe = _getRegex("regexSearchText", params)

        for name, view in grid.allViews.items():
            for index, line in enumerate(view):
                # Typing isn't quite right here - using the regex module, not re, so this next line is fine
                for match in searchRe.finditer(line, overlapped=True): # type: ignore
                    matches.append(matchLine(name, index, match.start(),
                                                match.end(), match.group()))
                    print(match)
        return grid.lineToEntry(matches)

class regexFilter(filterMethod):
    def filterMatches(self, matches: List[matchEntry], params: QueryDict) -> List[matchEntry]:
        matchRe = _getRegex("regexFilterText", params)
        retMatches: List[matchEntry] = []
        for match in matches:
            if matchRe.match(match.word):
                retMatches.append(match)
        return retMatches
            

allSearches.append(regexSearch("useRegexSearch"))
postFilters.append(regexFilter("useRegexFilter"))
