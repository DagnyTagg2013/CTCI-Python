
# ATTN:
# - QUICKSELECT or QUICKSORT in Python
# https://en.wikipedia.org/wiki/Quickselect
# - QUICKSORT details
# http://quiz.geeksforgeeks.org/quick-sort/
# - SWAPs in Python
# http://stackoverflow.com/questions/2493920/how-to-switch-position-of-two-items-in-a-python-list
#

# ALGO:
#
# COMPLEXITY:  O(NlogN) with logN recursive depth
# PARTITION (partition divider element, all less to left, all right to right, UNORDERED)
# - choose FIRST element as PIVOT
# - PIVOT | LEFT < PIVOT => | ... | <= RIGHT > PIVOT
# * start while section to process until SWAP needed:
# - scan LEFT start to RIGHT for all values LESS than pivot; STOP when found value GREATER than PIVOT
# - scan RIGHT start to LEFT for all values GREATER than pivot; STOP when found value LESS than PIVOT
# - detect FINISH Partition condition when RIGHT < LEFT
# - at THIS point; SWAP values between LEFT and RIGHT
# - RETURN RIGHT as SPLIT-BOUNDARY point or START of RIGHT partition
#
# RECURSE SORT:
# - Partition to return SPLIT point (or FIRST element of HIGHER part
# - Quicksort on LEFT LOWER part below SPLIT point
# - Quicksort on RIGHT HIGHER part above SPLIT point
#
# QUICK SELECT kth element:
# -> get the PIVOT index
# - if k == PIVOT index; DONE
# - if k < PIVOT index;
# * RECURSE on LEFT,
# - OTHERWISE
# - RECURSE on RIGHT of PIVOT index
# * DECONSTRUCT to FOR LOOP;
#   - if k == PIVOT index; DONE
#   - PARTITION
#   - MODIFYING LEFT, or RIGHT at end of each iteration

# ATTN
# - support for Python Exception stacktrace
# import traceback
import logging


# ATTN:  create PUBLIC version without TRACKING-STACK-PARAMS
def quicksort(data):

    rquicksort(data, 0, len(data) - 1, 0)

# ATTN:  create PRIVATE, RECURSIVE version!
# ATTN:  call PARTITION FIRST! which returns PARTITION IDX,
#        then quicksort on each half!
# ATTN:  use first, last indices!
# ATTN:  in-place modification of input data list
def rquicksort(data, firstIdx, lastIdx, level):

    print "=====>INSIDE Recursive QSORT at LEVEL:  {0}".format(level)

    # ATTN:  FIRST TEST EXIT condition to do-nothing, and also check BOUNDARY cases!
    if (firstIdx <= lastIdx) and (firstIdx >= 0) and (lastIdx < len(data)):

        # ATTN:  at this point, pivot value is in FINAL POSITION @ pivotIdx!
        pivotIdx = partition(data, firstIdx, lastIdx)
        # ATTN:  CAN select pivotIdx, or ASSUME its always the 0th element?
        # TODO:  RANDOMIZE selection of index, but for now, ASSUME FIRST element!
        # TODO:  the following partitioner SHOULD work, but doesnt!
        pivotIdx = rCleanerPartition(data, firstIdx, lastIdx, firstIdx)

        # ATTN: increment LEVEL PRIOR to recursive calls!
        level += 1

        print "\n---CALL R QUICK LOW with {0}:{1}".format(firstIdx, (pivotIdx - 1))
        # checking pivotIdx > 0, otherwise NON-EXISTING LOWER SEGMENT. so no need to subdivide, and can abort!
        if (pivotIdx >= 1):
            rquicksort(data, firstIdx, (pivotIdx - 1), level)

        # upper half
        print "\n---CALL R QUICK HIGH with {0}:{1}".format((pivotIdx + 1), lastIdx)
        rquicksort(data, pivotIdx + 1, lastIdx, level)

        # ATTN; in-place modification needs no return value
        print "\nreturn R SORT Level {0}".format(level)

    else:
        print "\nEXIT on boundary indices reached!"


