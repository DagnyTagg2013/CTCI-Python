
# matrix:  M rows, N columns
# blocked:  0 is blocked 1 is OK
# moves:  ONE right or ONE down
# path endpoints:  from (0,0) to (m-1, n-1)
# input1:  3 4
#         1 1 1 1
#         ...
#         => 10
# input2:  2 2
#          1 1
#          0 1
#         => 2
# FIND:  number of Paths == return mod(10exp9)
# ************
# INFO:  number of paths:  http://www.geeksforgeeks.org/count-possible-paths-top-left-bottom-right-nxm-matrix/
#         so start with 1st row, 1st col -- only ONE path to get to ORIGIN
#         this SEED is used to calculate then the TARGET CELL numpaths as the SUM of ways to get to ADJACENT cells
# ATTN:  __init__.py is used to designate a PACKAGE in Python!
import sys
import numpy
import copy
import traceback

# GLOBAL function; BEFORE class definition!
# ATTN:  Python Functions
# - https://www.tutorialspoint.com/python/python_functions.htm
# ATTN:  calling GLOBAL vs CLASS modules in Python SCRIPT; need to define PRIOR to invocation!
# - http://stackoverflow.com/questions/9455111/python-define-method-outside-of-class-definition
# - http://stackoverflow.com/questions/12691949/defining-a-global-function-in-a-python-script
# - http://stackoverflow.com/questions/27930038/how-to-define-global-function-in-python
def readInput():

    print "Enter matrix dimensions!"

    # ATTN:  cast to int!
    maxrows, maxcols = map(int, sys.stdin.readline().split(' '))
    print "MAX ROWS {0}, MAX COLS {1}\n".format(maxrows, maxcols)

    # ATTN initial space allocation!
    # allocate space here!
    matrix = numpy.ones((maxrows, maxcols))

    print "Enter matrix data by SPACE-SEP integer rows!!"
    for i in range(0, maxrows):
        row_data = list(map(int, sys.stdin.readline().split(' ')))
        for j in range(0, maxcols):
            matrix[i][j] = row_data[j]

    print "\nMATRIX:  \n"
    print matrix
    print "\n"

    return matrix


class MatrixPathsWBlocks:
    # instance method, ctor
    # http://stackoverflow.com/questions/1495666/how-to-define-a-class-in-python
    def __init__(self, openGrid=None):
        # ATTN:  SHAPE to get dimensions!
        (self.ROWS, self.COLS) = openGrid.shape
        # ATTN:  DEEP copy!
        self.OPEN = copy.deepcopy(openGrid)

    # ATTN:  FIRST-PASS; RECURSE FROM END-POSITION at MATRIX to BEGIN, TOWARDS ORIGIN!
	# ATTN:  RETURN TRUE if VALID; OTHERWISE CHAIN-FALSE to EXIT!
    # ATTN:  need to set self for THIS ptr!
    # ATTN:  Python pass-by-value vs pass-by-ref!
    # http://stackoverflow.com/questions/13299427/python-functions-call-by-reference
    # ATTN:  RETURNs TUPLE with True/False validPath, and then CUMULATIVE pathcount ACROSS recursive calls; where CHAINING result!
    # ATTN:  Python calling convention
    # - http://stackoverflow.com/questions/13299427/python-functions-call-by-reference
    # RETURN-VALUE as COMPOSITE elements of AGGREGATE RESULT for SUB-TREEs of decision-tree!
    def recurseCountPathsFromOuterToOrigin(self, x, y, pathTrackPointsList, visitedPointsMap):

        pathCountH = 0
        pathCountV = 0
        pathCountD = 0
        pathCountTotal = 0

        # ie EXIT this DEPTH-FIRST path exploration if BLOCKED point is hit;
        #    SO leave pathCount UNCHANGED!
        # - http://stackoverflow.com/questions/2220968/python-setting-an-element-of-a-numpy-matrix


        # CHECK2:  check if VISITED this point already to get result, so DON'T double-count, and just return prior-saved pathcount result!
        # test dictionary membership!
        #  -http://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
        if (x,y) in visitedPointsMap:
            # ie any path thru this point is DOUBLE-COUNTING, so return UNMODIFIED count of valid paths; and EXIT out of subtrees
            return visitedPointsMap.get((x,y))

        # ATTN:  add current point to pathTracker if valid, non-blocked spot
        # ATTN:  Python List syntax!
        # - http://www.thegeekstuff.com/2013/06/python-list/?utm_source=feedly
        pathTrackPointsList.append((x,y))

        # ATTN: FOUND BASE-TERMINATION CASE, reached ORIGIN, can EXIT, as DEPTH-FIRST to DESTINATION LEAF,
        #       or FOUND PATH to ORIGIN fro ENDPONT!!
        # ATTN:  Python AND op
        # ATTN:  Stack-accumulated ARRAY structure, CANNOT local-modify PRIMITIVE!
        if ((x == 0) and (y == 0)):
            return (True, 1)

        # ATTN:  init CHAIN isFoundPath
        isFoundPath = False

        # ATTN, ensure STEP-DECREMENT to 0 LOWER BOUND OK
        # ATTN:  CHECK for open BEFORE RECURSING -- THEREBY ELIMINATING BAD INVALID SUBTREE possibilities!
        # *** GO UP
        if (x >= 1) and self.OPEN[(x - 1), y]:
            # ie FURTHER depth-first-explore ways we can CHOOSE to branch a different path!
            (isFoundPath, pathCountH) = self.recurseCountPathsFromOuterToOrigin((x - 1), y, pathTrackPointsList, visitedPointsMap)

        # ATTN, using Python AND variables!
        # - http://stackoverflow.com/questions/18195322/pythons-logical-operator-and
        # ATTN, not ELSE, since ADDITIONAL depth-search branch!
        # ATTN,  CHAIN prior NOT-FOUND condition!
        # ATTN, ensure STEP-DECREMENT to 0 LOWER BOUND OK
        # *** GO LEFT
        # ATTN, not and end operators!
        # ATTN:  CHECK for open BEFORE RECURSING -- THEREBY ELIMINATING BAD INVALID SUBTREE possibilities!
        # if not isFoundPath and (y >= 1) and self.OPEN[x, (y - 1)]:
        if (y >= 1) and self.OPEN[x, (y - 1)]:
            # ie FURTHER depth-first-explore ways we can CHOOSE to branch a different path!
            (isFoundPath, pathCountV) = self.recurseCountPathsFromOuterToOrigin(x, (y - 1), pathTrackPointsList, visitedPointsMap)

        # *** GO DIAGONAL
        if (x >= 1) and (y >= 1) and self.OPEN[(x-1), (y-1)]:
            (isFoundPath, pathCountD) = self.recurseCountPathsFromOuterToOrigin((x - 1), (y - 1), pathTrackPointsList, visitedPointsMap)

        # remove Element IFF sub-path not found!
        # http://stackoverflow.com/questions/5844672/delete-an-item-from-a-dictionary
        if (not isFoundPath):
            # REMOVE current bad point option from Depth-Path experiment!
            del pathTrackPointsList[(x,y)]

        # ROLLUP sub-path-counts from higher-level nodes above LEAVES
        pathCountTotal = pathCountH + pathCountV + pathCountD

        # CACHE current point as visited!, in an EASY MAP for lookup!
        # ATTN:  Python Dictionary syntax!
        # - http://www.thegeekstuff.com/2013/06/python-list/?utm_source=feedly
        visitedPointsMap[(x,y)] = (isFoundPath, pathCountTotal)

        return (isFoundPath, pathCountTotal)



