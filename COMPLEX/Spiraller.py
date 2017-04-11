
#
# PROBLEM:
# - START at ORIGIN of matrix
#   - SPIRAL path around to centre, not crossing prior path

# TODO:
# - BREAKDOWN problem to move SPIRALLY (translate from my Java intqs airbnb SpiralPretty)

# STEP 1:  MINIMAL TRANSFORM move before having to examine state to decide on NEXT move!
# ATTN:  simple to MODIFY from clockwise to counter-clockwise with this!
# ATTN TRICKY:  MOST GRANULAR currRow, currCol which may move INDEPENDENTLY of Point PAIR!
#               THEN TEST AGAINST ALREADY-VISITED!
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
# http://python-guide-pt-br.readthedocs.io/en/latest/writing/logging/
# - ATTN:  VARIABLE ARGS
# http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
# - ATTN:  FORMAT STRINGS
# https://pyformat.info
# - ATTN:  DICTONARIES
# https://learnpythonthehardway.org/book/ex39.html
# http://stackoverflow.com/questions/473099/check-if-a-given-key-already-exists-in-a-dictionary-and-increment-it
# - ATTN: TODO - ENUMs in Python 2.x to print NAME for Enum VALUE
# http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python

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
        # ATTN:  need to HOLD THIS STATE for NEXT-STATE-TRANSITION RULE!
        self.currDirection = Direction.RIGHT
        # ATTN:  assume ORIGIN point VISITED already!
        self.visitedPoints = {(0,0):True}

    class Point:

        def __init__(self, x, y):
            self.x = x
            self.y = y

    # ATTN; parameterize function to handle a move in BOTH directions
    # TRICKY:  UP-DOWN operates on ROW, LEFT-RIGHT operates on COL!
    def _move(self, deltaX, deltaY):
        nextCol = self.currCol + deltaX
        nextRow = self.currRow + deltaY
        return (nextRow, nextCol)

    # ATTN:  Quora, Why Python has no switch statement, and implement via Dictionary and LAMBDA!
    def moveOneSpotInOneDirection(self, direction):

            # ATTN:  SETUP the direction SWITCH simulation via DICTIONARY to lambda function parameterized
            #        by DIRECTION KEY, executing specific move across 2D grid
            # TRICKY:  want to LAZY-EXECUTE, ie ONLY when get is invoked on specific input GET/SWITCH on DIRECTION
            #         SO want to pre-assign lambda function pointer with known input calling params
            moveOptions = {
                            Direction.RIGHT: lambda: self._move(1, 0),
                            Direction.DOWN: lambda: self._move(0, 1),
                            Direction.LEFT: lambda: self._move(-1, 0),
                            Direction.UP: lambda: self._move(0, -1)
                          }

            # TRICKY:  get() actually executes the SWITCH to the LAMBDA programmatic action,
            # then you have to do () to EXECUTE the actual ACTION
            calcNextMove = moveOptions.get(direction)
            (nextRow, nextCol) = calcNextMove()

            # ATTN: TEST BOUNDARY, and THROW EXCEPTION!
            # ATTN;  TEST VISITED, and THROW EXCEPTION!
            if (    (nextRow < 0)
                 or (nextRow >= self.MAX_ROWS)
                 or (nextCol < 0)
                 or (nextCol >= self.MAX_COLS)
                 # ATTN:  TEST DICTIONARY KEY exists with DEFAULT None value; to avoid KeyError!
                 or (self.visitedPoints.get((nextRow, nextCol), None) is not None)
               ):
                # ATTN:  use set CONTAINS here to test VISITED!
                # || (visitedPoints.contains(nextPoint)) ) {
                # ATTN TRICKY:  note now that currPoint on CALLER will NOT be UPDATED,
                # nor SAVED as Visited if current move crosses boundaries!
                raise IndexError("Move to Row or Column out-of-grid-bounds OR Visited spot already!")
            else:
                # ATTN:  only add to visited list AFTER verification!
                # ATTN:  only update current position AFTER verification!
                self.currRow = nextRow
                self.currCol = nextCol
                self.visitedPoints[(self.currRow, self.currCol)] = True

            # ATTN:  return LATEST VALIDATED position!
            return (self.currRow, self.currCol)


    def moveToBoundaryInOneDirection(self):

        try:
            # EXITs loop on exception, so only saves LAST VALID position!
            while (True):
                latestPosition = self.moveOneSpotInOneDirection(self.currDirection)
                print latestPosition

        except IndexError as err:
            # logging.exception("Expected Boundary Reached In Direction; so now change to SPIRAL towards next Direction!")
            print "Expected Boundary Reached In Direction; so now change to SPIRAL towards next Direction!"

        # returns only LAST VALID position!
        return (self.currRow, self.currCol)

    # ATTN:  Quora, Why Python has no switch statement, and implement via Dictionary and LAMBDA!
    def changeToSpiralDirection(self):

        # TRICKY: statement SAME as RETURN of one value!
        directionOptions = {
                                Direction.RIGHT: lambda: Direction.DOWN,
                                Direction.DOWN: lambda: Direction.LEFT,
                                Direction.LEFT: lambda: Direction.UP,
                                Direction.UP: lambda: Direction.RIGHT
                           }

        calcNextDirection = directionOptions.get(self.currDirection)
        self.currDirection = calcNextDirection()
        # logging.log(logging.INFO, 'CHANGED DIRECTION to {}'.format(self.currDirection))
        print 'CHANGED DIRECTION to {}'.format(self.currDirection)

        return self.currDirection


    def moveSpirally(self):

        numAllPoints = self.MAX_COLS * self.MAX_ROWS

        while (len(self.visitedPoints) < numAllPoints):

            self.moveToBoundaryInOneDirection()
            self.changeToSpiralDirection()

        print "DONE VISITING ALL POINTS!"

def main(args):

    # INPUT data
    # inputData = readInput()

    # GET dimensions of data for tracking visited points
    # - http://stackoverflow.com/questions/14847457/how-do-i-find-the-length-or-dimensions-size-of-a-numpy-matrix-in-python
    # (maxRows, maxCols) = inputData.shape
    # visitedCache =  numpy.zeros(maxRows, maxCols)

    # AGILE CASE 0:  use OOP to init CURRENT held-state!
    spy = Spiraller(3,3)
    # ATTN:  Python has no concept of private!
    print (spy.currRow, spy.currCol)

    # AGILE CASE 1:  move one space in given direction; and ATTN to how moves are RELATIVE to origin; raster scan to MAX right, to MAX down
    """
        latestPosition = spy.moveOneSpotInCurrentDirection(Direction.RIGHT)
        latestPosition = spy.moveOneSpotInCurrentDirection(Direction.DOWN)
        latestPosition = spy.moveOneSpotInCurrentDirection(Direction.LEFT)
        latestPosition = spy.moveOneSpotInCurrentDirection(Direction.UP)
        print latestPosition
    """

    # AGILE CASE 2: test BOUNDARY checks via stepping outside initial MAX DIMENSIONS
    """
    try:
        # for step in xrange(2):
        # EXITs loop on exception, so only saves LAST VALID position!
        for step in xrange(3):
            latestPosition = spy.moveOneSpotInOneDirection(Direction.DOWN)
            print latestPosition

    except Exception as ex:
        logging.exception("Something SILLY Happened!  Go recover!")
    """

    # AGILE CASE 3:
    # - encapsulate moving to BOUNDARY in ONE direction
    # - then SWITCH direction
    spy.moveSpirally()


if __name__ == '__main__':
    main(sys.argv)

