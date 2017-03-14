
# Given N numbers
# Find all Tuples of 2 elements (X,Y) where (X + Y) = K

# APPROACH
# - INPUT:  unordered, repeated elements, positive integers
# - OUTPUT: => 2-tuples, unique (ie mirror tuple not double-counted)
#           eg where K=2
#           (1,3) and (3,1) are just counted ONCE?
#           => only care about pairs of POSITIVE complement, or NEGATIVE also allowed?
#           => only care about DIRECTIONAL difference, not ABS difference between (X, Y)
#           eg where K=3, X=5
#              Y = 8 OR 2
#           eg where K=2, X=3
#               X + Y = K
#               Y = K - X
#               => Y = 2 - 3 = -1
#           BUT where K=3, X=1
#               Y = 3 - 1 = 2
#               where K=3, X=2
#               Y = 3 - 2 = 1
#           => need to check that complement is IN the original list of numbers!
#           and to MARK already accounted for in a tuple!

# NOTE:  Python set() implementation:
#        http://stackoverflow.com/questions/3949310/how-is-set-implemented
#
# HUGE NOTE:  Python Time-Complexity:
#        https://wiki.python.org/moin/
#
# HUGE NOTE:  Python List index on FIND
"""
try:
    idx = sequence.index(x)
    print '%s occurred at position %s.' % (x, idx)
except IndexError:
    # do error processing
"""
# ATTN: SET operations
#   http://stackoverflow.com/questions/17511270/how-can-i-add-items-to-an-empty-set-in-python
# ATTN:  MAP operations
#   http://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops-in-python

# CALC TUPLE
def getTuples(data, difference):

    # find in orig list, and MARK itself, and its pair as accounted for
    # REMOVE:  visited NOT needed since already have UNIQUE hashtable keys, and we are doing DIRECTIONAL difference, NOT ABS value
    # visited = {}
    # for item in data:
        # visited[item] = 0

    # NOTE: SET serves to remove duplicates, and don't need to SET associated VALUEs!
    uniques = set(data)
    foundTuples = set()

    for first in uniques:
        # FIRST + SECOND = DIFFERENCE; so SECOND = FIRST - DIFFERENCE
        second = first - difference
        # ATTN:  DEBUG numbers need conversion to string!
        # print "First: " + str(first)
        # print "Second: " + str(second)
        # ATTN:  dests that SECOND is within set of valid numbers to choose from!
        if second in uniques:
            foundTuples.add((first, second))
            # visited[first] = 1
            # visited[second] = 1

    return foundTuples

# DRIVER
data = [1, 3, 2, 4, 4, 6, 8, 5, 7]
difference = 3
result = getTuples(data, difference)
print result


