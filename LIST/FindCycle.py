
# PROBLEM:
# - find a CYCLE in a LinkedList, then correct it!

# CHEAT:
# - http://www.geeksforgeeks.org/detect-and-remove-loop-in-a-linked-list/

# ALGO 1:
# - assume list of KNOWN length; UNIQUE values
# - use LIST-ARRAY lookup to save VISITED node reference by REFERENCE
# - on traversing list; if FOUND visited, then CYCLE found!
#
# ALGO 2:
# - can use FAST/SLOW pointer and if they MEET, then CYCLE detected!
# - MEET point is ANYWHERE on loop; so set VISITED then SCAN pointer to scan until VISITED reached to COUNT elements in loop
# - tp FIND START of loop; set ptr1 to head; ptr2 to head + COUNT to be on loop;
#   move BOTH to SCAN one-at-a-time at the SAME pace,
#   they will meet at START of LOOP i.e. where ptr->next == ptr1
# - get pointer to LAST node, in loop; setting scan ptr to FIXED ptr at START of loop and scanning until NEXT equals that START

class Node:

    # ATTN:  def on Python ctor with self reference!
    def __init__(self, data):
        self.value = data
        self.next = None


# ATTN:
# - use HEAD# ATTN:  i
class LinkedList:

      # ATTN:  init EMPTY list
      def __init__(self):
        self.head = None


def loadList(values):

    # ATTN:  init list HEAD with FIRST node
    # ATTN:  init PRIOR pointer to FIRST node
    newList = LinkedList()
    priorNode = Node(values[0])
    newList.head = priorNode
    for i in range(1,len(values)):
        newNode = Node(values[i])
        #ATTN:  link the nodes!
        priorNode.next = newNode
        #ATTN:  iterate scan pointer!
        priorNode = newNode

    return newList

def hasCycle(linkedList):

    # ATTN:  THIS is the TRICK!
    #        lookup by node REFERENCE!
    visited = {}
    currNode = linkedList.head

    # ATTN:  indicator that cycle detected
    cycleDetected = False

    while (currNode != None):

        isVisited = visited.get(currNode, None)

        #ATTN: test for None!
        if isVisited is None:
            visited[currNode] = True
        else:
            cycleDetected = True
            break

        currNode = currNode.next

    return cycleDetected


# DRIVER test script
# values = [1,5,3,2,10]
# aList = loadList(values)

# TEST 1: empty list
test1 = LinkedList()
result1 = hasCycle(test1)
print "Found Cycle1:  {0}".format(result1)

# TEST 2:
# three nodes, cycle 3 back to 2
test2 = LinkedList()
test2.head = Node(1)
test2.head.next = Node(2)
twoPtr = test2.head.next
test2.head.next.next = Node(3)
test2.head.next.next.next = twoPtr
result2 = hasCycle(test2)
print "Found Cycle2:  {0}".format(result2)
