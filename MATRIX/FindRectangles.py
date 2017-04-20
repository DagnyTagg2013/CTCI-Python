__author__ = 'dagny t'

#
# Imagine we have an image.
# We represent this image as a simple 2D array, where every pixel is a 1 or a 0.
# The image you get is known to have a single rectangle of 0s on a background of 1s. 
# Write a function that takes in the image and returns the coordinates of the rectangle -- 
# either top-left and bottom-right; or top-left, width, and height.
#

image1 = [
  [1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 0, 0, 1],
  [1, 1, 1, 0, 0, 0, 1],
  [1, 1, 1, 0, 0, 0, 1],
  [1, 1, 1, 1, 1, 1, 1],
]

image2 = [
  [0, 0, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 0, 0, 1],
  [1, 0, 1, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 1],
  [1, 0, 1, 0, 0, 1, 0],
  [1, 1, 1, 0, 0, 1, 0],
  [1, 1, 1, 1, 1, 1, 0],
]

# CASE 1:  SINGLE Rectangle of 2x3 zeroes within larger 1's background
#          NO OTHER rectangles, and COULD BE on TOP LEFT ORIGIN boundary,
#          or BOTTOM RIGHT ORIGIN boundary
def findRectangleBounds(image):

    # ASSUME at least one non-empty row
    # ASSUME at least one non-empty col
    # OTHERWISE pre-validate here and raise ValueError("...")
    MAX_ROWS = len(image)
    MAX_COLS = len(image[0])

    # ATTN:  init to NOT-YET-FOUND value
    # ATTN:  init originating value to then detect transition to NEXT value!
    topleft = (-1,-1)
    bottomright = (-1,-1)

    # NOTE:  pass in pre-init topleft to detect FIRST EDGE
    def findTopLeft(image, topleft):

         # ATTN:  scan FORWARDs from BEGIN bound
        for r in xrange(MAX_ROWS):
            for c in xrange(MAX_COLS):
                if (image[r][c] == 0):
                        if topleft[0] == -1:
                            topleft = (r,c)
                        break
        return topleft

    # NOTE:  pass in pre-init bottomright to detect FIRST EDGE
    def findBottomRight(image, bottomright):

        # ATTN:  scan BACKWARDs from END bound
        for r in xrange(MAX_ROWS-1, 0, -1):
            for c in xrange(MAX_COLS-1, 0, -1):
                if (image[r][c] == 0):
                    if (bottomright[0] == -1):
                        bottomright = (r,c)
                    break
        return bottomright

    # ATTN:  call nested methods in outer function closure to get results!
    topleft = findTopLeft(image, topleft)
    bottomright = findBottomRight(image, bottomright)

     # CASE 2: EDGE case of single 0 element at top left
    if ((bottomright[0] == -1) and (topleft[0] != -1)):
        bottomright = topleft

    # CASE 3:  EDGE case of single 0 element at bottom right
    if ((bottomright[0] != -1) and (topleft[0] == -1)):
        topleft = bottomright

    return (topleft, bottomright)


# **************** AGILE TEST SCRIPT on IMAGE 1 ************
# print findRectangleBounds(image1)
# ((4, 3), (6, 5))

