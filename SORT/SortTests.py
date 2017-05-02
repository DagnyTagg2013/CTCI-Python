import copy

"""

SORTING TAKEAWAYS for COMPARISON:  compare(self,rhs) on ITEM or compare(lhs, rhs) on COLLECTION;
                                   RETURNs -1 when LHS < RHS, 0 when equal, +1 when LHS > RHS
- use TUPLE comparisons as proxy-substitute for having to code field-by-field comparison WITHIN INTERNAL __cmp__
eg http://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php
- use INTERNAL __cmp__ on ELEMENT Class to do NATURAL ASCENDING order comparison on ALL fields of Element,
  and is applied on List.sort() for example; ALSO can pass in getKey function somehow ...
eg SORT/SortTests.py
- use EXTERNAL sort function (defined and passed as a Lambda variable) on COLLECTION Class to do CUSTOM order comparision on SELECTED fields of Element,
  or to SWITCH-UP NATURAL ascending order by differing sort order precedence of the fields, and the like!
eg /HEAP/binheap.py

"""

"""

1)

GIVEN
- Ice Cream Parlor
- T trips
- M total money per trip
- each trip has N flavors from 1..N, with a cost for each flavor

FIND
- 2 kids each choose 1 flavor; and must sum to cost M
- ORDER 1st flavor prior to second

2) QUESTIONS
- DUPLICATEs:
NO choosing DUPLICATE flavors; but 2 ice cream flavors may have SAME price!
- MULTIPLE valid results:
MUST return ALL suitable flavor pairs; of the ORIGINAL MENU ITEM index!

3) GOTCHAs:
- distinguish INDEX vs VALUE
so SORT index,
vs ICE-CREAM TYPE index
vs price of flavor

4)  PYTHON:
- shallow vs deepcopy
https://docs.python.org/2/library/copy.html
http://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list
- list find item in
# http://stackoverflow.com/questions/176918/finding-the-index-of-an-item-given-a-list-containing-it-in-python

5) COLLECTIONS and TUPLE vs CMP comparison overrides!

https://docs.python.org/2/library/collections.html
http://stackoverflow.com/questions/5292303/how-does-tuple-comparison-work-in-python
http://stackoverflow.com/questions/7803121/in-python-heapq-heapify-doesnt-take-cmp-or-key-functions-as-arguments-like-sor
http://javaconceptoftheday.com/java-priorityqueue-example/
http://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php
http://stackoverflow.com/questions/407734/a-generic-priority-queue-for-python
https://docs.python.org/2.7/library/queue.html#Queue.PriorityQueue
https://docs.python.org/3/_sources/library/heapq.

"""

"""

PROBLEM SOLVING APPROACHES

APPROACH 1:
- START with MAP of ICE-CREAM flavor => cost;
  then want to calc TOTAL - cost = MATCH complement cost
  and need to LOOKUP BY COST complement to derive back the corresponding flavor
  READ to create NEW MAP to REVERSE cost => flavor;
  then find index of THAT to determine complement flavor
**** PROBLEM:  Map will NOT resolve DUPLICATEs by COST

APPROACH 2:
- scan thru orig flavors, and calc complement cost for EACH encountered

- construct COPY of flavors array; then SORT it to BST structure, where NOW the indices are NOT the same as original menu flavor indices
*** TRICK:  scan SORTED array to look-ahead to LARGER complement cost, EXCLUDING duplicate ice-cream positions!

- ALTERNATIVELY can create MenuItem TUPLE that captures the original association;
  then to the SORT, pass in a  __cmp__ method to the SORT that only looks at the COST part

=> ON having this sorted structure, can do linear scan to find complement with HIGHER sort location than first flavor;
   to get the SECOND flavor.

NOTE: if trying to get complement flavor menu item index; must allow parameter to pass in first index to indicate to
      EXCLUDE that from the search for the second index!

- NOW RETURN to ORIGINAL Menu to use "indexOf" to FIND actual Menu flavor index corresponding to the complement cost;
since we need to 'reverse-engineer' that flavor location index!

SORTING HOW-TO:

sorted(iterable[, cmp[, key[, reverse]]])
- NOTE:  cmp is SLOWER since it hits 2 elements at a time instead of 1 each via getKey()
- https://docs.python.org/2/howto/sorting.html#sortinghowto

"""

"""
TEST INPUT:

2 (trips)
4 (trip1 has $4 total)
5 (has 5 flavors)
1 4 5 3 2
4  (trip2 has $4 total)
4  (has 4 flavors, with duplicate)
2 2 4 3

TEST OUTPUT:

1 4
1 2

"""

import copy

