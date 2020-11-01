from typing import List

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
    def __init__(self, word: str, direction: str, index: int, locations: List[str]):
        self.word = word
        if direction in _directionTranslation:
            self.direction = _directionTranslation[direction]
        else:
            self.direction = direction
        # If unicode looks weird on some browsers, we should replace with images.
        self.index = index
        self.locations = locations
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.word != other.word:
            return False
        if self.direction != other.direction:
            return False
        if self.locations != other.locations:
            return False
        # Ignore index - this will be different despite being the same match
        return True


class matchLine:
    def __init__(self, viewName: str, lineIndex: int, start: int, end: int, word: str):
        self.viewName = viewName
        self.lineIndex = lineIndex
        self.start = start
        self.end = end
        self.word = word

