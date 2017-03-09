
## Given 2 strings A and B, find the minimum substring in A that contains all the chars in B with best time complexity
## A: 'xCxxAxBxCxxAx', B:'CBA', answer: 'AxBxC'

# STEP 1:  QUESTIONs on PROBLEM
# - B can have repeated chars
# - B can be longer than A
# - A or B can be empty
# - NO EXACT MATCH needed; OK to CONTAIN same SET of CHARs, UNORDERED, with SAME OR GREATER frequency!

# STEP 2:
# TALKED-THRU SOLUTION (before) call stop; documenting below (after) call stop:
# - ISOLATE CORE elements that MATTER:  UNORDERED, CHARs, FREQUENCY
# *** FORGOT on CALL:
# - OK not to be EXACT map code match; can have character occurrences  GREATER OR EQUAL!
# - TARGET DRIVEs the solution; and on CONVERT to MAP of CHARs, UNORDERED, with FREQUENCY!
# *** FORGOT on CALL for more flexible-than-exact match:
# - MINIMUM match substring in test is one which MATCHES ALL chars with counts (OR GREATER) of TARGET MAP above
# - MINIMUM match substring must be of length that's sum of chars from TARGET MAP above (OR SIMPLER, the LEN of TARGET STRING)
# - take SLIDING WINDOW thru TEST string from 0; of LENGTH equal to length ABOVE to detect MIN-CANDIDATE substring
# - CONVERT MIN-CANDIDATE to MAP and test for SUPERSET of TARGET MAP -- if so, we have an EXACT (or SUPERSET) MATCH!
# *** FORGOT on CALL:
# - EXPAND SLIDING WINDOW length until MATCH found; and BREAK out at FIRST MINIMAL WINDOW LENGTH found to match!

# ATTN:  testing for KEY in DICT
# - http://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
# ATTN:  Python STRING MATCH
# - http://stackoverflow.com/questions/31228467/is-in-the-python-something-like-method-findnext-in-string
# ATTN:  Python SUBSTRING, SLICE
# - http://stackoverflow.com/questions/663171/is-there-a-way-to-substring-a-string-in-python
# ATTN:  Python GOTCHA for LENGTH of STRING!
# OTHER languages:
# s = Substr(s, beginning, LENGTH)
# So the parameters are beginning and LENGTH
# But Python's behaviour is different, it expects beginning and one after END (!). This is difficult to spot by beginners. So the correct replacement for Substr(s, beginning, LENGTH) is
# s = s[ beginning : beginning + LENGTH]

# CODING SOLUTION (after) call stop; but already did code for getMap (before) call stop:

# CORE:  reduce String to CHAR keys and OCCURRENCEs
def getCodeMap(aStr):

    codeMap = {}
    for aChar in aStr:
        currCount = codeMap.get(aChar, None)
        if (currCount == None):
            codeMap[aChar] = 1
        else:
            codeMap[aChar] += 1

    return codeMap

# ATTN TO REDUCE CORE:  need to reduce to only CORE TARGET CHARS; IGNORING other CHARs!
def getTestMapSupersetTarget(testStr, targetMap):

    coreTestMap = {}
    for aChar in testStr:
        if aChar not in targetMap:
            pass
        else:
            currCount = coreTestMap.get(aChar, None)
            if (currCount == None):
                coreTestMap[aChar] = 1
            else:
                coreTestMap[aChar] += 1

    return coreTestMap

