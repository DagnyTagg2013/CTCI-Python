__author__ = 'dagnyt'

from random import randint


# ***** ORIGINAL INTERVIEW Q *****
# Fixed-size cache
# initialized with a size, never to exceed that size
# put(key, val) O(1)
# get(key) -> val (or None) O(1)

# Test Cases added during chat, with GET cases added after PUT cases
"""
testCache = Cache(3)
testCache.put("A", 1)
testCache.put("B", 2)
testCache.put("C", 3)
print testCache.get("B") # 2
testCache.put("D", 4)
print testCache.get("A") # One of these should be None
print testCache.get("B")
print testCache.get("C")
print testCache.get("D")
"""

"""

*** What I could have asked early on to help to clarify;

"Here's what I was thinking to do with an ALGO and DATA STRUCTURES to solve this problem
that would make the most sense to me in a real-world situation,
but I don't know if you may be thinking of any simplifications in data structures or algo
for the purposes of this interview exercise that you'd be happier with.
In which case; please specify."

* What test-cases/use-cases would you care about most (first)?
  Would you like me to start those;
  or would you like to start specifying those first?

* I'm going to put comments/or tests for the key cases that I will code below;
  then you can let me know if this is along the lines you're looking for in this interview

A) MAJOR POINTs to clarify

1) DECOUPLED interfaces on INTERMEDIARY CACHE implementation (between CLIENT and Data SERVER)
   eg1 PUBLIC CLIENT interface (CLIENT-driven GET, usually)
   eg2  PRIVATE INTERNAL (SERVER-driven PUT, usually)

   ie Typically, a Cache Client should only care about GET functionality,
      whereas an internal Server-facing implementation handles insert of fresh/new items into the internal cache data structure
    via a FETCH to DEEPer resource (e.g. DB, or even remote Server)

2) UPDATE/PUT policy (SERVER driven, USUALLY)

  This is typically driven SERVER-side; and DE-COUPLED from Client-side cache interface interface
  eg1 EVENT-DRIVEN:  item-based PUSH of each resource ELEMENT based on latest-written items from DEEPER DB,
                     with auto-increment monotonically increasing versionSequenceID.  This ID is used on Cache implementation
                     for Idempotency to only update on message with new increasing version ID.
  eg2 TIMED-BATCH DRIVEN:  PERIODIC-batch-pull of latest-written items from DEEPer DB,
                           OK to assume ALWAYs gets latest-state

3) EVICTION policy on GET (CLIENT-driven, USUALLY)

  ie there are important key distinctions which affect data structure choices and approach such as:
  eg1 Last Recently WRITTEN
      http://katrinaeg.com/lru-cache.html
  eg2 Last Recently READ
  eg3 Most Frequently READ

4) TIME-COMPLEXITY order of operations indicating Data Structures to use

  https://wiki.python.org/moin/TimeComplexity
  http://stackoverflow.com/questions/6256983/how-are-deques-in-python-implemented-and-when-are-they-worse-than-lists

  * need a FIFO Queue to (prioritize) Data to Evict (RETAIN on front; EVICT from end)
    - remove from middle, or find-remove
    - remove from end
    - add to front
    eg1 Array:  O(n)/O(1 + n)/O(n) as have to shift over items in contiguous memory
        List:   O(n)/O(1 + n)/O(n) as have to track next-prior where get() works in constant time in Python
                http://stackoverflow.com/questions/37350450/why-is-a-list-access-o1-in-python
        Deque:  O(n)/O(1)/O(1) where pop() and appendleft() work in constant time in Python
        heapq or PriorityQ:  O(1)/O(logN)/O(1) where delMin() works in constant time, insert() in O(logN) time
                 https://docs.python.org/2/library/queue.html

    **** NOTE: SORT for BinHeap/PriorityQ uses DEFAULT Python DEEP Comparison of TUPLE with (Priority, Data)

  * Need a NODE entity with RESOURCE data,
                       and PRIORITY (timeSequenceID for READ, accessCount for READ, timeSequenceID for WRITE)

  * Need a Lookup Map from KEY to NODE to easily FIND resource data by Client Lookup Key to Cache with

5) MINOR POINTs to clarify
eg1 What were the Types for Lookup Keys VS Resource Values that we'd want?  (ie Array by int Key OK; or Dict needed)
eg2 What were the Types for Priority metric that we want? (ie. ReadTimeSequenceID, RequestFrequencyCount, WriteVersionSequenceID, etc)
eg3  What were the Types for handling Idempotency for Data Version Updates (ie. WriteVersionSequenceID, etc)

6) LANGUAGE-SPECIFIC tricks

eg1 JAVA; where one can do Last-Recently-WRITTEN Cache via LinkedHashMap and removeEldestEntry(...)
http://stackoverflow.com/questions/224868/easy-simple-to-use-lru-cache-in-java
HOWEVER, this is NOT the the same as the more pragmatic real-world policies that are CLIENT-driven (as above)

TODO:  lookup CIRCULAR DEQUE implementation below
TODO:  implement LRU cache as below
eg2 Python3; where one can use DQUEUE, circular
http://katrinaeg.com/lru-cache.html
http://www.geeksforgeeks.org/implement-lru-cache/

7) DEEPER CACHE-REPLACEMENT POLICIES

https://en.wikipedia.org/wiki/Cache_replacement_policies

"""
#
# ***** SO,  MAJOR INTERVIEW PUNT on EVICTION POLICY *****

