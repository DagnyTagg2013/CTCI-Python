
"""

PROBLEM:

GIVEN:
- 2 strings

FIND:
- length of longest common sequence
- actual common sequence
- order matters
- match in letter and occurrences
- letters don't need to be contiguous

EXAMPLE:

ABCDGH, AEDFHR => 3, ADH
AGGTAB, GXTXAYB => 4, GTAB

INFO:  THIS IS BASIS for DIFF ALGO
- https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
- http://www.algorithmist.com/index.php/Longest_Common_Subsequence

TODO: find longest common sub-STRING; where ORDER DOES matter
TODO:  DUNNO about TREE representation here!
https://en.wikipedia.org/wiki/Longest_common_substring_problem

TODO: find the min DISTANCE between two strings
TODO: translation for insert vs remove?
http://www.geeksforgeeks.org/dynamic-programming-set-5-edit-distance/

"""

"""

TODO:  explain the following Time Complexity
SUPERBAD ALGO:
- generate 2expN subsequences for subsets of N items choose/not choose
- do N x M comparisons to test match across each
- OVERRIDING O(EXP N)

TODO:  explain following Time Complexity
RECURSIVE ALGO:
- START from END point in comparison grid
- TEST if equal, add ONE to the length count RETURNED from invoking count on diagonal substring
- OTHERWISE, take MAX of ADJACENT comparison counts

BETTER ALGO: is O(MN)
- REUSE subproblems
- GRID from 0 (empty string) to N on with axis for number of chars from Input String to consider
  2D is for cross-comparison between these two strings
- each element of Grid represents COUNT of matching chars in ADJACENT subsequences
- START from ORIGIN; and compare strings to determine whether to ADD to count from ADJACENT totals!

GET SUBSTRING:
- BUILD longest substring, walking through table count above RECURSIVEly FROM END point in comparison grid
  - DEPTH-FIRST call RECONSTRUCT on diagonal and ADD current contribution (X-1 for index position with 0-offset)
  - if EQUALITY, add one character to DIAGONAL backtrack
  - otherwise, just navigate BACKWARDs towards position with LARGEST common character count, UNTIL == condition is met
  - EXIT at ORIGIN

ATTN PYTHON TRICK for 2D matrix;
- can simulate with DICTIONARY indexed by TUPLE
- otherwise PREFER numpy MATRIX
- http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python
ATTN PYTHON TRICK to pre-init 2D array
w, h = 8, 5;
Matrix = [[0 for x in range(w)] for y in range(h)]

ATTN PYTHON TRICK string concat:
- http://stackoverflow.com/questions/1316887/what-is-the-most-efficient-string-concatenation-method-in-python

"""

# COMPUTE LENGTH of largest common string
def getLongestCommonString(x, y):

    n = len(x)
    m = len(y)

    # KEY POINT:  Build Count of Longest common String
    # TRICK!  Use dict as 2D Array!
    cross = {}

    # NOTE:  add one for 0 empty-set placeholder!
    for i in xrange(n + 1):
        for j in xrange(m + 1):
            if ((i == 0) or (j == 0)):
                # NOTE:  initialize FIRST ROW, FIRST COL with 0s
                cross[i, j] = 0
            # NOTE:  roll FORWARD SUM and INCREMENT from prior adjacent diagonal;
            # where SKIPPED nonmatching interim characters is OK and just adds 0
            elif x[i-1] == y[j - 1]:
                cross[i, j] = cross[i-1, j-1] + 1
            else:
                # NOTE: roll FORWARD, MAX of prior adjacent counts
                cross[i, j] = max(cross[i-1, j], cross[i, j-1])


    # GENERATE ACTUAL common string list of chars from BACKWARDS from MAXPOINT navigation of table count above!
    # NOTE:  Python trick to have sub-closure-function REFER to cross dictionary already defined Above!
    # NOTE:  may need REVERSE final string!
    # ATTN:  OK to have TAIL recursion via ONE ELIF statement as this denegerates to LOOP!
    def genCommonString(i, j):

        # ATTN:  exit base case!
        if i == 0 or j == 0:
            # ATTN:  init with LIST for fast EXTEND
            return []
        elif x[i-1] == y[j-1]:
            # ATTN, need to EXTEND via PRIOR DIAGONAL using + with SEQUENCED [] X char
            # ATTN:  use EXTEND on SEQUENCE via [] instead of APPEND on element
            return genCommonString(i-1, j-1) + [x[i-1]]
        # ATTN, navigate to MAX item!
        elif cross[i-1, j] > cross[i, j-1]:
            return genCommonString (i-1, j)     # TODO:  index out of bounds bug here; what if first elements in sequences arent equal
        else:
            return genCommonString(i, j-1)

    # ATTN:  construct string from List elements quickly
    return ''.join(genCommonString(n, m))

# DRIVER code

# TEST 1: same lengths
x = "ABCDGH"
y = "AEDFHR"
z1 = getLongestCommonString(x, y)
print z1

# TEST 2: differing lengths
x = "AGGTAB"
y = "GXTXAYB"
z2 = getLongestCommonString(x, y)
print z2

# TODO:  try EMPTY string
