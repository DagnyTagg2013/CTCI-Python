
from collections import deque

# PYTHON:
# https://pymotw.com/2/collections/deque.html

# MIN DEPTH:
# http://www.geeksforgeeks.org/find-minimum-depth-of-a-binary-tree/

# MAX DEPTH:
# http://www.geeksforgeeks.org/write-a-c-program-to-find-the-maximum-depth-or-height-of-a-tree/

class Node:

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


# building a Tree
#
#       1
#      / \
#     2   3
#    / \
#   4   5
#

# ATTN: assume FULL BINARY TREE (not SEARCH-TREE) and order LEFT before RIGHT in BFS!
treeData  = [None,1,2,3,4,5]

# ATTN: OK to do recursion here as non-overlapping
# ATTN: check EMPTY and one-node case!
# ATTN: take MAX, then ADD one!

def loadTree(treeData):

    bfsQ = deque()
    root = Node(treeData[1])
    bfsQ.append(root)

    # ATTN:  Pythonic way to check if Q
    scanIdx = 1
    dataEnd = len(treeData) - 1
    while bfsQ and (scanIdx < dataEnd):
        # FIFO to retrieve,then append next children
        levelRoot = bfsQ.popleft()
        scanIdx += 1
        levelRoot.left = Node(treeData[scanIdx])
        scanIdx += 1
        levelRoot.right = Node(treeData[scanIdx])
        # ATTN:  ADD children nodes to FIFO Q to navigate to NEXT sub-level of EACH node correctly
        bfsQ.append(levelRoot.left)
        bfsQ.append(levelRoot.right)

    return root

treeRoot = loadTree(treeData)

# ATTN:  DFS Tree Traversal w Stack!
"""
def printContents(currNode):

    if currNode is None:
        print "None\n"
        return

    if currNode is not None:
        print '{0}'.format(currNode.key)

    if currNode.left is not None:
        printContents(currNode.left)

    if currNode.right is not None:
        printContents(currNode.right)
"""

def printContents(currNode):

    dfsStack = deque()
    dfsStack.append(currNode)

    # test the Q not empty!
    while (dfsStack):

        # ATTN:  gets NEXT node in FIFO DFS order to traverse!
        currNode = dfsStack.pop()

        if currNode is None:
            print "None\n"

        if currNode is not None:
            print '{0}'.format(currNode.key)

        # ATTN:  stores  nodes for next-level traversal; take LEFT last, then pops LEFT first
        if currNode.right is not None:
            dfsStack.append(currNode.right)

        if currNode.left is not None:
            dfsStack.append(currNode.left)

print "TREE CONTENTS:"
printContents(treeRoot)

# TRICK:  check None, recur OTHER side and add one for current level
def minDepth(node):

    # ATTN: EMPTY CASE
    if node is None:
        return 0

    # ATTN:  ROOT case
    if node.left is None and node.right is None:
        return 1

    # If left subtree is Null, recur for right subtree
    if node.left is None:
        return minDepth(node.right)+1

    # If right subtree is Null , recur for left subtree
    if node.right is None:
        return minDepth(node.left) +1

    return min(minDepth(node.left), minDepth(node.right))+1

print "MIN Depth is:  {}".format(minDepth(treeRoot))


# TRICK:  check None, recur OTHER side and add one for current level
# Compute the "maxDepth" of a tree -- the number of nodes
# along the longest path from the root node down to the
# farthest leaf node
def maxDepth(node):

    # ATTN: EMPTY CASE
    if node is None:
        return 0

    # ATTN:  ROOT only case
    if node.left is None and node.right is None:
        return 1

    else:

        # Compute the depth of each subtree
        lDepth = maxDepth(node.left)
        rDepth = maxDepth(node.right)

        # ATTN:  use the larger one, then add for current level
        if (lDepth > rDepth):
            return lDepth+1
        else:
            return rDepth+1

print "MAX Depth is:  {}".format(maxDepth(treeRoot))