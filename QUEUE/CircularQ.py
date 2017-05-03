

__author__ = 'dagnyt'

# Applications of Circular Queues
# https://www.quora.com/What-are-the-applications-of-circular-queues-in-C

# WHY:  FIFO Queue; has REBUFERRING problem, having to SHIFT items over; so with this approach; no expensive shifting is necessary!
#       AND, can removeFromHead then deleteFromTail in O(1) constant time!
#       https://en.wikipedia.org/wiki/Circular_buffer#Full_.2F_Empty_Buffer_Distinction
#

# TRICKIEST:  - Differentiate between FULL vs EMPTY  (ie FRONT==REAR could mean FULL or EMPTY)
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
- use of Deque with Node having Prev/Next pointers to support insert-delete easily without having to track 'prev' pointer
"""

"""
    TODO:
        - implement via ARRAY
        - implement via LINKED LIST
"""

class Node:

    def __init__(self, data, prev=None, next=None):
        self.prev = prev
        self.data = data
        self.next = next

    def isSentinel(self):
        return (self.data == -1)

class CircleQ:

    def __init__(self, MAX_CAPACITY):
        self.MAX_CAPACITY = MAX_CAPACITY
        # set the SENTINEL here for EMPTY LIST
        self.HEAD = Node(-1)
        self.TAIL = self.HEAD

    def __repr__(self):

        scanPtr = self.HEAD
        while (self.HEAD is not None):
            print self.data
            scanPtr = self.next

    def __isEmpty(self):

        if (self.HEAD.data == -1) and (self.TAIL.data == -1):
            return True
        else:
            return False

    def __isFull(self):

        pass


    def appendToEnd(self, data):

        # CASE of EMPTY list
        if self.__isEmpty():
            self.HEAD = Node(data, self.TAIL)
        else:
            cacheTail = self.TAIL
            self.TAIL = Node(self.TAIL, data, cacheTail)

    # def removeFromFront(self):

