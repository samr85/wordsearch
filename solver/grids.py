from typing import List, Dict, Type
from defaultlist import defaultlist

from .matches import matchEntry, matchLine

class gridShape:
    def __init__(self, requestViews=None):
        self.name = self.__class__.__name__
        self.requestViews = requestViews
        self.views: Dict[str, List] = {}
        self.allViews: Dict[str, List] = {}

    # This produces a list of rotations of the grid, called views
    def generateLineViews(self, grid):
        allViews = {}
        viewH = [''.join(x) for x in grid]
        allViews['h'] = viewH
        allViews['h-'] = [x[::-1] for x in viewH]

        # print(viewH)
        viewV = [''.join(x) for x in zip(*viewH)]
        allViews['v'] = viewV
        allViews['v-'] = [x[::-1] for x in viewV]

        # print(viewV)
        viewDR = defaultlist(str)
        viewDL = defaultlist(str)

        height = len(viewH)
        width = len(viewV)
        for i in range(height):
            first = height - i - 1
            for j in range(width):
                viewDR[first + j] += viewH[i][j]
                viewDL[i + j] += viewH[i][j]

        # print(viewDR)
        # print(viewDL)
        allViews['dr'] = viewDR
        allViews['dr-'] = [x[::-1] for x in viewDR]
        allViews['dl'] = viewDL
        allViews['dl-'] = [x[::-1] for x in viewDL]

        self.allViews = allViews
        if self.requestViews:
            self.views = {key: allViews[key] for key in self.requestViews}
        else:
            self.views = allViews

    def lineToEntry(self, matches: List[matchLine]) -> List[matchEntry]:
        # This converts from a list of found words, back to the indexes in the original grid

        indexes = []
        gridWidth = len(self.allViews["h"][0])
        gridHeight = len(self.allViews["v"][0])
        for index, match in enumerate(matches):
            rev = False
            name = match.viewName
            if name[-1] == "-":
                # reverse match
                lineLen = len(self.views[name][match.lineIndex])
                newEnd = lineLen - match.start
                match.start = lineLen - match.end
                match.end = newEnd
                rev = True

            if name.startswith("h"):
                locations = ["%d_%d" % (v, match.lineIndex) for v in range(match.start, match.end)]
                indexes.append(matchEntry(match.word, name, index, locations))
                # print("%s: %s: %s"%(name, match.word, locations))
            elif name.startswith("v"):
                locations = ["%d_%d" % (match.lineIndex, h) for h in range(match.start, match.end)]
                indexes.append(matchEntry(match.word, name, index, locations))
                # print("%s: %s: %s"%(name, match.word, locations))
            elif name.startswith("dr"):
                offset = match.lineIndex - gridHeight + 1  # line index - height
                if offset < 0:
                    offsetX = 0
                    offsetY = -offset
                else:
                    offsetX = offset
                    offsetY = 0
                locations = ["%d_%d" % (h + offsetX, h + offsetY) for h in range(match.start, match.end)]
                indexes.append(matchEntry(match.word, name, index, locations))
                # print("%s: %s: %s"%(name, match.word, locations))
            elif name.startswith("dl"):
                if match.lineIndex < gridWidth:
                    offsetX = match.lineIndex
                    offsetY = 0
                else:
                    offsetX = gridWidth
                    offsetY = match.lineIndex - gridWidth
                locations = ["%d_%d" % (-h + offsetX, h + offsetY) for h in range(match.start, match.end)]
                indexes.append(matchEntry(match.word, name, index, locations))
                # print("%s: %s: %s"%(name, match.word, locations))
            else:
                indexes.append(matchEntry(match.word, name, index, []))
                print("%s: %s: %s" % (name, match.word, "Can't calculate"))
        return sorted(indexes, key=lambda x: (-len(x.word), x.word))

class gridRectangle(gridShape):
    pass

class gridOffset(gridShape):
    def __init__(self):
        super().__init__(["h", "h-", "v", "v-", "dr", "dr-"])


_allGrids = [gridRectangle, gridOffset]
allGrids: Dict[str, Type[gridShape]] = {}
for _grid in _allGrids:
    allGrids[_grid.__name__] = _grid
