
import collections
import traceback
import sys

def calcSimilarities(testString):

    similarityMap = collections.OrderedDict()
    for startSuffix in range(0, len(testString)):
        # ATTN:  SLICING of current String, like an ARRAY
        currentSuffix = testString[startSuffix:]
        for matchIndex in range(0, len(currentSuffix)):
            if testString[matchIndex] != currentSuffix[matchIndex]:
                #ATTN:  this breaks out of ALL loop-levels for some reason
                break
        # CASE 1: FIRST CHAR MISMATCH
        # - Exit when first non-match char reached at 0th char; set similarity to 0
        # CASE 2: PARTIAL SUFFIX MATCH
        # - Exit when first NON-MATCH char reached; set similarity to matchIndex,
        # or 1+ for 0-based last actually matching index on prior char at currIdx - 1
        # CASE 3: FULL SUFFIX MATCH
        # - Exit when FULL LENGTH of suffix matched; set similarity to matchIndex + 1, for actual LENGTH of 0-indexed strings
        if (matchIndex == 0) and (testString[0] != currentSuffix[0]):
            similarityMap[currentSuffix] = 0
        elif (testString[matchIndex] != currentSuffix[matchIndex]):
            similarityMap[currentSuffix] = matchIndex
        elif (testString[matchIndex] == currentSuffix[matchIndex]):
            similarityMap[currentSuffix] = matchIndex + 1
    return similarityMap

def  stringSimilarity(testCaseStrings):

     totalSimilarityPerTestCase = []
     for testNum in range(0, len(testCaseStrings)):
        # ATTN: ITERATE from SINGLE-INPUT CASE prior to adding DRIVING OUTER-LOOP
        similarityMap = calcSimilarities(testCaseStrings[testNum])

        # print "\n==> TEST CASE {0} for {1}:\n".format(testNum, testCaseStrings[testNum])
        # for suffix, similarity in similarityMap.items():
            # print "{0}:{1}".format(suffix, similarity)
            # ATTN:  sum values in dictionary

        totalSimilarityPerTestCase.append(sum(similarityMap.values()))

     return totalSimilarityPerTestCase