#ATTN:  should be STEP1!
#ATTN:  - assume FIRST element is pivot value
#       - test <= and >= against VALUE AND Indexes starting from both ENDs
#       - remember to SKIP past first pivotElement on left side, then move in OPPOSITE directions
#       - TEST DONE at CROSS < condition; OR SWAP otherwise
#       - OUTER while on Done enclosing each sub-scan loop to advance Left and Right independently until swap condition detected!
#       - SWAP first into RIGHT idx for PIVOT value-divider!
#       - RETURN pivotIdx
def partition(data, firstIdx, lastIdx):

    # INIT
    # - assume partitionValue is @ FIRST element
    # - set lowerScan to leftIdx, upperScan to rightIdx
    # - have OUTER loop which tracks DONE condition
    pivotValue = data[firstIdx]

    doneSwap = False
    lowerScan = firstIdx + 1  # ATTN:  this SKIPs first pivot value!
    upperScan = lastIdx

    while not doneSwap:

        # ATTN:  use <= and >= for FULL COVERAGE, and no need to SWAP on equals!
        # ATTN:  check for scan RELATIVE to pivotValue!
        # scans until swap condition found
        while (lowerScan <= upperScan) and (data[lowerScan] <= pivotValue):
            lowerScan += 1

        # scans until swap condition found
        while (upperScan >= lowerScan) and (data[upperScan] >= pivotValue):
            upperScan -= 1

        # test if swap
        # ATTN:  DO PYTHON SWAP or EXIT when Scans CROSS
        #        check with INEQUALITY!
        if (lowerScan <= upperScan):
            data[lowerScan], data[upperScan] = data[upperScan], data[lowerScan]
        else:
            doneSwap = True
            pivotIdx = upperScan

    # ATTN:  swap first element into correct Pivot at upperScan!
    data[firstIdx], data[pivotIdx] = data[pivotIdx], data[firstIdx]

    return pivotIdx

# ALGO:  much MORE elegant, as just using ONE while loop!
# - elements to < LEFT of partIndex are < PIVOT VALUE;
# - elements to >= RIGHT of partIndex are >= PIVOT VALUE
# => SCAN index for NEW data starts one AHEAD of partIndex initialized to -1;
# - partIdx points to FIRST or LEFTMOST element of GREATER segment
# - if new item GREATER than PIVOT VALUE; don't move partIdx, just advance new data SCAN; thus just growing HIGHER segment
# - if new item SMALLER, SWAP new data with  and also advance SCAN, thus growing LOWER segment
def rCleanerPartition(data, left, right, pivotIndex):

    print "\nPARTITION ENTRY:  "
    print str(data).strip('[]')
    print "LEFT:RIGHT:PIVOT {0}:{1}:{2}".format(left, right, pivotIndex)

    pivotValue = data[pivotIndex]

    # ATTN:  SWAP pivot value at END to prevent having to do FORWARD SHIFTS later!
    data[pivotIndex], data[right]  = data[right], data[pivotIndex]

    # ATTN:  - pivotIndex is dividing point between LOWER, HIGHER sections relative to the PIVOT VALUE
    #        - points to FIRST element of LOWER
    #        - increment when need to expand LOWER section on finding NEW element < PIVOT VALUE
    #        - initialize pivotIndex to one LESS than scanIndex!
    #          If never updated, this means ALL data values > Pivot Value!
    pivotIndex = (left - 1)
    # ATTN:  scanIndex is consuming data to examine RELATIVE to PIVOT, and is ALWAYs incremented
    #        NOTE stops one LESS than right since LAST element is PIVOT VALUE!
    for scanIndex in range(left, (right - 1)):
        # EZ CASE:  no need to move pivotIndex, just grow HIGHER SEGMENT by increase scanIndex from regular loop!
        # ATTN:  use INEQUALITY; no need to expand LOWER SEGMENT bound in this case
        if data[scanIndex] >= pivotValue:
            pass
        # GROW LOWER SEGMENT:  so need to move pivotIndex
        elif (data[scanIndex] < pivotValue):
            # ATTN:  increment pivotIndex FIRST to then be able to do SWAP
            pivotIndex += 1
            data[scanIndex], data[pivotIndex] = data[pivotIndex], data[scanIndex]

    # ATTN:  move pivot to its FINAL position
    data[pivotIndex], data[right] = data[right], data[pivotIndex]

    print "\nPARTITION EXIT:  "
    print str(data).strip('[]')
    print "PivotIndex:  {0}".format(pivotIndex)

    # ATTN:  returns MODIFIED input pivotIndex!
    return pivotIndex

# =======================================================================================================

try:

    # START with TEST DRIVER SCRIPT, or UNSORTED data; moving towards SORTED data
    # data = [54,26,93,17,77,31,44,55,20]
    data = [10, 80, 30, 90, 40, 50, 70]

    print "UNSORTED LIST: "
    # ATTN:  print elements of a LIST of str
    # OTHERWISE: straight conversion of sequence to a string, then remove enclosing brackets!
    # print ', '.join(data)
    print str(data).strip('[]')

    quicksort(data)

    print "\n SORTED LIST:  "
    print str(data).strip('[]')

except Exception as ex:

    # ATTN:  Python print stack trace
    # traceback.print_exc()
    logging.exception("WTF?!")









