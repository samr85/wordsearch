import os
import re
import pickle
import time

import ahocorasick

fileExt = ".automaton"
thisDir = os.path.dirname(os.path.abspath(__file__))
cacheDir = os.path.join(thisDir, "cache")
os.makedirs(cacheDir, exist_ok=True)
loadedAutomaton = {}

def getCache(filename, minLength):
    return os.path.join(cacheDir, filename+".%d"%(minLength)+fileExt)

def readWordlist(wordListFile):
    with open(os.path.join(thisDir, wordListFile)) as f:
        wordListOrig = list(f)
    # Remove any non a-z character, and make lowercase
    wordList = [re.sub('[^a-zA-Z]', '', x).lower() for x in wordListOrig]
    return set(wordList) # dedupe

def makeAutomaton(wordListFile, minLength):
    wordList = readWordlist(wordListFile)
    wordList = [x for x in wordList if len(x) >= minLength] #filter on length
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
def getAutomaton(wordListFile="words.txt", minLength=3):
    filename = getCache(wordListFile, minLength)
    if filename in loadedAutomaton:
        return loadedAutomaton[filename]
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    else:
        return makeAutomaton(wordListFile, minLength)

__all__ = ["getAutomaton"]