# NOTE:  this essentially tests match on SLIDING WINDOW to detect match with LENGTH AT LEAST equal OR GREATER to SUM num chars in targetStr
def printMinimumMatchStr(testStr, targetMap, windowLen):

    foundMatch = False

    maxLenWindow = len(testStr)
    stopScanIndexPlusOne = (maxLenWindow - windowLen)
    # ATTN:  length is NON-inclusive of LAST INDEX for loop!
    for i in range(0, stopScanIndexPlusOne):
        # ATTN:  Use Python SLICE specifying one PAST END index NOT Length!
        testWindow = testStr[i:(i + windowLen)]
        # ATTN:  need to get TEST map for EACH test substring!
        # ITERATE1:  need to ELIMINATE non-Target Char elements; only accumulating frequency of Target Char elements!
        testMap = getTestMapSupersetTarget(testWindow, targetMap)
        # ITERATE2:  need to test NOT just for EQUALITY;
        # ALSO for LARGER test-case where Char counts can be GREATER OR EQUAL to TargetMap!
        if (matchAtLeastTargetMap(testMap, targetMap)):
            print testWindow
            foundMatch = True
            # ATTN:  allow to continue looping for trial of NEXT segments of SAME length!

    return foundMatch

# ITERATE 3:  need to EXPAND FROM MIN TARGET CORE WINDOW, to progressive LARGER WINDOW LENGTHS if FIRST-TRY MIN-LENGTH doesn't work!
def expandMinimumMatchStr(testStr, targetStr):

    targetMap = getCodeMap(targetStr)
    minLenMatchWindow = len(targetStr)
    maxLenMatchWindow = len(testStr)

    foundMatch = False

    # ATTN: progressively EXPAND MIN LEN window from MOST MINIMAL to larger
    for windowLen in range(minLenMatchWindow, maxLenMatchWindow):
        foundMatch = printMinimumMatchStr(testStr, targetMap, windowLen)
        # ATTN:  break out immediately if found a MIN string for SMALLEST WindowLen; as DONE!
        if foundMatch:
            # ATTN: BREAK out of LOOP EARLY on MINIMUM String found!
            return

# ITERATE 4
# - need to test NOT just for EQUALITY, but for LARGER test-case where Char counts can be GREATER OR EQUAL to TargetMap!
def matchAtLeastTargetMap(testMap, targetMap):

    isMatch = True

    # ATTN:  DRIVE by target info!
    for aChar in targetMap.keys():
        currCount = testMap.get(aChar, None)
        # TESTs if CORE TARGET Char exists in testMap
        if aChar not in testMap:
            isMatch = False
            break
        # TESTs if CORE TARGET Char exists in MINIMAL quantity from CORE TARGET Map
        elif (currCount < targetMap.get(aChar)):
            isMatch = False
            break

    return isMatch


# ======== test driver code below ========

testStr = 'xCxxAxBxCxxAx'
targetStr = 'CBA'
# ATTN:  set FAIL STR!
failStr = "BOGUS"
# expectedResult = 'AxBxC'

targetMap = getCodeMap(targetStr)
testMap = getTestMapSupersetTarget(testStr, targetMap)
# ATTN: setup FAIL case to test against!
failMap = getTestMapSupersetTarget(failStr, targetMap)

# TEST 1:  FOCUS on CORE MINIMUM EXACT MATCH CASE, DEGNERATE DATA FORCE-MATCH
# isMatch = matchAtLeastTargetMap(targetMap, targetMap)
# print isMatch

# TEST 2:  FOCUS on CORE MINIMUM EXACT MATCH CASE, with REAL DATA
# isMatch = matchAtLeastTargetMap(testMap, targetMap)
# print isMatch

# isMatch = matchAtLeastTargetMap(failMap, targetMap)
# print isMatch

# TEST 3: FOCUS NEXT on SMALLEST CASE, on SMALLEST match Window
# isFoundMatch = printMinimumMatchStr(testStr, targetMap, 3)
# print isFoundMatch

# isFoundMatch = printMinimumMatchStr(testStr, targetMap, 6)
# SHOULD BE TRUE!
# print isFoundMatch

# TODO:
# BUG - xAxBxC PASSEs along with AxBxC
#     - need to eliminate LONGER string with SAME reduced mapCode!

# TEST 4:  EXPAND to MORE INEXACT SUPERSET MATCH CASE
expandMinimumMatchStr(testStr, targetStr)

# TODO:
# TEST 5: CHECK FOR DEGENERATE or EXCEPTION CASES
# - EMPTY LIST
# - B LONGER than A



