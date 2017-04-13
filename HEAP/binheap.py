"""

HEAP PROPERTY:  (MIN)
    - for each node X with parent P;
    the key in P is smaller or equal to key in X
    - CAREFUL, this is not the same as INORDER; so LEFT and RIGHT child may have ANY relationship with EACH OTHER

COMPLEXITY:

    - GET MIN-MAX:  O(1) + O(logN)
      O(1) to remove ROOT @ MIN-MAX,
      BUT then have to do heapify
      SWAP last element into ROOT,
      PERC DOWN O(logN)

    - BUILD:  O(N) degenerate from O(NlogN)
      O(NlogN) to build entire tree via INSERT for each element
      => degenerates to O(N) since HALF nodes are LEAVEs due to FULL BINARY tree,
         and only need O(1) to move to ONE level-up,
         similarly for all OTHER nodes across levels that are above leaf levels
      => MAX NUM NODES at height H is:  (N + 1)/2exp(H+1)
         COST to PERCOLATE each node at height H is at most:  (H=1)
      => SUMMATION over EACH levels from H=0(LEAF) to H=logN(ROOT)
         TAKE (num nodes at H) x (cost to percolate at H)
         => 2(N+1)

    - INSERT:  O(logN)
      O(logN) to insert one element
      add to END of array
      PERCOLATE UP via //2 > 0
      SWAP with parent if it is LESS than parent; thus preserving heap property

    - DELETE:  O(logN)
      REMOVE ROOT(min);
      then SWAP LAST leaf to ROOT;
      PERCOLATE DOWN via i*2 > currentSize, and take MinChild of i*2 or (i*2 + 1)
      SWAP with MIN CHILD if it is GREATER than child; thus preserving heap property

    - SORT:  O(N)
      extract the ROOT O(1) x for N nodes:  so get ASCENDING ORDER for MIN-HEAP
      TRADEOFF:  DESTROYs data-structure in the process

APPLICATION:
    - track the 5 (LARGEST) elements coming from a stream of data with a LARGE volume of data that
      cannot be all stored within memory, where say you have a MAX capacity of 10

SOLUTION:
    - use a MIN HEAP to retain the 5 largest elements; while periodically paring out the MIN elements
    when you have a MAX capacity of 10
    - for each new element in stream; compare to MIN, if LARGER;
    - remove MIN, and INSERT new element
    - at any time, have got k elements in heap!


COMPLETE BINARY TREE IMPLEMENTATION serialized into Array: (enables logarithmic performance)
    - full tree; each level below root has two children, EXCEPT for leaf nodes
    - representation in random-access sequential storage
    - NONE @ index 0
    - any element @ index N
    - parent @ index N/2
    - left child @ 2N
    - right child @ 2N + 1

"""

import sys

