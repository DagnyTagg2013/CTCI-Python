# TODO
#
# 1) COMPLEXITY: O(nlogn), best case is O(n) for sort
# - DIVIDE (1); CONQUER-RECURSE (logN) DEPTH; MERGE (N)
# - http://softwareengineering.stackexchange.com/questions/297160/why-is-mergesort-olog-n
#
# 2) OPTIMIZE to avoid excessive TEMP aux array creation-destruction
#    PRE-ALLOCATE FULL TEMP array as STACK-INPUT to TOP-LEVEL mergesort, pass-thru recurion levels AVOID excessive temp array creation
#    - mergeParts() signature changes to (origArray, TEMP, leftSTART, rightEND)
#    ATTN: SAFE way to calculate RELATIVE OFFSET for MID-point!
#    - leftEnd = leftStart + (rightEnd - leftStart)/2
#    - rightStart = leftEnd + 1
#    - size = (rightEnd - leftStart) + 1
#    - init leftStartIdx to leftStart, and go until <= leftEnd; SAME for right
#    * merge into stack-allocated temp[]
#    * FINAL copy-back temp into IN-PLACE original array; BUT from leftStart for SIZE
#
# 3) INVERSION-COUNT
#
import sys

#ATTN:  using LIST and NO NEED to import ARRAY in this case!

# STEP 1.4
# ATTN:  pass in ORIG dataList, along with Start/End Indexes!
# ALGO:
# - EXIT condition on ONE-element
# - divide into TWO, and recurse to SORT
# - call MERGE to merge TWO parts from above; which also controls InversionCount!
# RETURNS:  TUPLE(mergedResults, inversionCount)
def _recurseSort(dataList, startIdx, endIdx):

    # ATTN:  initialize inversion count
    totalInversionCount = 0

    # ATTN:  EXIT CONDITION, use >= for best coverage!
    if (startIdx >= endIdx):
        # TRICK: return ALLOCATED LIST of ONE; w TRAIL COMMA for ITERABLE!
        mergedResult = [ dataList[startIdx], ]
        # ATTN:  return orig inversion, as nothing further required!
        return (mergedResult, totalInversionCount)

    # ATTN: ITERATE state for recursive call
    midIdx = startIdx + (endIdx - startIdx)/2

    leftPart, leftInversionCount = _recurseSort(dataList, startIdx, midIdx)

    rightPart, rightInversionCount = _recurseSort(dataList, midIdx+1, endIdx)

    mergedResult, mergedInversionCount = mergeParts(leftPart, rightPart)

    # ATTN:  dividing inversionCounts for left, right; AND adding in MERGED count!
    # TODO: check OK for NOT double-counting the InversionCount, or ROLLUP @ EACH recursionLevel?
    totalInversionCount = leftInversionCount + rightInversionCount + mergedInversionCount

    return (mergedResult, totalInversionCount)


# STEP 1.3
# ALGO:  advance each side idx to MERGED result; not forgetting the TAIL case!
# ATTN:  RETURNs inversion count; but does NOT INPUT one!
# KEY:  count inversions
# - if smallest of LEFT (sorted) segment is GREATER than smallest of RIGHT (sorted) segment;
# COUNT of SWAP-INVERSIONS is REMAINING from leftIdx to len(leftPart)
# - ASSUMPTION is that each segment is SORTED at this point!
def mergeParts(leftPart, rightPart):

    mergedIdx = 0
    leftIdx = 0
    rightIdx = 0
    # TRICK:  declare inversionCount generated HERE to RETURN via TUPLE!
    inversionCount = 0

    # TRICK:  pre-allocate and init FULL amount space
    # ATTN:  Python range, stops one SHORT of RH Arg
    rightLen = len(rightPart)
    leftLen = len(leftPart)
    mergedLen = leftLen + rightLen
    mergedResult = [ -1 for x in range(0, mergedLen) ]

    # ATTN: while to check bound length of individual PARTs!
    while (     (rightIdx < rightLen)
            and (leftIdx < leftLen) ):

        # TODO:  DUNNO if this is equivalent to counting necessary SWAPs for EACH inversion instance?
        if (leftPart[leftIdx] > rightPart[rightIdx]):
            # ATTN:  OK to increment, NOT AUTO-INCREMENT!
            inversionCount += ( len(leftPart) - leftIdx )

        # ATTN:  handle CONTINUOUS case, don't forget =
        if (leftPart[leftIdx] <= rightPart[rightIdx]):
            mergedResult[mergedIdx] = leftPart[leftIdx]
            # ATTN:  no auto-incr ++ in Python!
            leftIdx += 1
        else:
            mergedResult[mergedIdx] = rightPart[rightIdx]
            rightIdx += 1

        mergedIdx = mergedIdx + 1

    # ATTN:  handle case where LEFT has leftover; conversely RIGHT
    if rightIdx == rightLen:
        # TRICK:  Python SLICing EASIER than while-loop-copy; BUT
        #         BUT while-copy-over is better for minimizing TEMP allocations!
        # mergedResult += leftPart[leftIdx:]
        while leftIdx < leftLen:
            mergedResult[mergedIdx] = leftPart[leftIdx]
            leftIdx = leftIdx + 1
            mergedIdx = mergedIdx + 1

    if leftIdx == leftLen:
        while rightIdx < rightLen:
            mergedResult[mergedIdx] = rightPart[rightIdx]
            rightIdx = rightIdx + 1
            mergedIdx = (mergedIdx + 1)

    # ATTN: return TUPLE of result and inversion count!
    return (mergedResult, inversionCount)

