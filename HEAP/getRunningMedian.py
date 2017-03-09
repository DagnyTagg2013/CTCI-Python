
# PROBLEM:  find the running median from a STREAM of ints
#

# - PYPI; the Python Package Index, kinda like Maven Repo!
# https://pypi.org

# - THEORY:  Heaps, Convert Heaps, Heapify, etc
# https://courses.csail.mit.edu/6.006/fall10/lectures/lec09.pdf

# TODO:
# - cache klargest
# have MAX HEAP, compare NEW to MAX ROOT in O(1); or ADD it in O(logN), but ONLY after REMOVING LAST MIN element!
# - cache via latestSequenceId or Timestamp

"""
ALGO:

We can use a max heap on left side to represent elements that are less than the effective median,
and a min heap on right side to represent elements that are greater than the effective median.

After processing an incoming element, the number of elements in heaps differ at most by 1 element.
When both heaps contain the same number of elements, we find the average of heap's root data as effective median.
When the heaps are not balanced, we select the effective median from the root of heap containing more elements.

- http://stackoverflow.com/questions/10657503/find-running-median-from-a-stream-of-integers

  For the first two elements add SMALLER one to the maxHeap on the left, and BIGGER one to the minHeap on the right.
  Then process stream data one by one,

  Step 1: Add next item to one of the heaps
  if next item is smaller than maxHeap root add it to maxHeap, else add it to minHeap

  Step 2: Balance the heaps (after this step heaps will be either balanced or
  one of them will contain 1 more item)

  if number of elements in one of the heaps is greater than the other by
  more than 1, remove the root element from the one containing more elements and
  add to the other one

  Then at any given time you can calculate median like this:

  If the heaps contain equal amount of elements;
    median = (root of maxHeap + root of minHeap)/2
  Else
    median = root of the heap with more elements

PYTHON COLLECTIONs:

HeapQ vs PriorityQueue
http://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php
http://stackoverflow.com/questions/36991716/whats-the-difference-between-heapq-and-priorityqueue-in-python

* PriorityQ
- threadsafe, slower
- https://docs.python.org/2/library/queue.html
- encapsulates list
- DEFAULT minheap
- TO use MAXHEAP -- can  first NEGATE elements prior to input,
  then negate them after output
- supports BASIC primitive elements, as well as TUPLE with Priority-first as primitive
- supports COMPLEX multi-field object comparison via _cmp_ override of Element
L < R => -ve for ASCENDING order
- uses put, get

* heapqueue
* http://stackoverflow.com/questions/14189540/python-topn-max-heap-use-heapq-or-self-implement
- DEFAULT minheap
- binds to list
-  TO use MAXHEAP -- can  first NEGATE elements prior to input,
  then negate them after output
  OR
- http://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python
 # ATTN: if an EVEN number, then STOP one SHORT
            if not (n % 2):
                n -= 1
import heapq
listForTree = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
heapq.heapify(listForTree)             # for a min heap
heapq._heapify_max(listForTree)        # for a max heap
_heappushpop_max, _siftdown_max, and _siftup_max
*** We should ONLY use heapq's function after heapifying the list!

- ROOT index at 0 (not 1)
- binds to [] list
- uses heappush, heappop

* COMPARATOR METHOD:

where ASCENDING order is:
+ when LHS > RHS
0 when equal
- when LHS < RHS

http://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python
http://stackoverflow.com/questions/33024215/built-in-max-heap-api-in-python


- Djikstra and priority queues
https://algocoding.wordpress.com/2015/03/25/dijkstras-algorithm-part-3b-priority-queue-in-java/

- priority Queue in Java w comparator for MIN-MAX
https://algocoding.wordpress.com/2015/03/25/dijkstras-algorithm-part-3b-priority-queue-in-java/

- ATTN:  list vs tuple efficiency; EXTEND over APPEND!
http://stackoverflow.com/questions/14446128/python-append-vs-extend-efficiency

"""


# import sys
# ver. < 3.0
# import Queue as Q
# impor math
import heapq

