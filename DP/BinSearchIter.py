import logging

# Iterative Binary
# - ASSUMES data are ORDERED within SEQUENTIAL ARRAY
# - deconstructed to WHILE loop; updating EITHER end or start to midIdx
# - DEFAULT foundIdx to -1
# ATTN:  distinction between
def binSearch(toFind, data, startIdx, endIdx):

    foundIdx = -1

    # ATTN:  EMPTY is special case
    if (data is None) or (len(data) == 0):
        raise

    # ATTN:  use DELTA/2
    midIdx = startIdx + (endIdx - startIdx)/2

    # ATTN:  stop at less or equal to!
    while ((startIdx <= endIdx) and (foundIdx == -1)):

        if (toFind < data[midIdx]):
            # ATTN: iterate one BELOW to NARROW range
            endIdx = midIdx - 1
        elif (toFind > data[midIdx]):
            # ATTN:  iterate one ABOVE to NARROW range
            startIdx = midIdx + 1
        else:
            foundIdx = midIdx

    return foundIdx

try:
    # Driver Script
    data0 = []
    data1 = [3]
    data2 = [1, 2, 3]
    data3 = [2, 3, 6, 8]
    data4 = [2, 5]

    toFind = 3
    found0 = binSearch(toFind, data0, 0, len(data0) - 1)
    print found0

    found1a = binSearch(toFind, data1, 0, len(data1) - 1)
    print found1a

    found1b = binSearch(4, data1, 0, len(data1) - 1)
    print found1b


except Exception, ex:

    logging.exception(ex)