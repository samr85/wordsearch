
_directionTranslation = {
    'h':   '→',
    'h-':  '←',
    'v':   '↓',
    'v-':  '↑',
    'dr':  '↘',
    'dr-': '↖',
    'dl':  '↙',
    'dl-': '↗'
    }


# The class for passing through to display.html to contain the information
#  required for displaying the results
class matchEntry:
    def __init__(self, word, direction, index, locations):
        self.word = word
        if direction in _directionTranslation:
            self.direction = _directionTranslation[direction]
        else:
            self.direction = direction
        # If unicode looks weird on some browsers, we should replace with images.
        self.index = index
        self.locations = locations


class matchLine:
    def __init__(self, viewName: str, lineIndex: int, start: int, end: int, word: str):
        self.viewName = viewName
        self.lineIndex = lineIndex
        self.start = start
        self.end = end
        self.word = word

