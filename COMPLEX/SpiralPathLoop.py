
#
# PROBLEM:
# - START at ORIGIN of matrix
#   - SPIRAL path around to centre, not crossing prior path

# TODO:
# - BREAKDOWN problem to move SPIRALLY  (translate from my Java intqs airbnb SpiralPretty)

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

#
# - ATTN:  Java Reflection vs Python
# https://www.quora.com/Is-there-an-equivalent-of-Java-reflection-in-Python
# - ATTN:  MATRICES
# - Matrices in Python and NumPy, or even SciKitLearn
# http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python33

import sys
import numpy


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



def main(args):

    inputData = readInput()

    # get dimensions of matrix
    # - http://stackoverflow.com/questions/14847457/how-do-i-find-the-length-or-dimensions-size-of-a-numpy-matrix-in-python
    (maxRows, maxCols) = inputData.shape

    visitedCache =  numpy.zeros(maxRows, maxCols)


if __name__ == '__main__':
    main(sys.argv)