# *******************************************************************************
# OBSERVATIONS:
# - MINIMUM data needed to make DECISION, and what KEY DECISIONs needed
# - vs MAXIMUM data to pickup from iterative row DATA SCAN;
# - vs what RESULTS can be DEDUCED from minimum Data
# - IDENTIFY MAP-CACHE/LOOKUP-BUILD iterative results oppty!
# - DECISIONS:
#   e.g. EDGE 1-to-0 to detect TOP-LEFT; then WIDTH; SCAN DOWN RHS to find 0-to-1 to detect BOTTOM-RIGHT!
#   NOTE:  OPTIMIZE to SKIP intermediate points if KNOW RECTANGLES always filled with 0s in them!
# - IDENTIFY DISJOINT/OVERLAP conditions!
# - IDENTIFY BOUNDARY cases!
#
#
## APPROACH 1:
#
# *******************************************************************************
# Systematic, generalized approach on PRECISE, MINIMUM, DEFINING conditions!
# *******************************************************************************
# - IMAGE-PROCESSING:  EDGE-CONDITION
# - topLeft (when EDGE-TRANSITION-BOUNDARY from Out-Of-Bounds OR 1 to 0 detected)
#
# MINIMUM DATA to save to MAKE A DECISION:
# - TOP LHS ANCHOR point of rectangle (transition boundary from 1-to-0 or 0 to Out-Of-Bounds)
# - ROW WIDTH (BETWEEN transition boundaries)
# - COLUMN length (BETWEEN transition boundaries)
# - CLOSE boundary (transition boundary from 0-to-1 or 0 to Out-Of-Bounds)
# WHAT DATA IS CONSTANT, WON'T CHANGE:
# - KNOW that only rectangular shapes, can rely on constant dimensions; so no need to check points WITHIN rectangle!
#
# *******************************************************************************
#
# *******************************************************************************
#
# SIMPLEST APPROACH with MINIMAL DATA
# TRICK:  - detect via CORNER EDGE-DETECTION via LOOK-BACK or LOOK-FORWARD!
#         - greedy-scan-iteration to pickup as much info as possible per row; via WIDTH calculation
#         - PIVOT-DERIVE height via path-trace!
#         - MINIMAL LOOKUP for next scan is via COLUMN
#           then closing CORNER EDGE-DETECTION via LOOK-FORWARD
#

# GIVEN:  one row of matrix
# ALGO:   detects all top left corners,
#         walks across top edge
# RETURNS:  MAP of TOP LEFT CORNERs to WIDTH found on specific row
def findTopLeftCorners(image, scanRow):

    # ASSUME at least one non-empty row
    # ASSUME at least one non-empty col
    # OTHERWISE pre-validate here and raise ValueError("...")
    MAX_ROWS = len(image)
    MAX_COLS = len(image[0])

    # validation
    if ((scanRow < 0)  or (scanRow >= MAX_ROWS)):
        return False

    foundTopLeftRects = {}
    # INIT to OUT-OF-BOUNDs
    priorLeft = -1
    # ATTN: scan FORWARDs from the BEGIN boundary
    for col in xrange(MAX_COLS):
        if (image[scanRow][col] == 0):
                # DETECT TOP LEFT CORNER based on spot directly ABOVE and to LEFT, via lookBack
                priorTop = image[scanRow - 1][col]
                if (
                     ((priorLeft == -1) or (priorLeft == 1))
                        and
                     ((priorTop == -1) or (priorTop == 1))
                   ):
                   topLeft = (scanRow, col)
                   # NOW, WALK the TOP ROW to DETERMINE the WIDTH
                   # init startCol
                   startCol = col
                   # ATTN:  STOP on RIGHT BOUNDARY as FIRST condition PRIOR to dereference!
                   while ((col < MAX_COLS) and (image[scanRow][col] == 0)):
                       # update prior value as scan, to detect breaks
                       priorLeft = image[scanRow][col]
                       col += 1
                   # now find WIDTH
                   rectWidth = col - startCol
                   # NOW, save WIDTH as value associated with topLeft corner anchor
                   foundTopLeftRects[topLeft] = rectWidth
                # update prior values
                else:
                    # update prior value as scan, to detect breaks
                    priorLeft = image[scanRow][col]
        else:
            priorLeft = image[scanRow][col]

    #ATTN:  don't forget to return!
    return foundTopLeftRects

    # ATTN:  actually call the nested function and return results!
    # return detectTopLeftCorners(scanRow)

