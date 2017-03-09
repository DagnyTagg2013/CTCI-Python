
# ALGO:  cache-memo PRIOR results to avoid entering redundant calculations!
#       BUILD on prior results!

# ATTN:  Python Arrays vs Lists
# http://stackoverflow.com/questions/176011/python-list-vs-array-when-to-use
# https://bradfieldcs.com/algos/analysis/performance-of-python-types/
# http://infoheap.com/python-initialize-list-with-same-value/

def rCountSkipPaths(hops, cache):

    # handle error-bound case!
    if (hops < 0):
        return 0

    elif (hops == 0):
        return 1

    # KEY
    elif (cache[hops] != -1):
        return cache[hops]
    else:
        # CALCULATE RESULT FROM PRIOR SMALL-CASE COMPONENTS, and CACHE for recall
        cache[hops] = rCountSkipPaths(hops - 1, cache) + \
                      rCountSkipPaths(hops - 2, cache) + \
                      rCountSkipPaths(hops - 3, cache)

    return cache[hops]

# load number of staircases
# load subsequent number of stairs
def loadStairCaseHeights():

    num_staircases = int(raw_input().strip())
    stairs = []
    for i in xrange(0, num_staircases):
        # ATTN:  note strip() and cast to int()
        oneStairsHeight = int(raw_input().strip())
        stairs.append(oneStairsHeight)

    return stairs


def countSkipPaths(hops):

    # ATTN:  initialize LIST with SAME VALUE
    cache = [-1] * (hops + 1)
    return rCountSkipPaths(hops, cache)

def loopDriver(stairs):

    for i in xrange(0, len(stairs)):
        numSkipPaths = countSkipPaths(stairs[i])
        print numSkipPaths


# SCRIPT to RUN this!
# countSkipPaths(3)
stairs = loadStairCaseHeights()
loopDriver(stairs)

"""
sample output:
3
1
3
7
1
4
44
"""


