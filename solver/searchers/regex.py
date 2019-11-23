import re
from .searchMethods import searchMethod, allSearches
from ..exceptions import badInput
from ..matches import matchLine

class regexSearch(searchMethod):
    def findMatches(self, grid, params):
        print("attempting to find regex")
        if "useRegexSearch" in params:
            print("regex found")
            matches = []
            try:
                searchStr = params["regexSearchText"]
            except ValueError:
                raise badInput("couldn't parse regexSearchText")

            print("searching for: %s"%(searchStr,))
            if not searchStr:
                raise badInput("Requested a regex search, but didn't give a regex")

            searchRe = re.compile(searchStr)
            for name, view in grid.allViews.items():
                for index, line in enumerate(view):
                    for match in searchRe.finditer(line):
                        matches.append(matchLine(name, index, match.start(),
                                                 match.end() - match.start(), match.group()))
                        print(match)
            return grid.lineToEntry(matches)
        return []


allSearches.append(regexSearch())
