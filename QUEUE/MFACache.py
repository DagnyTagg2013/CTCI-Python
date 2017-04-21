__author__ = 'dagny t'


# TODO: CAN TWEAK to do MOST RECENTLY ACCESSED via timestamp updates!

# Implement MOST FREQUENTLY USED  (Prioritize by COUNT of Accesses)
# KEY DATA STRUCTURES:  Priority Node by NumHits,
#                       Dictionary cache by URL to full Node to quickly update NumHits,
#                       Queue ordered with Most Frequent at FRONT, and Least Frequent NEW values at END to allow for easy eviction
# KEY ALGO:  need to update priority and SORTED POSITIOn in queue EACH time collection changes sohmehow
# TODO:  use deque collection! with MOST FREQUENT ACCESSED on one side, LEAST FREQUENT ACCESSED on ANOTHER
# - https://docs.python.org/2/library/collections.html#collections.deque
# TODO:  OR use Priority Queue collection => this reduces time to FIND LEAST frequently used, as based on HEAP!
# - http://boltons.readthedocs.io/en/latest/queueutils.
# PROBLEMS:  SLOW due to synchronization, AND no parameterizeable comparator function!
# https://docs.python.org/3/library/queue.html#Queue.PriorityQueue
# TODO:  use Dict to MAP from KEY of Item direct to Node Element on the Queue!
# PUNTING:  use LIST and SORT it EACH TIME priority of element modified!
# http://pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/

class PriorityNode:

    # ATTN:
    # - remember __ for ctor
    # - remember self
    # - OK to just reference self elements for declaration
    def __init__(self, url, page):
        # ATTN:  url or lookup KEY User Accesses
        self.key = url
        # ATTN:  PRIORITY, by count of number of Accesses!
        self.numHits = 1
        self.value = page

    def incrementHits(self):
        self.numHits += 1

    # ATTN:  allows to be PRINT-FORMATTED!
    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__,
                                  self.key,
                                  self.numHits,
                                  self.value)

    # ATTN to KEY POINT; to support this interface
    # SIMILARLY, could have sorted collection
    # - might use -1 * override to negate ASCEND to DESCEND on SPECIFIC INTEGER FIELD; but prefer to supply REVERSE parameter!
    # - MULTIPLE compound fields
    # - TUPLE elements, with FIRST-VALUE be INTEGER-valued KEY
    def __cmp__(self, other):
        if hasattr(other, 'numHits'):
            return self.numHits.__cmp__(other.numHits)

class MostFrequentlyUsedCache:

    def __init__(self, maxItems):

        self.MAX_ITEMS = maxItems
        # direct lookup to cached resource
        # ATTN:  Cache holds VALUE resource accessed, which is NOT duplicated in PriorityNode!
        self.lookupCache = {}
        # Q with MOST frequent access on LEFT for RETENTION
        #   but LEAST frequent access on RIGHT for fast REMOVAL!
        # ATTENTION:  simulate with finite-sized LIST-ARRAY since assume SMALL-SIZE MAX_ITEMS == 5!
        # self.freqPriorityQ = deque()
        # ATTN:  init list of certain size
        # http://stackoverflow.com/questions/10712002/create-an-empty-list-in-python-with-certain-size
        # ATTN:  this DOES need to hold pointer to PRIORITY NODE to lookup and increment; but ALSO the associated resource value!
        # KEY ISSUE:  needs to SORT via frequency as KEY of sort, so save elements of TUPLEs with primary value as FREQUENCY COUNT
        self.freqPriorityQ = [None] * self.MAX_ITEMS

    def get(self, url):

        # http://pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
        # sorted(self.freqPriorityQ, cmp, key, reversed=True )
        def getKey(priorityNode):
            return priorityNode.numHits

        # CASE 1:  accessed URL IS in cache,
        #          so INCREASE Priority Hit Count, RESORT Q by Priority
        #          return specific URL resource from cache!
        cachedPriorityPageNode = self.lookupCache.get(url, None)
        if (cachedPriorityPageNode is not None):

            # find the PRIORITY Node, and INCREASE its counter value!
            cachedPriorityPageNode.incrementHits()
            # NOW, re-sort the PRIORITY Q based on REVERSE-ORDER HIGHEST hits on FRONT, LOWEST on BOTTOM to minimize reshuffle
            #      as EVICTIONs come from RIGHT side of Q!

            # KEY POINT:  on modification of priority, need to RE-SORT!
            # give method to derive KEY from Node, then
            # whether to reverse T/F
            # NOTE:  CAREUL to move to FRONT of QUEUE the LEAST FREUQENTLY ACCESSED, and not just the LAST frequently accessed!
            # sorted(self.freqPriorityQ, getKey, True)
            sorted(self.freqPriorityQ)
            # NOW, debug to get values!
            print self.freqPriorityQ

            # ATTN:  returns actual resource VALUE
            return cachedPriorityPageNode.page

        # CASE 2: accessed URL is NOT in cache
        else:

            # simulate some code to DEEP-FETCH page from origin service, then construct priorty node from that
            page = "Deep-Fetched Page"
            newNode = PriorityNode(url, page)

            # CASE 2a:  cache is NOT full, so add it to cache and priority queue
            if ( len(self.lookupCache) < self.MAX_ITEMS ):

                # ATTN:  for lookup EASE, for frequency count updates, roll frequency count in same node as page resource value!
                self.lookupCache[newNode.url] = newNode
                # ATTN:  append on RIGHT as LEAST FREQ HIT, so can remove easily later
                self.freqPriorityQ.append(newNode)

            # CASE 2b:  cache is FULL, so EVICT LEAST frequently used item on RIGHT of PriorityQ,
            #                          also from lookup cache
            #                          then ADD NEW item to both lookupCache and RIGHT of PriorityQ
            else:

                # REMOVE key from Cache by lowest PRIORITY on RIGHT; then lookup in Dict to remtove it from THERE also!
                # http://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-
                leastPriorityNode = self.freqPriorityQ.pop()
                # ATTN:  KEY POINT to DRIVE cache item to remove via associating priority to URL KEY!
                leastPriorityPage = self.lookupCache.pop(leastPriorityNode.key, None)

                # ATTN:  append NEW Node on RIGHT as LEAST FREQ HIT
                self.freqPriorityQ.append(newNode)
                self.lookupCache[newNode.url] = newNode

# ATTN:  no PUT operation; as GET drives all DEEP-FETCHES of remote Page data!

# TESTING SCRIPT:
# - NOTE:  can use EITHER __cmp__ OR getKey methods to OVERRIDE; BUT __cmp__
#   is MORE extensible in that it support MULTIPLE non-integer field comparison overrides; but getKey() is only used in Sorted API
# - ALSO NOTE:  heapq is NOT parameterized to __cmp__; and priorityQ is therefore not either as its implemented with heapq;
#   but it DOES use getKey() and you can just save TUPLE as collection elements with Integer ordering value as first tuple element;
#   but must use INTEGER key to return from getKey()
# - OPTION 1:  with getKey override:  sorted(self.freqPriorityQ, getKey, True)
# - OPTION 2:  without getKey override:  sorted(self.freqPriorityQ)
# - cmp returns < 1 if LHS < RHS; 0 if equal; +1 if LHS > RHS

# TODO:  test REVERSE order with __cmp__ also!


