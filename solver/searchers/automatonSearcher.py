from . import automaton
from .searchMethods import searchMethod, searchParameter, subType, allSearches
from ..matches import matchLine

wlName = "wordList"
wlCustom = "custom"
wlMin = "minLength"
wlMax = "maxLength"
limitSizeParm = [searchParameter(wlMin, subType.drop, dropOptions=["2", "3", "4", "5", "6"]),
                 searchParameter(wlMax, subType.drop, dropOptions=["5", "6", "7", "8", "9"])]

wlParameter = [searchParameter(wordFile, subType.any, limitSizeParm) for wordFile in automaton.wordLists]
wlParameter.append(searchParameter(wlCustom, subType.text))


class automatonSearch(searchMethod):
    parameters = [searchParameter(wlName, "any", wlParameter)]

    def findMatches(self, grid, params):
        print("Requested automaton matching")
        for wlEntry, wlOptions in params.items():
            if wlEntry == wlCustom:
                print("Not yet implemented custom list parsing")
            else:
                if wlEntry not in automaton.wordLists:
                    print("ERROR: requested an invalid word list!!")
                    return
                else:
                    print("Requested word list: %s"%(wlEntry,))
                    A = automaton.getAutomaton(wlEntry, wlOptions[wlMin] if wlMin in wlOptions else 0,
                                               wlOptions[wlMax] if wlMax in wlOptions else 0)
                    matches = []
                    for gridDir, gridView in grid.views.items():
                        for lineIndex, line in enumerate(gridView):
                            for endIndex, found in A.iter(line):
                                matches.append(matchLine(gridDir, lineIndex, endIndex - len(found) + 1, endIndex + 1,
                                                         found))
                    return grid.lineToEntry(matches)


allSearches[wlName] = automatonSearch()
