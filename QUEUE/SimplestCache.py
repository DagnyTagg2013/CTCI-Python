__author__ = 'dagnyt'

from random import randint


# ***** ORIGINAL INTERVIEW Q *****
# Fixed-size cache
# initialized with a size, never to exceed that size
# put(key, val) O(1)
# get(key) -> val (or None) O(1)

# Test Cases added during chat
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

*** What I should have asked early on to help to clarify; as coding to initial PUT cases threw me off because of below (I did ask about Eviction policy)"

"Here's what I was thinking to do with an ALGO and DATA STRUCTURES to solve this problem that would make the most sense to me in a realistic situation,
but I don't know if you may be thinking of any data structure or policy simplification for the purposes of this interview exercise that you'd be happier with."

* What use-cases would you care about most (first)?  Would you like me to start those; or would you like to specify those first?
* I'm going to put comments/or tests for the key cases that I will code below; and you can let me know if this is along the lines you're looking for

* MAJOR POINTs to clarify

- EXTERNAL, PUBLIC CLIENT interface vs PRIVATE INTERNAL SERVER-driven interface and INTERNAL cache implementation
  eg Typically, a Cache Client should only care about GET functionality,
     where the internal implementation handles insert of fresh/new items into the internal cache data structure
     from a FETCH to DEEPer resource (e.g. DB, or even remote Server)

- EVICTION policy
  eg there are important key distinctions which affect data structure choices and approach such as:
     Last Recently WRITTEN vs
     Last Recently READ    vs
     Most Frequently READ

* MINOR POINTs to clarify

- What were the Types for Lookup Keys and then Values that we'd want?  (ie Array by int Key OK; or Dict needed)
- What were the Types for Priority metric that we want?

- MAJOR DISTINCTION within JAVA; where one can do Last-Recently-WRITTEN Cache via LinkedHashMap and removeEldestEntry(...)
http://stackoverflow.com/questions/224868/easy-simple-to-use-lru-cache-in-java
HOWEVER, is NOT the same as the more pragmatic real-world polic of Last Recently READ

"""
#
# ***** SO,  MAJOR INTERVIEW PUNT on EVICTION POLICY *****

# - so as not having to SORT FIFO PriorityQ content (for List in O(N); or for BinHeap in O(logN) implementations backing PriorityQ abstraction),
# PUNT on eviction policy to most RECENTLY WRITTEN LIFO @currSize index to avoid Performance Hit!

# (vs) in REAL-WORLD cases
# - typically only GET functionality exposed on a public interface; and not PUT
#   since retrieval of data for cache occurs within the internal implementation, and via
#   a fetch from a deeper resource (like DB or even remote location)
# - typically eviction priority logic is handled with LIFO Priority Q (NOT FIFO Stack) to:
# EVICT from low-priority side; and INSERT-with-SORT on High Priority Side
# -- so you RETAIN elements you most care about on LOWER Priority.

# eg1 RETAIN Most Frequently Accessed:
#    - keep count of access frequency on PriorityNode, with Lookup Key to Resource
#      then keep MIN BinHeap to EVICT in O(1) the least frequently accessed;
#      while adding in O(logN) the new element with access frequency count of 0

# ex2 RETAIN Most Recently Accessed:
#    - keep timestamp on PriorityNode, with Lookup Key to Resource
#      then keep MIN BinHeap to EVICT in O(1) the item with lowest timeSEQUENCE;
#      while adding in O(logN) new elements of higher timeSEQUENCE closest to the CURRENT time

# - typically INSERT new Item along with RE-SORT in PriorityQ after each ADD or REMOVE of Element into PriorityQ and associated Lookup Hash Dict!



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
    # - go add new resource into the internal Dictionary cache by key
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

        # INTERVIEW PUNT:  simulator for EXTERNAL DEEP DATA SOURCE; or a funciton which HOLDs State, can ITERATE on-fly without
        #                  preallocation like xrange
        # https://www.youtube.com/watch?v=bD05uGo_sVI
        self.deepDataSource = self.__DougAdamsGenerator()

    # TODO:  breakout into SEPARATE Server-side Interface
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

            # INTERVIEW PUNT:  DO NOTHING to update PriorityQ node for Read ACCESS; and RE-ORDER
            # FIFO PUNT to keep O(1) without shuffling priorityQ based on LAST WRITTEN Priority
            return alreadyExistResource

        # CASE 2.0: not found in Cache
        else:

            # INTERVIEW PUNT:  fetch resource from DEEPER location; like DB or Remote Server
            # deepFetchedResource = deepResource
            deepFetchedResource = next(self.deepDataSource)

            # TODO:  THROW EXCEPTION or return NONE if STILL NOT FOUND from DEEPER DATA SOURCE!

            # CASE 2.1:  Cache Full
            if (currentCacheSize == self.MAX_ITEMS):

                # INTERVIEW PUNT:  evict most recently WRITTEN (not necessarily READ) FIFO
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
            # INTERVIEW PUNT:  DO NOTHING to update PriorityQ node for Read ACCESS; and RE-ORDER
            # FIFO PUNT to keep O(1) without shuffling priorityQ based on LAST WRITTEN Priority
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