# ATTN:  Python PRINT Results!
def printResults(unsortedResults, sortedResults, inversionCount):

    # print '***** input numbers unsorted *****'
    # print ','.join(str(x) for x in unsortedResults)

    # ATTN: note CAST to String and '.'.join for ...
    # print '***** output numbers sorted *****'
    # print ','.join(str(x) for x in sortedResults)

    # ATTN: formatted String output
    # print '***** TOTAL inversion-swaps *****'
    print '{0:d}'.format(inversionCount)
    print '\n'

# STEP 1.2
# ATTN:  ENCAPSULATE recursive args, and START with initialized stack-state vars!
# RETURNS:  TUPLE(mergedResults, inversionCount)
def mergeSort(dataList):
    (mergedResults, inversionCount) = _recurseSort(dataList, 0, len(dataList) - 1)
    return  (mergedResults, inversionCount)

# ATTN:  main entrypoint function!
def count_inversions(dataList):

    (mergedResults, inversionCount) = mergeSort(dataList)
    return inversionCount

# STEP 1.1
def main(args):

    # TEST1:  one-element
    # print ('\n***** TEST1 *****\n')
    dataList = [1,]
    # dataList = [5, 3]
    # ATTN:  DEBUG via typing!
    # print type(dataList)
    # (sortedResults, inversionCount) = mergeSort(dataList)
    # printResults(dataList, sortedResults, inversionCount)
    inversionCount = count_inversions(dataList)
    print inversionCount

    """
        # TEST2:  even-elements
        print ('\n***** TEST2 *****\n')
        dataList = [5,3]
        (sortedResults, inversionCount) = mergeSort(dataList)
        printResults(dataList, sortedResults, inversionCount)

        # TEST3:  odd-elements
        print ('\n***** TEST3 *****\n')
        dataList = [2,4,1]
        (sortedResults, inversionCount) = mergeSort(dataList)
        printResults(dataList, sortedResults, inversionCount)
   """

    # TODO:  Dont know how to do inversion-count for handling this case; as result should be "4"
    # TEST4:  odd-elements, unsorted and repeated elements
    # print ('\n***** TEST4 *****\n')
    dataList = [2,1,3,1,2]
    (sortedResults, inversionCount) = mergeSort(dataList)
    printResults(dataList, sortedResults, inversionCount)

    """
         # TEST5:  odd-elements, sorted and repeated elements
        print ('\n***** TEST5 *****\n')
        dataList = [1,1,2,2,2]
        (sortedResults, inversionCount) = mergeSort(dataList)
        printResults(dataList, sortedResults, inversionCount)
    """

# STEP 1.0
if __name__ == "__main__":
    main(sys.argv)

"""
# ATTN:  using SKELETON Driver script with stdin to get input here!
t = int(raw_input().strip())
for a0 in xrange(t):
    n = int(raw_input().strip())
    arr = map(int, raw_input().strip().split(' '))
    print count_inversions(arr)
"""
