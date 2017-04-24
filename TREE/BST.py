
# TODOs:
# - get depth

# ORIGINAL TREE:
#      2
#     / \
#    1   3
#         \
#          4

# ATTN: ALGO
# - PREORDER SERIALIZE-DESERIALIZE with SENTINEL-MARKER character for NULL!
# - http://codereview.stackexchange.com/questions/149617/serialize-and-deserialize-binary-tree
# ATTN:  list extension
# - http://stackoverflow.com/questions/252703/append-vs-extend
# ATTN:
# Python collection for deque!
# - https://docs.python.org/2.6/library/collections.html
# - http://stackoverflow.com/questions/5652278/python-2-7-how-to-check-if-a-deque-is-empty
# - http://stackoverflow.com/questions/9289614/how-to-put-items-into-priority-queues
# ATTN:
# Python static class methods!
# - http://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python
#
# ATTN:
# Multiple CTORs in Python!
# - http://stackoverflow.com/questions/2164258/multiple-constructors-in-python
from collections import deque

# ATTN
# - support for Python Exception stacktrace
# import traceback
import logging

# FOUNDATIONS:
# - https://en.wikipedia.org/wiki/Binary_search_tree
#
# ATTN:  Python Deep Copy vs Copy!
# - http://stackoverflow.com/questions/3975376/understanding-dict-copy-shallow-or-deep/3975388#3975388

# ATTN:  Python Underscores!
# - http://stackoverflow.com/questions/1301346/what-is-the-meaning-of-a-single-and-a-double-underscore-before-an-object-name

# ATTN:  Explanation of deque
# - https://docs.python.org/2.6/library/collections.html

# ATTN:  def and __init__ sufficient for class elements declaration
class Node:

    # ATTN:
    # - remember __ for ctor
    # - remember self
    # - OK to just reference self elements for declaration
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    @staticmethod
    def createNodeFromSubtrees(key, value, leftSubtree, rightSubtree):

        freshNode = Node(key, value)
        freshNode.left = leftSubtree
        freshNode.right = rightSubtree

        return freshNode

