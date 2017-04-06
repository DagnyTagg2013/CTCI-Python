
#
# PROBLEM:
# - START at ORIGIN of matrix
#   - SPIRAL path around to centre, not crossing prior path

# TODO:
# - BREAKDOWN problem to move SPIRALLY (translate from my Java intqs airbnb SpiralPretty)

# STEP 1:  MINIMAL TRANSFORM move before having to examine state to decide on NEXT move!
# ATTN:  simple to MODIFY from clockwise to counter-clockwise with this!
# ATTN TRICKY:  MOST GRANULAR currRow, currCol which may move INDEPENDENTLY of Point PAIR! -- AND TEST AGAINST ALREADY-VISITED!
# public Point moveOneSpotInCurrentDirection(Direction d, int currRow, int currCol, Set visitedPoints) {

# STEP 2:  ENCAPSULATE in WHILE to REPEAT steps until NEXT decision!
# public Point moveSeveralPointsUntilBound(Direction d, int currRow, int currCol, Set visitedPoints)

# STEP 3:  ENCAPSULATE DECISION for DIRECTION change
# public Direction changeDirection(Direction currDirection)

# STEP4:  LOOP based on DECISION and SEQUENCE MOVES!
# public Set<Point> moveSpirally() {

# ***** PYTHON SYNTAX *****
# - ATTN:  Java REFLECTION vs Python
# https://www.quora.com/Is-there-an-equivalent-of-Java-reflection-in-Python
# - ATTN:  MATRICES
# - Matrices in Python and NumPy, or even SciKitLearn
# http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python33
# - ATTN:  LAMBDAS
# http://stackoverflow.com/questions/890128/why-are-python-lambdas-useful
# http://stackoverflow.com/questions/29767310/pythons-lambda-with-no-variables
# - ATTN:  Exceptions and Errors
# http://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
# http://stackoverflow.com/questions/5191830/best-way-to-log-a-python-exception
# https://docs.python.org/2/library/exceptions.html

import sys
import numpy
import logging

# ATTN:  global direction
class Direction:
    RIGHT, DOWN, LEFT, UP = range(4)

def readInput():

    print "Enter matrix dimensions!"
    # ATTN:  cast to int!
    maxRows, maxCols = map(int, sys.stdin.readline().split(','))
    # ATTN THIS WON'T work for initial space allocation!

    """
    matrix = []
    for i in range(0, maxRows):
        matrix[i] = list(map(int, sys.stdin.readline().split(',')))
    """

    # allocate space here!
    matrix = numpy.zeros((maxRows, maxCols))

    print "Enter matrix data by CSV integer rows!!"
    for i in range(0, maxRows):
        row_data = list(map(int, sys.stdin.readline().split(',')))
        for j in range(0, maxCols):
            matrix[i][j] = row_data[j]

    print matrix

    return matrix


class Spiraller():

    def __init__(self, maxRows, maxCols):
        self.currRow = 0
        self.currCol = 0
        self.MAX_ROWS = maxRows
        self.MAX_COLS = maxCols

    class Point:

        def __init__(self, x, y):
            self.x = x
            self.y = y

    # ATTN; parameterize function to handle a move in BOTH directions
    def _move(self, deltaX, deltaY):
        self.currCol += deltaX
        self.currRow += deltaY
        return (self.currRow, self.currCol)

    # ATTN:  Quora, Why Python has no switch statement, and implement via Dictionary
    def moveOneSpotInOneDirection(self, direction):

            # ATTN:  SETUP the direction SWITCH simulation via DICTIONARY to lambda function parameterized
            #        by DIRECTION KEY, executing specific move across 2D grid
            # ISSUE:  want to LAZY-EXECUTE, ie ONLY when get is invoked on specific input GET/SWITCH on DIRECTION
            #         SO want to pre-assign lambda function pointer with known input calling params
            moveOptions = {
                            Direction.RIGHT: lambda: self._move(1, 0),
                            Direction.DOWN: lambda: self._move(0, 1),
                            Direction.LEFT: lambda: self._move(-1, 0),
                            Direction.UP: lambda: self._move(0, -1)
                          }

            # ATTN:  get() actually executes the SWITCH!
            calcNextMove = moveOptions.get(direction)
            (nextRow, nextCol) = calcNextMove()

            # NEXT TEST BOUNDARY, and THROW EXCEPTION!
            if (    (self.currRow < 0)
                 or (self.currRow >= self.MAX_ROWS)
                 or (self.currCol < 0)
                 or (self.currCol >= self.MAX_COLS)
               ):
                # ATTN:  use SET CONTAINS here to test VISITED!
                # || (visitedPoints.contains(nextPoint)) ) {
                # ATTN TRICKY:  note now that currPoint on CALLER will NOT be UPDATED,
                # nor SAVED as Visited if current move crosses boundaries!
                raise IndexError("Move to Row or Column out-of-grid-bounds")

            # ATTN:  add to visited list AFTER verification!
            # nextPoint.setData(data[currRow][currCol]);
            # visitedPoints.add(nextPoint);

            return (nextRow, nextCol)


def main(args):

    # INPUT data
    # inputData = readInput()

    # get dimensions of matrix
    # - http://stackoverflow.com/questions/14847457/how-do-i-find-the-length-or-dimensions-size-of-a-numpy-matrix-in-python
    # (maxRows, maxCols) = inputData.shape
    # visitedCache =  numpy.zeros(maxRows, maxCols)

    # AGILE CASE 0:  use OOP to init CURRENT held-state!
    spy = Spiraller(3,3)
    # ATTN:  Python has no concept of private!
    print (spy.currRow, spy.currCol)

    # AGILE CASE 1:  move one space in given direction; and ATTN to how moves are RELATIVE to origin; raster scan to MAX right, to MAX down
    # latestPosition = spy.moveOneSpotInCurrentDirection(Direction.RIGHT)
    # latestPosition = spy.moveOneSpotInCurrentDirection(Direction.DOWN)
    # latestPosition = spy.moveOneSpotInCurrentDirection(Direction.LEFT)
    # latestPosition = spy.moveOneSpotInCurrentDirection(Direction.UP)
    # print latestPosition

    # AGILE CASE 2: test BOUNDARY checks via stepping outside initial MAX DIMENSIONS
    try:
        # for step in xrange(2):
        for step in xrange(3):
            latestPosition = spy.moveOneSpotInOneDirection(Direction.DOWN)
            print latestPosition

    except Exception as ex:
        logging.exception("Something SILLY Happened!  Go recover!")

if __name__ == '__main__':
    main(sys.argv)

