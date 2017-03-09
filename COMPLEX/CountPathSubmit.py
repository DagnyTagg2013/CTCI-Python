import numpy

# DP-building pathcount from ORIGIN out to MAX point
# WANT THIS vs RECURSION on
# def buildPathCount(self, openGrid):
def buildPathCount(openGrid):

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
                # ATTN:  Building result from directly ABOVE, directly LEFT
                pathCountCache[r,c] = pathCountCache[r-1,c] + pathCountCache[r,c-1]
                # ATTN:  MAY PERMIT DIAGONAL PATH; ONLY on PRIMARY DIAGNOAL to ORIGIN
                if ((r-1) == (c-1)):
                    pathCountCache[r,c] += pathCountCache[r-1,c-1]


    # at this point, FINAL MAX POINT COUNT is calculated
    return pathCountCache[(ROWS - 1), (COLS - 1)]