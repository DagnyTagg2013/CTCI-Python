# TODO:  state PROBLEM of suffix test SIMILARITY of number of chars with ORIG string!

import collections
import traceback
import sys

#***** FIND returns start pos
# - http://pythoncentral.io/how-to-see-if-a-string-contains-another-string-in-python/
#***** REGEX, where match() is @ START; but search() is anywhere
# - https://www.tutorialspoint.com/python/python_reg_expressions.htm
#***** LIST
# - http://www.thegeekstuff.com/2013/06/python-list/?utm_source=feedly
#***** DICTIONARY
# - https://www.tutorialspoint.com/python/python_dictionary.htm
#***** ORDERED DICTIONARY collection
# - https://pymotw.com/2/collections/ordereddict.html
#***** FLOW-CONTROL
# - http://www.tutorialspoint.com/python/python_loop_control.htm
#***** SLICE
# - http://stackoverflow.com/questions/509211/explain-pythons-slice-notation
#***** STRING
# - https://www.tutorialspoint.com/python/python_strings.htm
#***** ELIF
# - https://www.tutorialspoint.com/python/python_if_else.htm
#***** Python TRIM equivalence
# - http://stackoverflow.com/questions/761804/trimming-a-string-in-python

def calcSimilarities(testString):

    similarityMap = collections.OrderedDict()
    for startSuffix in range(0, len(testString)):
        # ATTN:  SLICING of current String, like an ARRAY to generate SUFFIX strings offset from beginning of string
        currentSuffix = testString[startSuffix:]
        # ATTN:  scan matches on characters here
        for matchIndex in range(0, len(currentSuffix)):
            if testString[matchIndex] != currentSuffix[matchIndex]:
                #ATTN:  this breaks out of ALL loop-levels for some reason
                break
        # CASE 1: FIRST CHAR MISMATCH
        # - Exit when first non-match char reached AT 0th char; set similarity to 0
        # CASE 2: PARTIAL SUFFIX MATCH
        # - Exit when first NON-MATCH char reached; set similarity to matchIndex, or 1+ last actually matching index at 1 BEFORE current matchIndex
        # CASE 3: FULL SUFFIX MATCH
        # - Exit when FULL LENGTH of suffix matched; set similarity to matchIndex + 1, for actual LENGTH of 0-indexed strings
        if (matchIndex == 0) and (testString[0] != currentSuffix[0]):
            similarityMap[currentSuffix] = 0
        elif (testString[matchIndex] != currentSuffix[matchIndex]):
            similarityMap[currentSuffix] = matchIndex
        elif (testString[matchIndex] == currentSuffix[matchIndex]):
            similarityMap[currentSuffix] = matchIndex + 1
    return similarityMap

def readInput():

    # print "==> Enter number of string Test Cases!\n"

    # ATTN:  cast to int!
    numTests = int(sys.stdin.readline())
    # print "\nINPUT NUMBER OF TESTS IS:  {0}\n".format(numTests)

    # print "==> Enter each test string; one per line:\n"
    testStrings = []
    for i in range(0, numTests):
        # NOTE:  default input type is string; so no cast; but need to cleanup!
        testStrings.append(sys.stdin.readline().strip())

    # print "\nINPUT TEST STRINGS READ ARE:  "
    # print testStrings

    return testStrings

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

# ATTN:  no main needed; run as Driver Script
try:

    # TEST CASE1: input 1, then ababaa
    # test1 = "ababaa"
    testCaseStrings = readInput()

    resultsPerTestCase = stringSimilarity(testCaseStrings)

    print resultsPerTestCase

except Exception as ex:
    traceback.print_exc(ex)