class menuItem:

    def __init__(self, menu_id, cost):
        self.menu_id = menu_id
        self.cost = cost

    # TODO:  SUPPORTs NATURAL ordering based on ALL fields
    #        but can override per-class, or apply via lhs,rhs to larger collection structure
    #        with __cmp__(lhs, rhs); BUT then less efficient to call over all overlapping adjacent pair elements!
    #
    # def __cmp__(self, rhs):
    # def compareByCosts(lhs, rhs):
    """
    def __cmp__(lhs, rhs):
        if (lhs.cost < rhs.cost):
            return -1
        elif (lhs.cost == rhs.cost):
            return 0
        else:
            return 1
    """
    def __cmp__(self, rhs):
        if self.cost < rhs.cost:
            return -1
        elif self.cost == rhs.cost:
            return 0
        else:
            return 1

    # MAJOR TODO:  handle DUPLICATE index finds when id differs!
    """
    def __eq__(self, rhs):
         if (    (self.cost == rhs.cost)  ):
             #and (self.menu_id == rhs.menu_id) ):
             return 1
         else:
             return 0
    """

    def __repr__(self):

        return "({}:{})".format(self.menu_id, self.cost)

# INSTEAD:  prefer getKey() method passed into sort operation on OVERALL collection!
def getKey(menuItem):
    key = menuItem.cost
    print "Key to SortBy:  {}".format(key)
    return key

def ext_cmp(lhs, rhs):
        if (lhs.cost < rhs.cost):
            return -1
        elif (lhs.cost == rhs.cost):
            return 0
        else:
            return 1

# TODO:  NOT generic for dataType!
def binSearch(toFind, data, startIdx, endIdx):

    foundIdx = -1

    # ATTN:  EMPTY is special case
    if (data is None) or (len(data) == 0):
        raise

    # ATTN:  use DELTA/2
    midIdx = startIdx + (endIdx - startIdx)/2

    # ATTN:  stop at less or equal to!

    while ((startIdx <= endIdx) and (foundIdx == -1)):

        #ATTN:  have to compare COST number to data subelement!
        if (toFind < data[midIdx].cost):
            # ATTN: iterate one BELOW to NARROW range
            endIdx = midIdx - 1
        elif (toFind > data[midIdx].cost):
            # ATTN:  iterate one ABOVE to NARROW range
            startIdx = midIdx + 1
        else:
            foundIdx = midIdx

    return foundIdx


def findComplementFlavorsByCost(menu, total):

    # construct MenuItems by COST collection; to be sorted by cost
    # GOTCHA allocate a LIST
    menuOrderedByCost = [None] * len(menu)
    for i in xrange(0, len(menu)):
        menuOrderedByCost[i] = menuItem(i, menu[i])
    print "LOADED COPY ORIGINAL MENU"
    print menuOrderedByCost

    # NOTE: this sort is to help us SKIP over duplicate values!
    # strategy = lambda(x): getKey(x)
    # ERROR:  getKey takes exactly one argument, two given
    # sorted(menuOrderedByCost, getKey)
    # sorted(menuOrderedByCost)
    menuOrderedByCost.sort()
    print "SORTED MENU!"
    endIdx = (len(menuOrderedByCost) - 1)
    print menuOrderedByCost

    for orderedByCostId in xrange(0, len(menuOrderedByCost)):

        complementCost = total - menuOrderedByCost[orderedByCostId].cost

        # ATTN:  similar to Java .indexOf equivalent to .find!
        # ATTN:  START search AFTER current index, so that found index will be DIFFERENT index
        #        and MIRROR IMAGE across PIVOT-MEDIAN from ORIGINAL menu
        # try:
        # ATTN:  for Python, List.index() gives no START index to offset into,
        #        so cannot START search AFTER current sorted position,
        #        AND it throws an Exception
        #        SO write-proprietary binsearch to simulate Java Arrays.binarySearch
        # sortedFlavorIndex = menuOrderedByCost.index(complementCost, (orderedByCostId + 1), endIdx)
        # TODO:  issue here where binsearch needs PARAMETERIZATION on type to compare objects!
        sortedFlavorIndex = binSearch(complementCost, menuOrderedByCost, (orderedByCostId + 1), endIdx)
        # TODO:  Handle case of -1 where NO complement found

        print "FOUND COMPLEMENT COSTS:  {}:({}:{})".format(menuOrderedByCost[orderedByCostId], sortedFlavorIndex, complementCost)

        """
                # ATTN:  List index()  exception if item not found
                except Exception as ex:
                    logging.exception(ex)
                    print 'NO COMPLEMENT FOUND; SKIP to CONSIDER NEXT FLAVOR PAIR!'
                    continue
        """

        # NOW, translate to an ORDERED pair of original menuIndexes for this pair of flavors found by orderedByCostId
        # orig_index1 = menuOrderedByCost[orderedByCostId].menu_id
        # orig_index2 = menuOrderedByCost[sortedFlavorIndex].menu_id

        # pairFlavors = (min( orig_index1, orig_index2), max(orig_index1, orig_index2))

        # return pairFlavors

# DRIVER SCRIPT:



menu = [1, 4, 5, 3, 2]
total = 4

dir(menu)

print "FINDING INDEX OF VALUE"
print menu.index(3,1,4)
# print menu.index(3,4,4)

findComplementFlavorsByCost(menu, total)

