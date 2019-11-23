from typing import List, Dict, NamedTuple
import os
import re
import pickle
import time

import ahocorasick

fileExt = ".automaton"
wordListsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordLists")
cacheDir = os.path.join(wordListsDir, "cache")
os.makedirs(cacheDir, exist_ok=True)
loadedAutomaton = {}

def getCache(filename, minLength):
    return os.path.join(cacheDir, filename + ".%d"%(minLength,) + fileExt)

def readWordList(wordListFile):
    with open(os.path.join(wordListsDir, wordListFile) + ".txt") as f:
        wordListOrig = list(f)
    # Remove any non a-z character, and make lowercase
    wordList = [re.sub('[^a-zA-Z]', '', x).lower() for x in wordListOrig]
    return set(wordList)  # dedupe

def makeAutomaton(wordListFile, minLength):
    wordList = readWordList(wordListFile)
    wordList = [x for x in wordList if len(x) >= minLength]  # filter on length
    print("Found %d entries"%(len(wordList)))

    start = time.time()
    A = ahocorasick.Automaton()
    for word in wordList:
        A.add_word(word, word)
    A.make_automaton()
    print("ahocorasick automation took: %.8f seconds to build"%(time.time() - start))

    filename = getCache(wordListFile, minLength)
    with open(filename, "wb") as f:
        pickle.dump(A, f)
    loadedAutomaton[filename] = A
    return A

# Loads the cached version of the automaton for this file and length,
#  or creates a new one if it's not yet cached
def getAutomaton(wordListFile="words", minLength=0, maxLength=0):
    if not minLength:
        minLength = 3
    filename = getCache(wordListFile, minLength)
    if filename in loadedAutomaton:
        return loadedAutomaton[filename]
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    else:
        return makeAutomaton(wordListFile, minLength)

class FileEntry(NamedTuple):
    name: str
    wordCount: int

def findWordLists() -> Dict[str, FileEntry]:
    allFiles: List[str] = os.listdir(wordListsDir)
    retList = {}
    for file in allFiles:
        if file.endswith(".txt"):
            with open(os.path.join(wordListsDir, file), "rb") as f:
                entryLen = len(f.readlines())
            retList[file[:-4]] = FileEntry(file[:-4], entryLen)
        
    return retList


wordLists = findWordLists()

__all__ = ["getAutomaton", "wordLists"]