# ATTN:  class and classname
class BST:

    def __init__(self):
        self.head = None

    # ATTN:  syntax for recursive calls
    # - add self argument to reference within instance
    # - must use def keyword and colon
    # - handle EMPTY case
    # - must invoke with self. but then only pass in args AFTER implicit self firstarg!
    # ATTN:  this is OK recursion as ELIF TAIL recursion decomposes to LOOP
    def rsearch(self, currNode, keyToFind):

        # ATTN:  handle EMPTY and EQUALs EXIT case
        if (currNode == None) or (currNode.key == keyToFind):
            return currNode
        elif (keyToFind < currNode.key):
            return self.rsearch(currNode.left, keyToFind)
        else:
            return self.rsearch(currNode.right, keyToFind)

    # ATTN:  iterative search
    def isearch(self, keyToFind):

        # ATTN:  initialize FOUND Node
        foundNode = None
        currNode = self.head

        # ATTN:  OPPOSITE of EXIT condition!
        while (currNode is not None) and (currNode.key != keyToFind):
            if (keyToFind < currNode.key):
                currNode = currNode.left
            else:
                currNode = currNode.right

        # ATTN:  TEST END OF WHILE CONDITION!
        if (currNode is not None) and (currNode.key == keyToFind):
                foundNode = currNode

        return foundNode

    # ATTN:  insert data
    # ATTN:  RETURN of currNode, ASSIGNED to LEFT or RIGHT
    def _rinsert_(self, currNode, key, value):

        # ATTN:  RETURN on BASE EXIT case!
        if (currNode == None):
            #ATTN: call to method JUST uses key, value
            currNode = Node(key, value)
            return currNode

        if (key < currNode.key):
            currNode.left = self._rinsert_(currNode.left, key, value)

        elif (key > currNode.key):
            currNode.right = self._rinsert_(currNode.right, key, value)

        else:  # equals case
            print "ABORTING INSERT: as DUPLICATE key is not permitted\n"

        # ATTN:  return node at the end!
        return currNode

    def insert(self, key, value):

        self.head = self._rinsert_(self.head, key, value)

    # ATTN:  Print BST Contents
    def _rPrintContents_(self, currNode):

        if currNode is None:
            print "None\n"
            return

        if currNode is not None:
            print '{0}:{1}'.format(currNode.key, currNode.value)

        if currNode.left is not None:
            self._rPrintContents_(currNode.left)

        if currNode.right is not None:
            self._rPrintContents_(currNode.right)

    def printContents(self):

        self._rPrintContents_(self.head)

    # ATTN: what's in queue at any time is NEXT in Z-TRACE BFS traversal
    def bfs(self):

        # ATTN: initialize FIFO queue with HEAD
        queue = deque()
        queue.append(self.head)
        currNode = self.head

        # ATTN:  REMOVE node first to process; then add its LEFT, RIGHT to Q!
        # ATTN:  Run until queue is EMPTY; note syntax for EMPTY is just TRUE-FALSE!
        while (queue):

            currNode = queue.popleft() #ATTN:  popleft removes element from FRONT of queue!
            print "{0:1}, ".format(currNode.key, currNode.value)

            #ATTN:  check for None before dereference, note SYNTAX!
            if (currNode.left is not None):
                queue.append(currNode.left)

            if (currNode.right is not None):
                queue.append(currNode.right)

    # ATTN: what's in stack at any time is NEXT in DEFTH-FIRST PRE-ORDER traversal!
    def dfs(self):

        #  **********
        #  ATTN:  FIFO from SAME-SIDE, and most efficient on RIGHT side NOT LEFT!

        stack = deque()
        # ATTN:  appendLeft is equivalent to PUSH onto stack!
        #        need to START with HEAD!
        stack.append(self.head)
        currNode = self.head

        # ATTN:  REMOVE node first to process; then add its LEFT, RIGHT to Q!
        while (stack):

            currNode = stack.pop()
            print "{0:1}, ".format(currNode.key, currNode.value)

            if (currNode.left is not None):
                stack.append(currNode.left)

            if (currNode.right is not None):
                stack.append(currNode.right)

    # ATTN:  PUBLIC, non-recursive call with HEAD!
    def serialize(self, sentinel = '#'):

        return self._rserialize_(self.head, sentinel)


    # ATTN1:  SERIALIZING using PRE-ORDER:  ROOT, LEFT, RIGHT;
    #         - since need to access ROOT prior to attaching LEFT, RIGHT
    # ATTN2:  check for NULL
    # ATTN3:  use KEY for values to save
    def _rserialize_(self, currNode, sentinel = '#'):

        # CASE1:  INITIALIZE ROOT first
        # ATTN:  init with ROOT, and use , for ITERABLE!
        serialized = [currNode.key, ]

        # CASE2:  LEFT, but test for NULL first before recursing!
        if currNode.left is None:
            serialized.append(sentinel)
        else:
            # ATTN:  recursive invocation on instance method with SELF!
            serialized.extend(self._rserialize_(currNode.left, sentinel))

        # CASE3:  RIGHT, but test for NULL first before recursing!
        if currNode.right is None:
            serialized.append(sentinel)
        else:
            serialized.extend(self._rserialize_(currNode.right, sentinel))

        return serialized

    # ATTN0:  DESERIALIZE using PRE-ORDER: ROOT (save), LEFT, RIGHT, (reconstruct on ROOT)
    # - since have to NAV down before enough info to get subtrees to attache to root
    # ATTN1:  need to specify class static method as instance not created yet!
    # ATTN2:  need to create instance by invoking class CTOR!
    # ATTN3:  need to RETURN TUPLE w latest constructed SUB-ROOT, and NEXT scanIndex
    @staticmethod
    def deserialize(data, sentinel = '#'):

        maxDataIdx = len(data) - 1

        # ATTN:  nested sub-helper function in function which uses data from ENCLOSING function!
        def rdeserialize(scanIndex):

            # CASE1:  handle the None case, increment scan pointer
            if data[scanIndex] == sentinel:
                return (None, (scanIndex + 1))
            else:
                # ATTN:  CACHE ROOT value FIRST, as LATER scanIndex will be advanced thru serialized string!
                cached_level_root_val = data[scanIndex]

            # CASE2:
            # ATTN:  PRE-validate BEFORE recursing that you have data left
            if (scanIndex < maxDataIdx):
                leftSubtree, scanIndex = rdeserialize((scanIndex + 1))

            # CASE3:
            # ATTN:  note how input scanIndex is OUTPUT from ABOVE after
            #        returning with depth-first traversal index offsets!
            # ATTN:  PRE-validate BEFORE recursing that you have data left
            if (scanIndex <= maxDataIdx):
                rightSubtree, scanIndex = rdeserialize(scanIndex)

            # CASE4:  NOW have enough info to construct the ROOT at this level via ctor!
            #         INITIALIZE value to same as key!
            return ( Node.createNodeFromSubtrees(cached_level_root_val, cached_level_root_val, leftSubtree, rightSubtree),
                     scanIndex)

        # ATTN: like MAIN script calling into SUB-FUNCTION!
        headNode = None
        builtTree = None
        lastScanIndex = None
        (headNode, lastScanIndex) = rdeserialize(0)
        builtTree = BST()
        builtTree.head = headNode
        return builtTree


# NOTE: main Driver script for method calls
bst = BST()
bst.insert(2, "B")
bst.insert(1, "A")
bst.insert(3, "C")
bst.insert(4, "D")

# print "\nACTUAL BST CONTENTS HERE:"
# bst.printContents()

# foundNode = bst.isearch(4)
# print "\nFOUND NODE:  {0:1}".format(foundNode.key, foundNode.value)

# notFoundNode = bst.isearch(9)
# print "\nNOT FOUND NODE:  {0}".format(notFoundNode)

# print "\nBFS CONTENTS:  \n"
# bst.bfs()

print "\nSERIALIZED BST:\n"
serialized = bst.serialize('#')
#ATTN:  print contents of integer list!
print str(serialized).strip('[]')

print "\nDESERIALIZED BST:\n"
freshTree = BST.deserialize(serialized, '#')
# ATTN:  SERIALIZE-DESERIALIZE-SERIALIZE should RECOVER original tree!
print type(freshTree)
serialized = freshTree.serialize('#')
print str(serialized).strip('[]')

# ATTN:  how to handle exceptions!
try:

    print "\nDFS CONTENTS:  \n"
    bst.dfs()

except Exception as ex:

    # ATTN:  Python print stack trace
    # traceback.print_exc()
    logging.exception("WTF?!")