# ATTN:  simulate Java, main; executed only in IMPORT!
def main(opengrid):

    # catching exceptions in Python
    # - http://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python

    try:

        cumulativeCounter = MatrixPathsWBlocks(opengrid)

        # START from DEPTH-FIRST path search from Origin (0,0), with PathCount of 0
        # AND pathTracker initialized to LIST of Point tuples (later)
        pathTrackPointsList = []
        visitedPointsMap = {}
        maxCols, maxRows = opengrid.shape
        # ATTN:  CAREFUL that horizontal-X scans across COLs; and vertical-y scans across ROWs!
        (isFoundPath, totalPathCount) = cumulativeCounter.recurseCountPathsFromOuterToOrigin((maxCols - 1), (maxRows - 1), pathTrackPointsList, visitedPointsMap)
        print "FOUND PATH?  {0}; with COUNT:  {1}".format(isFoundPath, totalPathCount)

    except Exception as ex:
        traceback.print_exc(ex)


# ATTN:  this only executes when file executes as a SCRIPT; BUT EVERYTHING ABOVE executes EVERY TIME FILE is imported!
# http://stackoverflow.com/questions/22492162/understanding-the-main-method-of-python
# ATTN:  GLOBAL
# - http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
# NOTE:  need to access GLOBAL namespace!
if __name__ == '__main__':
    # calls GLOBAL function declared ABOVE class from here!
    # opengrid = readInput()

    # ATTN:  Initializing a 2D Array in Python to STUB inputs!
    # - http://stackoverflow.com/questions/4151128/what-are-the-differences-between-numpy-arrays-and-matrices-which-one-should-i-u
    # - http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python
    # TODO:  replace this MOCK input with ACTUAL readInput()

    # **** TEST CASE 1
    opengrid = numpy.matrix([[1,1], [1,1]])

    # **** TEST CASE 2
    # opengrid = numpy.matrix([[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]])

    # NOTE:  main() on LAST line!
    main(opengrid)



# ************** template code for I/O! **************************

"""
f = open(os.environ['OUTPUT_PATH'], 'w')


_a_rows = 0
_a_cols = 0
_a_rows = int(raw_input())
_a_cols = int(raw_input())

_a = []
for _a_i in xrange(_a_rows):
    _a_temp = map(int,raw_input().strip().split(' '))
    _a.append(_a_temp)

res = numberOfPaths(_a);
f.write(str(res) + "\n")

f.close()
"""