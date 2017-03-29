

#
# DISCLAIMER:  This WAS A HOME-TEST JUST FOR PRACTICE-REVIEW-LEARNING
# - FOUND THIS on Dynamic-Programming to avoid EXPONENTIAL TIME COMPLEXITY EXPLOSION OF RECURSIVE approach:
#   http://www.geeksforgeeks.org/count-possible-paths-top-left-bottom-right-nxm-matrix/
# - ALGO
# - num paths to each cell from origin is calculated by SUM of num path FROM adjacent cells LEFT and ABOVE
# - SO CACHE pathcounts, building INCREMENTALLY; initialize 1st row, 1st col to 1's -- only ONE path to get to ORIGIN
# - This SEED from 1st row and column count of 1 are used to calculate the TARGET CELL numpaths as the SUM of ways to get FROM ADJACENT cells
#
import sys
import numpy
# import copy
import traceback

"""
DEPRECATED RECURSIVE IMPLEMENTATION:  (recurse from FAR end of GRID, and TERMINATE at ORIGIN)  SUPER-BAD EXPONENTIAL COMPLEXITY

// Returns count of possible paths to reach cell at row number m and column
// number n from the topmost leftmost cell (cell at 1, 1)
int  numberOfPaths(int m, int n)
{
   // If either given row number is first or given column number is first
   if (m == 1 || n == 1)
        return 1;

   // If diagonal movements are allowed then the last addition
   // is required.
   return  numberOfPaths(m-1, n) + numberOfPaths(m, n-1);
           // + numberOfPaths(m-1,n-1);
}

"""

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
    """
    def __init__(self, openGrid=None):
        # ATTN:  SHAPE to get dimensions!
        (self.ROWS, self.COLS) = openGrid.shape
        # ATTN:  DEEP copy!
        self.OPEN = copy.deepcopy(openGrid)
    """

    # DP-building pathcount from ORIGIN out to MAX point
    # WANT THIS vs RECURSION on
    # def buildPathCount(self, openGrid):
    def buildPathCount(self, openGrid):

        # ATTN:  SHAPE to get dimensions!
        (ROWS, COLS) = openGrid.shape

        # initialize pathCountCache
        pathCountCache = numpy.zeros((ROWS, COLS))

        # initialize FIRST COLUMN across ALL rows with 1s; as numpaths from origin to any point on first column is 1
        for r in range(0, ROWS):
            # ATTN: IFF current point is on a BLOCKED spot; FORCE its in-place pathcount to 0 as THIS spot CANNOT be on a valid path!
            if (openGrid[r,0] == 0):
                pathCountCache[r,0] = 0
            else:
                pathCountCache[r,0] = 1

        # initialize FIRST ROW across ALL cols with 1s; as numpaths from origin to any point on first row is 1
        # ATTN:  Python RANGE goes to one-less LAST COL!
        for c in range(0, COLS):
            # ATTN: IFF current point is on a BLOCKED spot; FORCE its in-place pathcount to 0 as THIS spot CANNOT be on a valid path!
            if (openGrid[0,c] == 0):
                pathCountCache[0,c] = 0
            else:
                pathCountCache[0,c] = 1

        # BUILDING current count from ADJACENT cells from MAX points BACK to ORIGIN; incl DIAGONAL adjacency
        # START OFFSET from FIRST COL, and ROW
        for r in range(1, ROWS):
            for c in range(1, COLS):
                # ATTN: IFF current point is on a BLOCKED spot; FORCE its in-place pathcount to 0 as THIS spot CANNOT be on a valid path!
                if (openGrid[r,c] == 0):
                     pathCountCache[r,c] = 0
                else:
                    # ATTN:  Building result from ADJACENT counts, directly ABOVE, directly LEFT
                    pathCountCache[r,c] = pathCountCache[r-1,c] + pathCountCache[r,c-1]
                    # ATTN:  MAY PERMIT DIAGONAL PATH; ONLY on PRIMARY DIAGONAL from ORIGIN
                    if ((r-1) == (c-1)):
                        pathCountCache[r,c] += pathCountCache[r-1,c-1]


        # at this point, FINAL MAX POINT COUNT is calculated
        return pathCountCache[(ROWS - 1), (COLS - 1)]


if __name__ == '__main__':

    # opengrid = numpy.matrix([[1,1], [0,1]])
    opengrid = numpy.matrix([[1,1,1,1], [1,1,1,1], [1,1,1,1]])
    # TODO:  feed from readInput()
    # opengrid = readInput()

    try:
        # driver = MatrixPathsWBlocks(opengrid)
        numPaths = MatrixPathsWBlocks().buildPathCount(opengrid)
        print "FINAL PATHCOUNT is:  {0}\n".format(numPaths)

    except Exception as ex:
        traceback.print_exc(ex)

