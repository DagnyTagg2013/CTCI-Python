__author__ = 'dagny t'

# Imagine we have an image. We’ll represent this image as a simple 2D array where every pixel is a 1 or a 0.
# The image you get is known to have a single rectangle of 0s on a background of 1s. Write a function that takes in the image and returns the coordinates of the rectangle -- either top-left and bottom-right; or top-left, width, and height.
#
image = [
  [1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 0, 0, 1],
  [1, 0, 1, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 1],
  [1, 0, 1, 0, 0, 1, 1],
  [1, 1, 1, 0, 0, 1, 1],
  [1, 1, 1, 1, 1, 1, 1],
]

# CASE 1:  SINGLE Rectangle of 2x3 zeroes within larger 1's background
def findRectangleBounds(image):

    # ASSUME at least one non-empty row
    # ASSUME at least one non-empty col
    # OTHERWISE pre-validate here and raise  ValueError("...")

    MAX_ROWS = len(image)
    MAX_COLS = len(image[0])

    def findTopLeft(image):
        # ATTN: init to NOT-FOUND values
        toplh = (-1,-1)
        for r in xrange(MAX_ROWS):
            for c in xrange(MAX_COLS):
                if (image[r][c] == 0):
                        if toplh[0] == -1:
                            toplh = (r,c)
                        break
        return toplh

    def findBottomRight(image, toplh):
        # ATTN: init to NOT-FOUND values
        bottomrh = (-1,-1)
        # ATTN:  scan BACKWARDs from OUTER bound
        for r in xrange(MAX_ROWS-1, 0, -1):
            for c in xrange(MAX_COLS-1, 0, -1):
                if (image[r][c] == 0):
                    if (bottomrh[0] == -1):
                        bottomrh = (r,c)
                    break

        # CASE 2: EDGE case of single 0 element at toplh
        if ((bottomrh[0] == -1) and (toplh[0] != -1)):
            bottomrh = toplh

        return bottomrh

    # ATTN:  CALL nested methods in outer function closure to get results!
    toplh = findTopLeft(image)
    bottomrh = findBottomRight(image, toplh)
    return (toplh, bottomrh)


# ************** DRIVER SCRIPT ****************************
# ATTN:  DRIVER script here!
print findRectangleBounds(image)


# - cache with DICT anchor KEY = toplh; VALUE = bottomrh;
# - scan for 0;
# => check if position r is >= toplhs, or c >= toplhs of cached tophls (can fit in MULTIPLE possible rectangles)
#    - if it IS; then store this LATEST (r,c) scanned 0 as LARGEST scanned position
#      i.e. use as CUMULATIVE STATE TRACKER!
# - if NOT member of existing rectangle, ENTER as NEW RECTANGLE entry in cache
# => DETECTION CONDITION for bottom rhs CLOSURE is that 1 is on RIGHT (AND) on BOTTOM
#    so MARK as CLOSED RECTANGLE; and REMOVE from STILL EXPANDING/SEARCHING WORKING cache to lookup!
#    => add to COMPLETED CACHE of rectangles!
def findAllRectangles(image):

    MAX_ROWS = len(image)
    MAX_COLS = len(image[0])

    cachedExploringRects = {}
    cachedCompletedRects = {}

    for r in xrange(MAX_ROWS):
        for c in xrange(MAX_COLS):
            if (image[r][c] == 0):
                # STEP1: locate Owner rectangle(s) for current scan point, then save it as LATEST FAR BOUNDARY associated with toplh anchors
                # STEP 2:  test for CLOSURE point by look-ahead RIGHT, LEFT for EITHER 1 or MATRIX BOUND, then CLOSEit!
                # TODO:  want FASTEST 2D RANGE LOOKUP of associated toplh rectangle anchor by CURRENT (r,c)
                # KNOW:  current scanning row is ALWAYS >= CACHED toplhs RECTANGLE ANCHOR previously cached!
                # ONLY CARE to TEST variable:  current scanning column is greater or equal to RECTANGLE ANCHOR PREVIOUSLY CACHED
                # SO:  can OPTIMIZE LOOKUP BY ADDING ORDERED COLUMN BUCKETS with LISTS of Toplh ANCHOR tuple points
                allToplhAnchors = cachedExploringRects.keys()
                for oneExploringRectToplh in allToplhAnchors:
                    if ((r >= oneExploringRectToplh[0]) and (c >= oneExploringRectToplh[1])):
                        cachedExploringRects[oneExploringRectToplh] = (r,c)

                # DETECT completion, and MOVE from ExploringRects to CompletedRects!