# GIVEN:  top left corner of rectangle, width
# ALGO:   navigates to top right corner; than walks down until Bottom Right Corner detected
# RETURNS:  bottom right corner
def deriveBottomRightCorner(image, topLeft, rectWidth):

    MAX_ROWS = len(image)

    topRightCol = topLeft[1] + rectWidth - 1
    topRightRow = topLeft[0]

    bottomRightCorner = None
    priorRow = topRightRow
    for scanRow in xrange(topRightRow, MAX_ROWS):
        # DETECTs the EDGE-shift to 1
        # ATTN:  referencing 2-D array needs [][] rather than TUPLE!
        if (image[scanRow][topRightCol] == 1):
            bottomRightCorner = (priorRow, topRightCol)
            break
        # ATTN:  save PRIOR history BEFORE iterating to next Row scan value!
        priorRow = scanRow

    # DETECTs case where found Rectangle is on BOTTOM matrix boundary
    if (     (bottomRightCorner is None)
         and (scanRow == (MAX_ROWS - 1))
       ):
       bottomRightCorner = (priorRow, topRightCol)

    return bottomRightCorner

# GIVEN:  image ROW
# ALGO:   - for row, finds the TopLeft corners as KEY in Dict, mapped to VALUE of rectangle Width
#         - derives the bottom corner, and replace WIDTH with it
# RETURNS:  Dictionary mapping ROW_NUM to TopLeft corner, BottomRight corner tuple
def findDiagonalCorners(image, scanRow):

    foundRects = findTopLeftCorners(image, scanRow)

    # ATTN:  parse out corner, width via collection here!
    for topLeftCorner, width in foundRects.items():
        bottomRightCorner = deriveBottomRightCorner(image, topLeftCorner, width)
        # NOW, just OVERLAY foundRects entry with BOTTOM-RIGHT Corner!
        foundRects[topLeftCorner] = bottomRightCorner

    # ATTN:  remember to RETURN!
    return foundRects

# GIVEN: matrix
# ALGO:  scans each Row
#        finds Dict map of TopLeft corner to WIDTH of rectangle
#        walks to bottom Right corner to find closing point
# RETURN:  FLATTENED MAP of TUPLES of rectangles defined by TopLeft and BottomRight points!
# ATTN:  how to reproduce flatmap in Python
# http://www.markhneedham.com/blog/2015/03/23/python-equivalent-to-flatmap-for-flattening-an-array-of-arrays/
def findAllRectanglesInMatrix(image):

    MAX_ROWS = len(image2)
    allRectsInGridByRow = {}
    for scanRow in xrange(MAX_ROWS):
        foundRectsByRow = findDiagonalCorners(image2, scanRow)
        # ACCUM results here IFF non-empty
        # ATTN:  Pythonic way to check for empty
        if foundRectsByRow:
            allRectsInGridByRow[scanRow] = foundRectsByRow

    # NOTE:  could have just omitted owning scanRow; but just trying
    #        to DECONSTRUCT nested Dictionary into LIST of its individual ELEMENTs!
    flattened_rectangles = [
                            rectangles
                            # ATTN: without items(), default is keys()
                            for rowData in allRectsInGridByRow.items()
                            # retrieve EACH of SEVERAL items in VALUE entry of rowData!
                            for rectangles in rowData[1].items()
                           ]

    return flattened_rectangles

# *************** AGILE TEST SCRIPT on IMAGE 2 ***************

# foundRects = findTopLeftCorners(image2, 3)
# {(3, 1): 1}
# foundRects2 = findTopLeftCorners(image2, 2)
# {(2, 3): 3}
# print foundRects2
# foundRects5 = findTopLeftCorners(image2, 5)
# {(5, 6): 1, (5, 3): 2}
# print foundRects5

# ATTN:  iterate thru a dictionary
# https://www.mkyong.com/python/python-how-to-loop-a-dictionary/
# for each foundRects anchored by TopLeft corners on Row; derive BottomRight corner
"""
for topLeftCorner, width in foundRects5.items():
    bottomRightCorner = deriveBottomRightCorner(image2, topLeftCorner, width)
    # NOW, just OVERLAY foundRects entry with BOTTOM-RIGHT Corner!
    foundRects5[topLeftCorner] = bottomRightCorner
# {(5, 6): (7, 6), (5, 3): (6, 4)}
print foundRects5
"""

# NOW, call compound function based on test script above
# foundRects5 = findDiagonalCorners(image2, 5)
# {(5, 6): (7, 6), (5, 3): (6, 4)}
# print foundRects5

# foundRects2 = findDiagonalCorners(image2, 2)
# {(2, 3): (3, 5)}
# print foundRects2


