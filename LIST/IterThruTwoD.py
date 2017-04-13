
# PROBLEM:
# - support next() iteration through a 2D List of:
#   - rows of uneven length
#   - possibly empty rows
#   - integer values
# - support hasNext() to PEEK next value exists prior to iteration, idempotent -- can be called over with same result
# - support remove() to remove LAST-seen value from next()
#
# ASSUMPTIONS:
# - no worries about None data
# - first element always is a non-empty row with at least one column datapoint

# APPROACH:
#
# BRAINSTORM -- CORE of what's important!
# - ITERATION over SELF-MODIFYING DATA is DUMB:
#
"""
MAJOR TODO ISSUE:

You need to take a copy of the list and iterate over it first, or the iteration will fail with what may be unexpected results.
http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating

For example (depends on what type of list):

for tup in somelist[:]:
    etc....
An example:
>>> somelist = range(10)
>>> for x in somelist:
...     somelist.remove(x)
>>> somelist
[1, 3, 5, 7, 9]

>>> somelist = range(10)
>>> for x in somelist[:]:
...     somelist.remove(x)
>>> somelist
[]
"""
#
# ITERATOR
# - store original data structure
# - store LATEST state
# - needs to account for offset into different row lengths RELATIVE to current state!
#
# SPECIAL INPUT CONDITIONS
# *** ATTENTION:  no sense to FLATTEN to 1D position offset at we can't rely on UNIFORM ROW size!
# - input has VARYing length rows
# - OK to assume NO None items, and that input has AT LEAST first row, with one or more elements
#
# CODE
# - start with SIMPLEST-BASE data input case, for CORE function,
#   to determine what data storage is needed,
#   then just get simplified tests to pass
# - ATTENTION:  PEEK AHEAD before attempting to dereference!
# *** then MOVE ONTO more complex cases LATER!

# ATTN:  Python Exceptions!
# - http://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
# - http://stackoverflow.com/questions/1508467/log-exception-with-traceback
#

import logging

class Iterator():

    def __init__(self, data):

        self.data = data
        # TODO:  validate that data has AT LEAST one Row, one Column and throw exception otherwise!
        self.currRow = 0
        self.currCol = 0
        self.priorRow = -1
        self.priorCol = -1
        # NOTE:  we need to determine NUM ROWs for CASES 3, 4 in NEXT below!
        self.numRows = len(data)
        # NOTE: DEBUG BELOW!
        # print self.data
        # print self.numRows

    def next(self):

        # CASE 1:  get FIRST element
        if ((self.currRow == 0) and (self.currCol == 0)):
            nextItem = self.data[0][0]
        else:
            # ATTENTION: CACHE for later REMOVE!
            self.priorRow = self.currRow
            self.priorCol = self.currCol
            nextItem = self.data[self.currRow][self.currCol]

        # ***************** UPDATE current Position pointers ********************

        # TODO:  this exception should only get raised in invocation of next() at LAST empty Row position,
        #        and NOT yet on THIS FIRST next() call
        # CASE 6:  EXCEPTION, EARLY EXIT on case where we are at the LAST row, and it's empty
        #          AND we try to call NEXT
        if ( (self.currRow == (self.numRows - 1)) and ( len(data[self.currRow]) == 0 ) ):
            raise IndexError

        # CASE 2:  iterate current position to NEXT,
        #          but FIRST PEEK if BOUND reached
        # FIRST if there's data left in the current row,
        # and have to RECALC each time!
        lenCurrRow = len(data[self.currRow])

        if ((self.currCol + 1) < lenCurrRow):
            self.currCol += 1

        # CASE 4:  we have NO more rows so we need to throw an exception if BOUNDary reached!
        # ATTN PYTHON uses ELIF!
        elif ((self.currRow + 1) > self.numRows):
            raise IndexError

        # CASE 3: we cross current Row bound into first item of next row
        #         and need to RESET column
        elif ((self.currRow + 1) < self.numRows):

            # CASE 5: check if we come across an EMPTY row, but FIRST check if currRow even exists,
            # then we need to cycle to get to the NEXT nonempty row
            self.currRow += 1
            while ( ( (self.currRow + 1) < self.numRows ) and ( len(data[self.currRow]) == 0 ) ):
                self.currRow += 1

            # ATTN: column always RESETs to 0 on getting to the next row!
            self.currCol = 0

        # ****************** NOW RETURN NEXT ITEM! ************************
        #
        return nextItem


    # ATTN TRICKY:
    # - set TOMBSTONE value without removing to not disturb-reallocate the current 2D structure!
    def remove(self):

        if ((self.priorRow == - 1) and (self.priorCol == -1)):
            # NOTE:  error if next() has not been called to initialize this previously
            raise IndexError

        # check for PRIOR remove, and raise error if previously removed
        if (self.data[self.priorRow][self.priorCol] ==  -1):
            raise IndexError
        else:
            priorValue = self.data[self.priorRow][self.priorCol]
            # mark tombstone
            self.data[self.priorRow][self.priorCol] = -1
        return priorValue

    # ATTN NEED to add this for debug purposes!
    def show(self):

        print self.data


# Test Driver
# ATTN:  enclose in EXCEPTION BLOCK!

try:

    data = [[1,2], [], [], [3,4,5], [6], []]
    iter = Iterator(data)

    print iter.next()  # 1
    print iter.next()  # 2
    print iter.next()  # 3
    print iter.next()  # 4
    print iter.next()  # 5
    print iter.next()  # 6
    # print iter.next()  # ERROR, IndexOutOfRange

    print iter.remove()
    iter.show()

    # TODO:  handle HAS_NEXT case
    #        via PEEK on pre-existing nextItem WITHOUT iteration with next
    """

        print iter.next()

        print iter.hasNext()
        print iter.hasNext()
        print iter.next()
    """

except IndexError, err:

    logging.exception(err)