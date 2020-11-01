from typing import List
from . import automaton
from .searchMethods import searchMethod, allSearches
from ..matches import matchLine, matchEntry
from django.http import QueryDict
from ..grids import gridShape
from ..exceptions import badInput

class automatonSearch(searchMethod):
    def __init__(self, wordList: automaton.FileEntry):
        super().__init__("dict_" + wordList.name)
        self.wordList = wordList

    def findMatches(self, grid: gridShape, params: QueryDict) -> List[matchEntry]:
        print("Searching wordlist %s"%(self.wordList.name,))
        try:
            minLen = int(params.pop(self.requestName + "_min", 0))
            maxLen = int(params.pop(self.requestName + "_max", 0))
        except ValueError:
            raise badInput("min/max value for word list %s wasn't understood"%(self.wordList.name, ))

        A = self.wordList.getAutomaton(minLen, maxLen)
        matches: List[matchLine] = []
        for gridDir, gridView in grid.views.items():
            for lineIndex, line in enumerate(gridView):
                for endIndex, found in A.iter(line):
                    matches.append(matchLine(gridDir, lineIndex, endIndex - len(found) + 1, endIndex + 1,
                                             found))
        return grid.lineToEntry(matches)

for wordList in automaton.wordLists.values():
    allSearches.append(automatonSearch(wordList))