class RunningMedian:

    # init heaps to form something like a binsearch partition, but on MEDIAN element (picture HOURGLASS w RHS minheap on TOP
    # - LHS MAX HEAP is all elements LESS than median, where median is root of MAX heap
    # - RHS MIN HEAP is all elements GREATER than median, where median is root of MIN heap
    # smaller input element goes to root of LHS MAX HEAP, larger input element goes root of RHS MIN HEAP
    def init(self, first, second):

        if (first < second):
            self.maxheap = [first,]
            self.minheap = [second,]

        else:
            self.maxheap = [second,]
            self.minheap = [first,]

    # ATTN:  this is Python default CTOR with explicit THIS pointer!
    def __init__(self):

          self.stagefirst = -1
          self.maxheap = []
          self.minheap = []


    # - ADD to END, then SWAP-PERCOLATE UP to root
    # - if input number is smaller than median root of MAX HEAP, then add it to MAX_HEAP, call heapify()
    # - otherwise, add to MIN_HEAP, to call heapify()
    # - TEST which heap has more elements; then pull those out to insert into smaller heap to keep them BALANCED
    def addNewItem(self, newitem):

        maxlen = len(self.maxheap)
        minlen = len(self.minheap)

        # ATTN:  Handle adding FIRST item!
        if (maxlen == 0) and (minlen == 0) and (self.stagefirst == -1):
            self.stagefirst = newitem
            return

        # ATTN:  Handle adding SECOND item!
        if (maxlen == 0) and (minlen == 0) and (self.stagefirst != -1):
            if (newitem < self.stagefirst):
                self.maxheap.append(newitem)
                self.minheap.append(self.stagefirst)
            else:
                self.minheap.append(newitem)
                self.maxheap.append(self.stagefirst)
            return

        # ATTN:  Handle adding items beyond SECOND item!
        if (newitem < self.maxheap[0]):
                heapq.heappush(self.maxheap, newitem)
                # ATTN:  must heapify each time!
                heapq._heapify_max(self.maxheap)
        else:
                heapq.heappush(self.minheap, newitem)
                # ATTN:  must heapify each time!
                heapq.heapify(self.minheap)

        # ATTN:  RECALC difference after add!
        maxlen = len(self.maxheap)
        minlen = len(self.minheap)
        difference = maxlen - minlen
        abs_difference = abs(difference)

        # ATTN:  STOP when difference is 1 or less
        # e.g. test on diff 3, diff 2, diff 1
        stop = (abs_difference - 1)
        for i in range(0, stop):

            # more elements in TOP RHS minheap
            if (difference < 1):
                overflow = heapq.heappop(self.minheap)
                heapq.heappush(self.maxheap,overflow)
                # ATTN:  Must heapify EACH time!
                heapq._heapify_max(self.maxheap)

            # more elements in BOTTOM LHS maxheap
            if (difference > 1):
                overflow = heapq.heappop(self.maxheap)
                heapq.heappush(self.minheap, overflow)
                heapq.heapify(self.minheap)

    # ATTN:  handle all initialization scenarios!
    # i.e. EMPTY, 1-element, more than 1 element!
    def getMedian(self):

       # ATTN:  Handle INITIAL Boundary case of ZERO-ELEMENT heap
       lowerLen = len(self.maxheap)
       upperLen = len(self.minheap)
       if (lowerLen == 0) and (upperLen == 0) and (self.stagefirst == -1):
           return -1

       # ATTN:  Handle case of ONE element heap!
       if (lowerLen == 0) and (upperLen == 0) and not(self.stagefirst == -1):
           return self.stagefirst * 1.0

       # ATTN:  Handle case of TWO or more element heaps!
       median = None

       # ATTN:  split the difference for equal partitions
       if (lowerLen == upperLen):
           # ATTN:  use DECIMAL to get non-truncating division
           median = (self.maxheap[0] + self.minheap[0])/2.0
       # ATTN:  odd one out is the median
       elif (lowerLen < upperLen):
           # ATTN: no need for PEEK, as 0th element is one to use!
           median = self.minheap[0] * 1.0
       else:
           median = self.maxheap[0] * 1.0

       return median

def main(args):

    print ("WELCOME TO RUNNING MEDIAN!")

    mockStream1 = [1, 2, 3]
    rmdriver1 = RunningMedian()
    # rmdriver1.init(mockStream1[0], mockStream1[1])
    rmdriver1.addNewItem(mockStream1[0])
    rmdriver1.addNewItem(mockStream1[1])
    rmdriver1.addNewItem(mockStream1[2])
    runningMedian = rmdriver1.getMedian()
    print "MEDIAN 1.0:  {0}".format(runningMedian)

    mockStream2 = [1, 2, 3, 4]
    rmdriver2 = RunningMedian()
    # rmdriver2.init(mockStream2[0], mockStream2[1])
    rmdriver2.addNewItem(mockStream2[0])
    rmdriver2.addNewItem(mockStream2[1])
    rmdriver2.addNewItem(mockStream2[2])
    runningMedian = rmdriver2.getMedian()
    print "MEDIAN 2.0:  {0}".format(runningMedian)
    rmdriver2.addNewItem(mockStream2[3])
    runningMedian = rmdriver2.getMedian()
    print "MEDIAN 2.1:  {0}".format(runningMedian)

    mockStream3 = [6, 12, 4, 5, 3, 8, 7]
    rmdriver3 = RunningMedian()
    # rmdriver3.init(mockStream3[0], mockStream3[1])
    rmdriver3.addNewItem(mockStream3[0])
    rmdriver3.addNewItem(mockStream3[1])
    rmdriver3.addNewItem(mockStream3[2])
    runningMedian = rmdriver3.getMedian()
    rmdriver3.addNewItem(mockStream3[3])
    runningMedian = rmdriver3.getMedian()
    rmdriver3.addNewItem(mockStream3[4])
    rmdriver3.addNewItem(mockStream3[5])
    rmdriver3.addNewItem(mockStream3[6])
    runningMedian = rmdriver3.getMedian()
    print "MEDIAN 3.0:  {0}".format(runningMedian)

# invocation of LIVE data input!
# NOTE:  DIRECTLY from CTCI skeleton for reading inputs
# - total number of entries in stream
# - enter a number on each line
# OUTPUT - calculates "running" median!
# TODO: figure out if wasteful to append to LIST each time?
def loadDataPoints():

    n = int(raw_input().strip())
    a = []
    a_i = 0
    for a_i in xrange(n):
        a_t = int(raw_input().strip())
        a.append(a_t)

    return a

def debugDump(rmdriver):

    # DEBUGGING
    # ATTN:  http://stackoverflow.com/questions/15769246/pythonic-way-to-print-list-items
    print ("===")
    print "*"
    for p in rmdriver.minheap: print p
    for p in rmdriver.maxheap: print p
    print "*"


def runDataPoints(mockStream):

    rmdriver = RunningMedian()

    for i in range(0, len(mockStream)):
        rmdriver.addNewItem(mockStream[i])
        # debugDump(rmdriver)
        runningMedian = rmdriver.getMedian()
        print "{0}".format(runningMedian)



# NOTE:  NOT executed on IMPORT!
if __name__ == '__main__':

    # ATTN:  invocation of GLOBAL method as TEST driver
    # main(sys.argv)

    # ATTN:  run ACTUAL driver script
    dataPoints = loadDataPoints()
    runDataPoints(dataPoints)




