from typing import List

from .grids import gridShape, allGrids
from .searchers import allSearches
from .matches import matchLine, matchEntry


# Primary entry point into this file.  Returns a list of matchEntry objects containing all matches
# TODO: Needs lots of error checking!!
def getGridMatches(grid, gridType="gridRectangle", method="wordList") -> List[matchEntry]:
    if gridType in allGrids:
        thisGrid = allGrids[gridType]
    thisGrid = allGrids[gridType]()
    thisGrid.generateLineViews(grid)
    print("Requesting method: %s"%(method))
    if method in allSearches:
        return allSearches[method].findMatches(thisGrid, {"words": {}})
    else:
        print("Requested unknown method! %s"%(method))
        print(allSearches)


# Can call this on the command line to test things without using the GUI, this is the entry point if you do that
if __name__ == "__main__":
    arrayIn = ["hello1",
               "eeeee1",
               'lllll1',
               'lllll1',
               'ooooo1']

    arrays = genViews(arrayIn)

    #import code
    #code.interact(local=locals())

    import time
    ret = []
    start = time.time()
    Aut = automaton.getAutomaton(minLength=3)
    for _ in range(100):
        findWordsFromAutomaton(arrays, Aut)
    print("ahocorasick: %.8f seconds"%(time.time() - start))
    print(ret)


