from defaultlist import defaultlist

from . import automaton

# This produces a list of rotations of the grid, called views
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

# The class for passing through to display.html to contain the information
#  required for displaying the results
class matchEntry:
    def __init__(self, word, direction, index, locations):
        self.word = word
        self.direction = direction
        self.index = index
        self.locations = locations

# This converts from a list of found words, back to the indexes in the original grid
# Matches = [
#  0: Name of view the match was found in, (if it ends with a -, it counds it as a backwards match in the original view)
#  1: Line in the view that the match was found,
#  2: First letter of the match
#  3: Last letter of the match
# ]
# Returns a list of matchEntry classes for displaying
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

# Takes a dictionary of views of the grid, and matches each line against the automaton
# Returns a list of matchEntry objects for display
def findWordsFromAutomaton(gridViews, A):
    matches = []
    for dir, gridView in gridViews.items():
        for lineIndex, line in enumerate(gridView):
            for endIndex, found in A.iter(line):
                matches.append((dir, lineIndex, endIndex - len(found) + 1, endIndex + 1, found))
    return getIndexes(gridViews, matches)

# Primary entry point into this file.  Returns a list of matchEntry objects containing all matches
def getGridMatches(grid, method="wordlist"):
    gridViews = genViews(grid)
    if method == "wordlist":
        Aut = automaton.getAutomaton(minLength=3)
        return findWordsFromAutomaton(gridViews, Aut)


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


