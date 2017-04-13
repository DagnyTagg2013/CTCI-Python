# CACHING Kth Largest Element in a Stream
# - http://www.geeksforgeeks.org/k-largestor-smallest-elements-in-an-array/

# QUESTIONS:
# - K is small or large
# - N is small or large
# - want to cache LARGEST K or SMALLEST K from LARGE N in stream where K is a relative SMALL number

# SIMPLE SOLUTION 1: ARRAY (K is small, N is small)
# - ARRAY of K elements
# - find MIN:  O(K)
# - ATTN:  HOLD LARGEST
# - for (each) NEW element X, compare to MIN and if its GREATER, SWAP out MIN with NEW element
# - LOOP
# - COMPLEXITY:  O (N x K)
# *** NOTE: for K is 1:  its ENOUGH to cache SINGLE MIN
#
#
# SOLUTION 2:  MIN HEAP for K LARGEST elements, or MAX HEAP for K SMALLEST elements
# - MIN Heap (N is large, K is small)
# - for (each) NEW element X in stream; compare to MIN:  O(N)
#   if LARGER; remove MIN, and INSERT new element O(log K)
# - at any time, have got K elements in heap which are LARGEST
# COMPLEXITY:  O (N log K)
# where N is num elements encountered,
# and K is num elements cached on heap

# ALGO:
# - http://stackoverflow.com/questions/30914801/optimal-algorithm-to-return-largest-k-elements-from-an-array-of-infinite-number
# => PYTHON SORT:
# - mergesort used by default
# - can customize with fields/tuples for comparison with cmp function passed in
# => PYTHON MODULEs vs PACKAGE:
# - <filename>.py has <filename> as MODULE to import
# - __init__.py empty file designates the file directory name as PACKAGE to import

# ATTN:  ORDER of import name specification!
from HEAP import binheap

class CacheKLargestByList():

    def __init__(self, k):
        self.max_count = k
        self.count = 0
        # ATTN: can be SortedList via Python collection for Tree Structure?
        self.cache = []

    # NOTE:  this has logN QUICKSORT timing!
    def refreshMinInCache(self, newItem):
        # PUNT to sort FIRST
        self.cache.sort()
        # ATTN:  key point; if new item is greater than MIN, then SWAP IN new item to track LARGEST K RUNNING; or LARGER MIN!
        if (newItem > self.cache[0]):
            # Python SWAP in this case
            self.cache[0], newItem = newItem, self.cache[0]

        # ATTN, otherwise, don't save newItem, and drop it!

    def process_stream(self, newItem):

        # if Cache not yet FULL
        if self.count < self.max_count:
            self.cache.append(newItem)
            self.count += 1

        if self.count == self.max_count:
            self.refreshMinInCache(newItem)

        print "DEBUG:  cache contents"
        print self.cache

# TODO:  finish this implementation after extending heap support
"""
class CacheKLargestByHeap():

    def __init__(self, k):
        self.max_count = k
        self.count = 0
        # ATTN: can be SortedList via Python collection for Tree Structure?
        self.cache = binheap.BinHeap()

    # NOTE:  this has logN QUICKSORT timing!
    def refreshMinInCache(self, newItem):
        # KEY POINT:
        # - FIRST peek MIN on List to DECIDE if SWAP needed
        cachedMin = self.cache.heaplist[0]
        # ATTN:  key point; if new item is greater than MIN, then SWAP IN new item to track LARGEST K RUNNING; or LARGER MIN!
        if (newItem > cachedMin):
            # On REMOVE use APIs which INTERNALLY percDown the last-swapped-in element!
            extractedMin = self.cache.delMin
            # ADD in the newItem to cache, which INTERNALLY does APPEND and PERC-UP to Heapify!
            self.cache.insert(newItem)

            # TODO: REMOVE corruption of CACHE_LIMIT_PLUS_ONE

        # ATTN, otherwise, don't save newItem, and drop it!

    def process_stream(self, newItem):

        # if Cache not yet FULL
        if self.count < self.max_count:
            self.cache.heaplist.extend([newItem])
            self.count += 1

        if self.count == self.max_count:
            self.refreshMinInCache(newItem)

        print "DEBUG:  cache contents"
        print self.cache
"""


"""
    MAIN DRIVER TESTING of prior classes!
"""
inputStream = [4, 7, 3, 9, 1, 10]
processor = CacheKLargestByList(3)
for newItem in inputStream:
    processor.process_stream(newItem)


# TODO implement heap-based cache here!
# - Q:  need to REVISE binheap to INHERIT from AbstractAncestor?
# - Q:  NO typecheck on CTOR, but take variable of specified class type?
# - Q:  annotations for override?
# - revise init, insert, buildHeap

# TODO implement max-heap here!
# - Q:  need to allow override of comparison function
# - revise percUp, percDown, findMinChild
"""
class HeapCache(binheap):

    def __init__(self):
        pass

    def altered(self):
        pass
"""