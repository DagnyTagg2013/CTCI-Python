

__author__ = 'dagnyt'

# Applications of Circular Queues
# https://www.quora.com/What-are-the-applications-of-circular-queues-in-C

# WHY:  FIFO Queue; has REBUFERRING problem, having to SHIFT items over; so with this approach; no expensive shifting is necessary!
#       AND, can removeFromHead then deleteFromTail in O(1) constant time!
#       https://en.wikipedia.org/wiki/Circular_buffer#Full_.2F_Empty_Buffer_Distinction
#

# TRICKIEST:  - Differentiate between FULL vs EMPTY  (ie HEAD==END could mean FULL or EMPTY)
#             http://stackoverflow.com/questions/17239317/circular-queue-without-wasting-an-entry-or-using-counter
#             https://en.wikipedia.org/wiki/Circular_buffer#Full_.2F_Empty_Buffer_Distinction
#             * avoid counter as one more thing to coordinate
#             * use SENTINEL value
#             - FRONT points to first Node; and SENTINEL->next is FRONT
#             - END points to next Node to write new data into (one past last node of actual data); and END->next is SENTINEL
#             * EMPTY is when FRONT == REAR of SENTINdEL value
#             * FULL is when FRONT is NOT SENTINEL value;  REAR->next->next is FRONT

"""

KEY INTERFACE OPERATIONS/BOUNDARY CONDITIONS

1) APPEND (to END)
   - check if FULL; and can either throw Exception, Return Error Code, or release thread then
     release Lock/wait()/capture Lock when notified/while loop to retest condition

2) REMOVE (from FRONT)
   - check if EMPTY; and can either throw Exception, Return Error Code, or release thread then
     release Lock/wait()/capture Lock when notified/while loop to retest condition

3) HANDLE EMPTY case
   -

4) HANDLE N-NODE case
   -

5) HANDLE FULL case

"""

"""
OPTIMAL:
- one element is "sentinel" element, separating HEAD and END elements of Queue;
  then you don't have to waste cycles checking every instance of updating currentCount
- use of Deque with Node having Prev/Next pointers to support insert-delete easily
  without having to track 'prev' pointer
"""

"""
    TODO:
        - implement via ARRAY
        - implement via LINKED LIST
"""

class Node:

    # def __init__(self, data, prev=None, next=None):
    def __init__(self, data, next=None):
        # self.prev = prev
        self.data = data
        self.next = next

    def isSentinel(self):
        return (self.data == -1)

"""
    def __repr__(self):
        print self.data
"""

class CircleQ:

    def __init__(self, MAX_CAPACITY):

        self.MAX_CAPACITY = MAX_CAPACITY

        # ATTN:  sentinel is MAX_CAPACITY + 1 Node
        sentinel = Node(-1)
        self.HEAD = sentinel

        # ATTN:  cache PRIOR
        prior = self.HEAD
        for i in xrange(0, MAX_CAPACITY):
            curr = Node(i)
            # ATTN:  link PRIOR to CURRENT,
            #        then advance PRIOR!
            prior.next = curr
            prior = curr

        # ATTN:  Now handle FINAL CIRCULAR connection to SENTINEL at MAX_CAPACITY + 1
        curr.next = sentinel

        # ATTN:  Now handle setting to EMPTY condition!
        self.TAIL = sentinel

    # def __repr__(self):
    def display(self):

        scanPtr = self.HEAD

        # ATTN:  TYPICALLY check is not None; but NOW check for SENTINEL RECUR flag
        #        as next is NEVER None in CIRCULAR List!
        #        AND We want to test for crossCount == 2 since we want to print ALL pre-allocated elements even with EMPTY unallocated!
        crossSentinelCount = 0
        while (crossSentinelCount != 2):
            if (scanPtr.data == -1):
                crossSentinelCount += 1
            print scanPtr.data
            scanPtr = scanPtr.next

        # TODO:  return a String from __repr__

    def isEmpty(self):

        # ATTN:  Typically check if these references are equal AND not None; but for our setup, use SENTINEL value
        if (self.HEAD.data == -1) and (self.HEAD == self.TAIL):
            return True
        else:
            return False


    def isFull(self):

        # ATTN:  distinction from EMPTY is SENTINEL
        if ((self.TAIL.data ==  -1) and (self.TAIL.next == self.HEAD)):
            return True
        else:
            return False


    # ATTN:  this becomes unecessary with doubly-linked Node which has PREV ptr in addition to NEXT
    def findNodeToInsertAfter(self):

        scanPtr = self.HEAD
        while (scanPtr.data != -1):
            scanPtr = scanPtr

    def appendToEnd(self, data):

        # CASE of EMPTY list
        if self.isEmpty():
            self.HEAD = Node(data, self.TAIL)
        # CASE of non-EMPTY list
        else:
            cacheTail = self.TAIL
            self.TAIL = Node(self.TAIL, data, cacheTail)

    # def removeFromFront(self):

# *************** TEST SCRIPT ***************


myQ = CircleQ(3)
# ATTN:  uses __repr__()
# print myQ
# ATTN:  uses public display
# EXPECTED:  0 1 2
myQ.display()

isEmpty = myQ.isEmpty()
# EXPECTED:  False
print isEmpty

isFull = myQ.isFull()
# EXPECTED:  True
print isFull







