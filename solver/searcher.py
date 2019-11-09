from defaultlist import defaultlist
import code
import time
import re
import pickle

from . import automaton

Aut = automaton.getAutomaton()

def genViews(grid):
    arr = {}
    viewH = [''.join(x) for x in grid]
    arr['h'] = viewH
    arr['h-'] = [x[::-1] for x in viewH]

    #print(viewH)
    viewV = [''.join(x) for x in zip(*viewH)]
    arr['v'] = viewV
    arr['v-'] = [x[::-1] for x in viewV]

    #print(viewV)
    viewDR = defaultlist(str)
    viewDL = defaultlist(str)

    height = len(viewH)
    width = len(viewV)
    for i in range(height):
        first = height - i - 1
        for j in range(width):
            viewDR[first + j] += viewH[i][j]
            viewDL[i+j] += viewH[i][j]

    #print(viewDR)
    #print(viewDL)
    arr['dr'] = viewDR
    arr['dr-'] = [x[::-1] for x in viewDR]
    arr['dl'] = viewDL
    arr['dl-'] = [x[::-1] for x in viewDL]
    return arr

class matchEntry:
    def __init__(self, word, direction, index, locations):
        self.word = word
        self.direction = direction
        self.index = index
        self.locations = locations

def getIndexes(gridViews, matches):
    indexes=[]
    gridWidth = len(gridViews["h"][0])
    gridHeight = len(gridViews["v"][0])
    for index, match in enumerate(matches):
        match = list(match)
        rev = False
        name = match[0]
        if name[-1] == "-":
            # reverse match
            lineLen = len(gridViews[name][match[1]])
            match3 = lineLen - match[2]
            match[2] = lineLen - match[3]
            match[3] = match3
            rev = True

        if name.startswith("h"):
            locations = ["%d_%d"%(v, match[1]) for v in range(match[2], match[3])]
            indexes.append(matchEntry(match[4], name, index, locations))
            #print("%s: %s: %s"%(name, match[4], locations))
        elif name.startswith("v"):
            locations = ["%d_%d"%(match[1], h) for h in range(match[2], match[3])]
            indexes.append(matchEntry(match[4], name, index, locations))
            #print("%s: %s: %s"%(name, match[4], locations))
        elif name.startswith("dr"):
            offset = match[1] - gridHeight + 1 # line index - height
            if offset < 0:
                offsetX = 0
                offsetY = -offset
            else:
                offsetX = offset
                offsetY = 0
            locations = ["%d_%d"%(h + offsetX, h + offsetY) for h in range(match[2], match[3])]
            indexes.append(matchEntry(match[4], name, index, locations))
            #print("%s: %s: %s"%(name, match[4], locations))
        elif name.startswith("dl"):
            if (match[1] < gridWidth):
                offsetX = match[1]
                offsetY = 0
            else:
                offsetX = gridWidth
                offsetY = match[1] - gridWidth
            locations = ["%d_%d"%(-h + offsetX, h + offsetY) for h in range(match[2], match[3])]
            indexes.append(matchEntry(match[4], name, index, locations))
            #print("%s: %s: %s"%(name, match[4], locations))
        else:
            indexes.append(matchEntry(match[4], name, index, []))
            print("%s: %s: %s"%(name, match[4], "Can't calculate"))
    return sorted(indexes, key=lambda x: (-len(x.word), x.word))

def findWordsFromAutomaton(gridViews, A):
    matches = []
    for dir, gridView in gridViews.items():
        for lineIndex, line in enumerate(gridView):
            for endIndex, found in A.iter(line):
                matches.append((dir, lineIndex, endIndex - len(found) + 1, endIndex + 1, found))
    return getIndexes(gridViews, matches)

def getGridMatches(grid, method="wordlist"):
    gridViews = genViews(grid)
    if method == "wordlist":
        return findWordsFromAutomaton(gridViews, Aut)

if __name__ == "__main__":
    arrayIn = ["hello1",
               "eeeee1",
               'lllll1',
               'lllll1',
               'ooooo1']

    arrays = genArrays(arrayIn)


    #code.interact(local=locals())

    ret = []
    start = time.time()
    for _ in range(100):
        findWordsFromAutomaton(arrays, Aut)
    print("ahocorasick: %.8f seconds"%(time.time() - start))
    print(ret)


