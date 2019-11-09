import os
import re
import pickle
import time

import ahocorasick

fileExt = ".automaton"
thisDir = os.path.dirname(os.path.abspath(__file__))
cacheDir = os.path.join(thisDir, "cache")
os.makedirs(cacheDir, exist_ok=True)

def getCache(filename):
    return os.path.join(cacheDir, filename+fileExt)

def readWordlist(wordListFile="words.txt"):
    with open(os.path.join(thisDir, wordListFile)) as f:
        wordListOrig = list(f)
    wordList = [re.sub('[^a-zA-Z]', '', x).lower() for x in wordListOrig]
    wordList = set(wordList) #dedupe
    wordList = [x for x in wordList if len(x) > 2]

    print("Found %d entries"%(len(wordList)))
    return wordList

def makeAutomaton(wordListFile):
    wordList = readWordlist(wordListFile)

    start = time.time()
    A = ahocorasick.Automaton()
    for word in wordList:
        A.add_word(word, word)
    A.make_automaton()
    print("ahocorasick automation took: %.8f seconds to build"%(time.time() - start))
   
    with open(getCache(wordListFile), "wb") as f:
        pickle.dump(A, f)
    return A

def getAutomaton(wordListFile="words.txt"):
    filename = getCache(wordListFile)
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    else:
        return makeAutomaton(wordListFile)

__all__ = ["getAutomaton"]
