
import logging

# Build an N-Tree from 2D array of Parent-Child pairs

"""

   TREE:

            3
          / | \
        4   5  6
           / \
          7   8
         /
        9


    ALGO:

       - ASSOCIATIVE MAP; ACCUMULATING EDGEs per Parent node!
         KEY value => Node
         ** need ROOT and CHILD nodes to LOOKUP CHILD as ROOT of NEXT-LEVEL tree down!
       - WALK up from ANY EDGE to LOOKUP PARENT where Node.Parent == None
         to find ROOT of tree
       - DEPTH-WALK is similar; and O(logN)

"""

class Node:

    # ATTN:
    # - remember __ for ctor
    # - remember self
    # - OK to just reference self elements for declaration
    # - MULTIPLE nodes, so LIST
    def __init__(self, key, parent = None):
        self.key = key
        self.children = []
        self.parent = parent

    def addChild(self, key):
        self.children.extend([key])


def buildTree(data):

    if (len(data) == 0):
        raise ValueError("Input data must be non-empty!")

    accumMap = {}

    # NOTE:  accumulate EDGES for each level ROOT; via adding BOTH vertices of given EDGE-PAIR in 2D array to the Map!
    for edge in data:

        # ATTN:  to protect against KeyError, provide DEFAULT NONE
        # LOOKUP ROOT,
        # - if not exists, then add KEY to NODE value Map
        # - if exists, then add CHILD to NODE
        # LOOKUP CHILD,
        # - if not exists, then add KEY to NODE value Map
        # - if exists, do nothing; as this edge ENDs at this CHILD, and we have no info to lower-level grandchildren at this point
        # => NEW CHILD
        rootAccumEdges = accumMap.get(edge[0], None)
        if (rootAccumEdges is None):
            newParent = Node(edge[0])
            accumMap[edge[0]] = newParent
            rootAccumEdges = newParent
        rootAccumEdges.addChild(edge[1])

        # ATTN:  passes DEFAULT value, otherwise KeyError if not found!
        subRootAccumEdges = accumMap.get(edge[1], None)
        if (subRootAccumEdges is None):
            # NOTE:  set PARENT from above
            newChild = Node(edge[1], newParent)
            accumMap[edge[1]] = newChild

    # pick first Level root, ten track to OVERALL Tree ROOT
    # - http://stackoverflow.com/questions/30362391/how-to-find-first-key-in-a-dictionary
    # nextLevelRoot = next(iter(accumMap)).

    #ATTN:  pickup FIRST ROOT here!
    allKeys = accumMap.keys()
    nextRootUp = accumMap[allKeys[0]]

    while nextRootUp is not None:
        # ATTN:  need this to get prior node to END NONE
        trailRootUp = nextRootUp
        nextRootUp = nextRootUp.parent
    globalRoot = trailRootUp

    return globalRoot

# **************** DRIVER to test tree build ***************
try:

    testData1 = [[1,2]]
    rootTree1 = buildTree(testData1)

    testData2  = [[5,7], [3,6], [7,9], [3,4], [5,8], [3,5]]
    rootTree2 = buildTree(testData2)

    # testData3 = []
    # rootTree3 = buildTree(testData3)

except Exception as ex:

    logging.exception(ex)