# NOW, iterate thru ALL ROWs to ACCUMULATE row-level results for the ENTIRE matrix!
# ATTN:  concatenating two dictionaries, NOT like List.extend()!
# http://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/
"""
MAX_ROWS = len(image2)
allRectsInGridByRow = {}
for scanRow in xrange(MAX_ROWS):
    foundRectsByRow = findDiagonalCorners(image2, scanRow)
    # ACCUM results here IFF non-empty
    # ATTN:  Pythonic way to check for empty
    if foundRectsByRow:
        allRectsInGridByRow[scanRow] = foundRectsByRow
print allRectsInGridByRow
"""
# {0: {(0, 0): (0, 1)}, 2: {(2, 3): (3, 5)}, 3: {(3, 1): (5, 1)}, 5: {(5, 6): (7, 6), (5, 3): (6, 4)}}

# NOW, call compound function based on test script above
allRectangles = findAllRectanglesInMatrix(image2)
print allRectangles

# *************************** REJECTED  EXPERIMENTS -- TOO COMPLEX TO MATCH after-fact ************************************


# ATTN:  Detect BOTTOM-RIGHT Corner
# - if image content at position is 0
# - and if contents of point directly below, and also to the right is either OUT-OF-BOUNDs or 1
# ATTN:  index vs DEREFERENCED value!
"""
    def detectOneBottomRightCorner(image, row, col):

        MAX_ROWS = len(image)
        MAX_COLS = len(image[0])

        if (image[row][col] != 0):
            return False

        if (     ( (col == (MAX_COLS - 1)) or (image[row][col + 1] == 1) )
             and ( (row == (MAX_ROWS - 1)) or (image[row + 1][col] == 1) )
           ):
            return True
        else:
            return False
"""

# foundClosingCorner = detectOneBottomRightCorner(image2, 3, 3)
# False
# foundClosingCorner = detectOneBottomRightCorner(image2, 3, 5)
# True
# foundClosingCorner = detectOneBottomRightCorner(image2, 7, 6)
# print foundClosingCorner

# APPROACH 0:  - scan row; detect TOP-LEFT via LOOKBACK top and left for ENTRY EDGE 0 or out-of-bounds to 1
#                          scan to WIDTH
#                          detect BOTTOM-RIGHT via LOOKFORWARD right and bottom for EXIT EDGE
#                          where (C-ANCHOR + WIDTH) == (c) and r will always be greater than cached value already
#                          SO LOOKUP by CALCULATED (C-ANCHOR + WIDTH) !
#              *** can WALK EDGE DOWN to derive the BOTTOM-RIGHT-CORNER!
#
# APPROACH 1:  MAP of SUB-MAPs
#              MAP1 is KEYed by COLUMN;
#              values of MAP1 are
#              MAP2 keyed by TOP-LEFT point-tuple;
#              values are LATEST accumulated BOTTOM-RIGHT tuple
#
# APPROACH 2:  * SCAN ROW BY ROW for TOPLEFT, but SKIP WIDTH to get to next TOPLEFT on same row
#              ALSO, detect WIDTH, and SCAN DOWN to detect BOTTOM RIGHT
#              * CAN UPDATE SCAN by SKIP of END ROW-COLUMN by 1-boundary

# DATA STRUCT for APPROACH #2:  MAP1 is KEYed by TOP-LEFT point, then WIDTH,
#                               then traverse DOWN until BREAK found,
#                               to save BOTTOM-RIGHT point, and HEIGHT
#                               initialize with (-1, -1) for WIDTH, HEIGHT
#
#                               - scan TEST if point is IN existing RECT
#                                 if (r,c) is within r and c bounds of EXISTING RECTs,
#                                 SKIP scan by WIDTH
#                                 OTHERWISE - ADD as NEW TOP-LEFT for NEW RECTANGLE FOUND!
#
#                               - TEST RECT MEMBERSHIP
#                                 - if c in range of TOP-LEFT C0 to < (C0 + WIDTH)
#                                 - if r in range of TOP-LEFT R0 to < (R0 + HEIGHT)
#