# - so as not having to SORT FIFO PriorityQ content (for List in O(N);
# or for BinHeap in O(logN) implementations backing PriorityQ abstraction),
# PUNT on eviction policy to most RECENTLY WRITTEN LIFO @currSize index to avoid Performance Hit!

# (vs) in REAL-WORLD cases
# - typically only GET functionality exposed on a public interface; and not PUT
#   since retrieval of data for cache occurs within the internal implementation, and via
#   a fetch from a deeper resource (like DB or even remote location)
# - typically eviction priority logic is handled with FIFO Priority Q (NOT LIFO Stack) to:
#   EVICT from END or Low-priority side;
#   and INSERT at BEGIN -with-SORT on High Priority Side
# -- so you RETAIN elements you most care about on HIGHER Priority.

# eg1 RETAIN Most Frequently Accessed:
#    - keep count of access frequency on PriorityNode, with Lookup Key to Resource
#      then keep MIN BinHeap to EVICT in O(1) the least frequently accessed;
#      while adding in O(logN) the new element with access frequency count of 0 to START

# ex2 RETAIN Most Recently Accessed:
#    - keep timestamp on PriorityNode, with Lookup Key to Resource
#      then keep MIN BinHeap to EVICT in O(1) the item with lowest timeSEQUENCE;
#      while adding in O(logN) new elements of higher timeSEQUENCE closest to the CURRENT time

# - typically INSERT new Item along with RE-SORT in PriorityQ after each ADD or REMOVE of Element
#   into PriorityQ AND update associated Lookup Hash Dict!


"""

    GET semantics

    # LOOKUP internal Hash Map/Dict by key to see if resource already in cache; and DEFAULT to None if not found

    # CASE 1.0: already in cache
    #
    #           - update/re-sort priorityQ IFF Current Get/READ access relevant
    #             to priority eviction policy e.g. Most Frequently READ, Most Recently Read
    #           - return the found resource

    # CASE 2.0: not already in cache
    #
    #           - go FETCH resource from DEEPER location:  DB or Remote Server
    #           - TODO:  API DECISION TO THROW EXCEPTION or return NONE if STILL NOT FOUND from DEEPER DATA SOURCE!

    # CASE 2.1: count == MAX
    #           - find key to EVICT via PriorityQ supporting EVICTION POLICY; FIFO to evict FIRST Prioritized
    #           - lookup resource in internal cache Dict to FREE using key from above
    #           - free lookup dependent cache and Q references and FREE them to avoid Memory Leaks
    #
    # CASE 2.2: count < MAX
    #           pass

    # (common to all cases 2.1, 2.2)
    # - go update/insert new resource into the internal Dictionary cached by key
    # - go insert/re-sort PriorityQ by Priority metrics associated with above
    # - return the resource from Cached Dict if found

"""


