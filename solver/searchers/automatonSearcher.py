from typing import List
from . import automaton
from .searchMethods import searchMethod, allSearches
from ..matches import matchLine, matchEntry
from django.http import QueryDict
from ..grids import gridShape
from ..exceptions import badInput

class automatonSearch(searchMethod):
    # parameters = [searchParameter(wlName, "any", wlParameter)]

    def findWordListMatches(self, grid, params: QueryDict, wordList: str) -> List[matchEntry]:
        print("Searching wordlist %s"%(wordList,))
        try:
            minLen = int(params.pop("dict_" + wordList + "_min", 0))
            maxLen = int(params.pop("dict_" + wordList + "_max", 0))
        except ValueError:
            raise badInput("min/max value for word list %s wasn't understood"%(wordList, ))

        A = automaton.getAutomaton(wordList, minLen, maxLen)
        matches: List[matchLine] = []
        for gridDir, gridView in grid.views.items():
            for lineIndex, line in enumerate(gridView):
                for endIndex, found in A.iter(line):
                    matches.append(matchLine(gridDir, lineIndex, endIndex - len(found) + 1, endIndex + 1,
                                             found))
        return grid.lineToEntry(matches)

    def findMatches(self, grid: gridShape, params: QueryDict) -> List[matchEntry]:
        allMatches: List[matchEntry] = []
        for wordList in automaton.wordLists:
            if "dict_" + wordList in params:
                del params["dict_" + wordList]
                allMatches.extend(self.findWordListMatches(grid, params, wordList))
        return allMatches


allSearches.append(automatonSearch())
