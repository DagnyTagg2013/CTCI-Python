
import sys

# TODO:  run test on this!

# Node is defined as
class node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

"""
CAVEAT:  NOT sufficient to check that within ONE given level; this property holds, for successive levels
This instead must hold ACROSS ALL levels for left and right subtrees:
eg the following is not a BST since 4 > 3.

            3
           / \
          2   5
         / \
        1   4
        KEY:
        - must track STACK-STATE-NARROWING RANGEs!
        - INT_MAX = 4294967296
        - INT_MIN = -4294967296
        ATTN:
        - Python test for null is "not xxx"
        - NEED TO MODIFY INSERT to support RECORDING MIN and MAX on tree!
        DATA:
        - min, max, SIZE of subtree incl this node
        EXIT:
        - null or 1-node  case, return TRUE
        TEST:
        - current node value is NOT > MIN, < MAX, return FALSE
        - recurse on LEFT child; is BST between MIN on THIS parent node, and this parent node's root value
        - AND recurse on RIGHT child; is BST between THIS parent node value, and MAX
"""
# returns BOOLEAN
# TODO:  test if should be doing this with WHILE-ITERATION loop?
# TODO:  When is it OK to use Recursion; NOT THIS case as EXP (NOT TAIL RECURSION)
def rIsBST(current, min, max):

    # EXIT CASE:  test for NULL or SINGLE-NODE case!
    # ATTN:  note Python test for null is 'is not None' or 'is None'
    if (       (current == None)
            or ((current.left is None) and (current.right is None))):
        return True


    # test for immediate BST-property violations!
    if ((current.data < min)  or (current.data > max)):
        return False

    # ATTN:  test for NULL FIRST!!!
    # ATTN:  NARROW range +-1 RELATIVE to current.data!
    isLeftBST = (current.left is None) or ( (current.left is not None) and rIsBST(current.left, min, current.data - 1))
    isRightBST = (current.right is None) or ( (current.right is not None) and rIsBST(current.right, current.data + 1, max))

    # test for RECURSIVE SUBTREE property validation on sub-range!
    return isLeftBST and isRightBST

# ATTN:  calls into RECURSIVE with INITIAL MAX and MIN int values for Python
def check_binary_search_tree_(root):

    return rIsBST(root, -(sys.maxint - 1), sys.maxint)

# TODO:  need to construct tree to test against; but this is in STUBBED code somwhere!