class SimpleCache:

    # INTERVIEW PUNT:  simulator for EXTERNAL DEEP DATA SOURCE; or a funciton which HOLDs State, can ITERATE on-fly without
    #                  preallocation like xrange
    # https://www.youtube.com/watch?v=bD05uGo_sVI
    def __DougAdamsGenerator(self):
        # SIMILAR to randint(0,max)
        for i in xrange(42,100):
            yield i


    def __initialLoad(self):

        # INTERVIEW PUNT:  simulate initial cache load of DEFAULT data from DEEPER data source; LESS than MAX
        self.lookupDict = { "A":1,
                            "B":2}

        self.priorityQ[0] = "A"
        self.priorityQ[1] = "B"

        # print self.lookupDict
        # print self.priorityQ

        # INTERVIEW PUNT:  simulator for EXTERNAL DEEP DATA SOURCE; or a function which HOLDs State, can ITERATE on-fly without
        #                  preallocation like xrange
        # https://www.youtube.com/watch?v=bD05uGo_sVI
        self.deepDataSource = self.__DougAdamsGenerator()

    # TODO:  breakout into SEPARATE Server-side Interface
    # TODO:  also support one-off Event-Driven data update with Idempotency check on WriteVersionSequenceID
    def batchRefresh(self):

       # INTERVIEW PUNT:  simulate CACHE REFRESH Driven SERVER-side;
       #                  as INDEPENDENT and decoupled from CLIENT-SIDE access and PriorityQ Metrics!
       for cacheKey in self.lookupDict:
            self.lookupDict[cacheKey] = next(self.deepDataSource)

    def __repr__(self):
       return "LOOKUP MAP:\n{}\nPRIORITY Q:\n{}".format(self.lookupDict, self.priorityQ)

    def __init__(self, maxItems=3):

        self.MAX_ITEMS = maxItems
        # MINOR TRICK:  this is keyed by associative key of any type, to resource value
        self.lookupDict = {}
        # MAJOR TRICK:  this should run as PRIORITY Q to delMin to RETAIN items @ FRONT, to EVICT @ END
        #               AND it holds lookup KEY to resource in the lookupDict to reference actual resource above!
        self.priorityQ = [None] * self.MAX_ITEMS

        self.__initialLoad()


    def get(self, key):

        alreadyExistResource = self.lookupDict.get(key, None)
        currentCacheSize = len(self.lookupDict)

        # CASE 1.0: found in Cache
        if (alreadyExistResource is not None):

            # INTERVIEW PUNT:  DO NOTHING to update PriorityQ node for Read ACCESS; and RE-ORDER,
            # LIFO PUNT to keep O(1) (without) shuffling priorityQ based on LAST WRITTEN Priority
            return alreadyExistResource

        # CASE 2.0: not found in Cache
        else:

            # INTERVIEW PUNT:  fetch resource from DEEPER location; like DB or Remote Server
            # deepFetchedResource = deepResource
            deepFetchedResource = next(self.deepDataSource)

            # TODO:  THROW EXCEPTION or return NONE if STILL NOT FOUND from DEEPER DATA SOURCE!

            # CASE 2.1:  Cache Full
            if (currentCacheSize == self.MAX_ITEMS):

                # INTERVIEW PUNT:  evict most recently WRITTEN (not necessarily READ) LIFO
                # MAJOR POINT! ==> FREE DANGLING object REFERENCES to prevent Memory Leaks!
                #              ==> FREEs the old resource somehow,
                #                  by allowing runtime to handle compaction of dereferenced resource;
                #                  not just a SHALLOW Dict key removal!
                # http://stackoverflow.com/questions/5844672/delete-an-item-from-a-dictionary
                oldResourceKey = self.priorityQ[(self.MAX_ITEMS - 1)]
                oldResource = self.lookupDict[oldResourceKey]
                self.lookupDict[oldResourceKey] = None
                del(self.lookupDict[oldResourceKey])
                currentCacheSize -= 1
                # free associated priorityQ reference
                self.priorityQ[(self.MAX_ITEMS - 1)] = None

            # CASE 2.2: Cache Not Full
            else:

                # defer to shared processing for general Case 2.0
                pass

            # for BOTH cases 2.1, 2.2; we want to ADD to PriorityQ, and lookupDict!
            # INTERVIEW PUNT:  DO NOTHING to update PriorityQ node for Read ACCESS, and RE-ORDER
            # INSTEAD:  LIFO PUNT to keep O(1) without shuffling priorityQ based on LAST WRITTEN Priority
            self.lookupDict[key] = deepFetchedResource
            self.priorityQ[currentCacheSize] = key

        # 2.0
        return self.lookupDict[key]

        # should never get here

# *************** TEST DRIVER SCRIPT *****************

print "\n***** STARTING TEST SCRIPT *****\n"

testCache = SimpleCache(3)
print "IMMEDIATELY AFTER CTOR:"
print "\nEXPECT A, B loaded, with None space in Cache"
print testCache

r1 = testCache.get("A")
print "\nEXPECT A returned resource"
print "Resource for A:  {}".format(r1)
print testCache

r2 = testCache.get("B")
print "\nEXPECT B returned resource"
print "Resource for B:  {}".format(r2)
print testCache

r3 = testCache.get("C")
print "\nEXPECT C deep-fetched"
print "Resource for C:  {}".format(r3)
print testCache

r4 = testCache.get("D")
print "\nEXPECT C evicted, D deep-fetched"
print "Resource for D:  {}".format(r4)
print testCache

testCache.batchRefresh()
r5 = testCache.get("A")
print "\nEXPECT A with UPDATED data"
print "Resource for A:  {}".format(r5)
print testCache