# MIN HEAP implementation
class BinHeap:

    # external exception type
    INVALID_OP_FOR_EMPTY_MSG = "Cannot execute this operation on an Empty Heap"

    # internal limit on CACHE for HELD items, but PLUS ONE is for 0th element with dummy value of 0
    # _CACHE_LIMIT = 10

    def __init__(self):
        # 0th element is dummy placeholder with value 0
        self.heaplist = [0]
        self.currentSize = 0
        print "DONE with CTOR!"

    def printContents(self):
        print self.heaplist

    def isEmpty(self):
        # NOTE:  empty condition is when there's just the ONE 0th dummy value remaining!
        return (len(self.heaplist) == 1)

    # i is current index of element we're percolating UP the MIN heap
    # moving UP; need to do // 2 on i
    def __percUp__(self, i):
        # to move UP, but STOP once ROOT is reached; or just (prior) to 0th dummy element
        while i // 2 > 0:
            # IFF MIN HEAP property is violated; SWAP child with parent
             # TODO:  INVERT this comparison for MAX-HEAP
            if self.heaplist[i] < self.heaplist[i//2]:
                tmp = self.heaplist[i // 2]                 # save parent
                self.heaplist[i // 2] = self.heaplist[i]    # put child in parent's place
                self.heaplist[i] = tmp                      # swap parent into child's old place
            i = i // 2

    """
        INSERT just appends new element to END;
        then percolates UP the new element to restore heap property
    """
    def insert(self, newValue):
        # ATTENTION, test CACHE_LIMIT; but move OUTSIDE this implementation via INHERITANCE-OVERRIDE!
        # if ((self._CACHE_LIMIT + 1) == len(self.heaplist)):
             # EVICT MIN element, keeping CACHE number of MAX elements!
        #    top = self.delMin()
        #    print "Cache Eviction of element value:  {0}".format(top)
        # THEN, append newValue
        self.heaplist.append(newValue)
        self.currentSize = self.currentSize + 1
        self.__percUp__(self.currentSize)

   # FIND MIN CHILD - determines which is the smaller child in the cases of either just one or up to two children
    def __findMinChildIdx__(self, i):
    # in the case where we are at the last leaves of the tree; and
    # there is no right child existing; just take the last left child
    # ATTN:  CHECK BOUND for RIGHT CHILD!
        if (i * 2 + 1) > self.currentSize:
            return i * 2
        else:
        # TODO:  INVERT this comparison for MAX-HEAP
        # otherwise, there are two children; and we want to pick the smaller one
            if (self.heaplist[i*2] < self.heaplist[i*2 + 1]):
                return i * 2
            else:
                return i * 2 + 1

    # i is the current index of element we're percolating DOWN the MIN heap
    # moving DOWN; we need to do * 2 on i
    def __percDown__(self, i):
        # move DOWN, but STOP once LAST LEAF is reached; or AT the currentSize of the Heap!
        while (i * 2) <= self.currentSize:
            # ATTN:  on perc DOWN, need to swap with minChild!
            minChildIdx = self.__findMinChildIdx__(i)
            # TODO:  INVERT this comparison for MAX HEAP
            # IFF MIN HEAP property is violated; SWAP parent with child
            if self.heaplist[i] > self.heaplist[minChildIdx]:
                tmp = self.heaplist[i]
                self.heaplist[i] = self.heaplist[minChildIdx]
                self.heaplist[minChildIdx] = tmp
            i = minChildIdx

    """
        DELETE just pops TOP (MIN) element;
               then replaces it with BOTTOM (last leaf) element;
               then percolates DOWN that element to restore heap property

        returns top of Heap
    """
    def delMin(self):
        # CHECK BOUNDARY:  when NO elements are left to pop
        if (self.isEmpty()):
            raise ValueError(self.INVALID_OP_FOR_EMPTY_MSG);

        # ATTENTION:  TOP is always at index 1;
        # and index 0 is just a dummy value, just to simplify
        # arithmetic for walking the Heap
        # ATTENTION:  TOP is NOT retrieved with a pop() operation (bottom is);
        # so we need to first SAVE its value!
        top = self.heaplist[1]
        # SWAPs last LEAF into ROOT position
        self.heaplist[1] = self.heaplist[self.currentSize]
        # NOW shrink the array by POP/dropping off the bottom/tail!
        self.currentSize = self.currentSize - 1
        # removes redundant copy of LAST LEAF that got placed at the ROOT
        bottom = self.heaplist.pop()
        # percolate DOWN the swapped-in LEAF from the NODE position!
        self.__percDown__(1)
        return top

    """
        BUILDs a heap on THIS object; so OVERWRITEs any pre-existing one!
        - from an input List of items
        - such that MIN Heap property holds
        - starts at level JUST ABOVE the leaves; or HALFWAY through the full binary tree!
          then STOPs at the ROOT
        - percolates the value DOWN; WITHOUT LOSING original position
          then proceeds to next item
    """
    def buildHeap(self, alist):
        self.currentSize = len(alist)
        # START scanning nodes to move, exactly ONE level above bottom leaf level;
        # since we're going to Percolate Down the results!
        i = len(alist) // 2
        # initializes heaplist with 0th dummy element, and ALL items in input list
        self.heaplist = [0] + alist[:]


        # ATTN:  handle CACHING EXTERNAL to this implementation!
        # numToCopy = len(alist)
        # if (numToCopy >= self._CACHE_LIMIT:
        #    numToCopy = self._CACHE_LIMIT
        # self.heaplist = [0] + alist[0:numToCopy]

        # NOW HEAPIFY by MOVing from ONE LEVEL ABOVE LEAVES
        # UP to ROOT
        while (i > 0):
            self.__percDown__(i)
            i = i - 1

def main(args):

    # CASE 0:  CTOR
    print 'ENTERED Main!'
    bh = BinHeap()
    print 'RETURNED from CTOR'

    # CASE 1:  INITIALIZE 1
    print("\nINCREMENTALLY ADD from 1-4 HEAP CONTENTS")
    print("ADD 9:")
    bh.insert(9)
    bh.printContents()
    print("ADD 5:")
    bh.insert(5)
    bh.printContents()
    print("ADD 1:")
    bh.insert(1)
    bh.printContents()
    print("ADD 3:")
    bh.insert(3)
    bh.printContents()

    # CASE 2:  INITIALIZE 10 @ max external capacity
    # NOTE:  initialization REPLACEs any pre-existing heap!
    print("\nBULK-INIT 10-HEAP CONTENTS")
    bh.buildHeap([9,5,6,2,3,11,30,45,15,50])
    bh.printContents()

    # CASE 3:  Testing External Cache-Control
    print("\nADDING ELEMENT 88 to MAX-10 HEAP CACHE")
    print("CACHE BEFORE INSERT:")
    bh.printContents()
    newStreamElement = 88;
    bh.insert(newStreamElement);
    print("CACHE AFTER INSERT:")
    bh.printContents()

    # CASE 4:  Testing REMOVAL for SORT
    print "\nHEAP-SORTING VIA REMOVAL OF TOP MIN-ELEMENTS"
    print("HEAP BEFORE SORT:")
    bh.printContents()
    sortedResult = []
    while (not bh.isEmpty()):
        top = bh.delMin()
        # print "removing item value:  {0}".format(top)
        sortedResult.append(top)
    print("HEAP AFTER SORT:")
    bh.printContents()
    print "HEAP-SORTED RESULT:"
    print sortedResult

    # CASE 5:  Testing BOUNDARY case of deletion from EMPTY Heap
    print "\nATTEMPT REMOVAL from EMPTY HEAP:  "
    eh = BinHeap()
    eh.printContents()
    try:
        top = eh.delMin()
    except ValueError as e:
        print e
    else:
        print "Popped top with value of:  {0}".format(top)
    finally:
        print "This concludes testing for the EMPTY HEAP case!"


# NOTE:  use the following to permit in-module unit-testing!
# ATTENTION:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    main(sys.argv)