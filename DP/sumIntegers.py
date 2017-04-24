__author__ = 'dagny t'

"""
Create a function that returns the sum of the two lowest positive numbers given an array of minimum 4 integers. No floats or empty arrays will be passed.

For example, when an array is passed like [19,5,42,2,77], the output should be 7.

[10,343445353,3453445,3453545353453] should return 3453455.

Hint: Do not modify the original array.
"""

# ************* SCRIPT-TESTING on test case data *************************

"""
data = [19,5,42,2,77]

# CACHE first two values
if data[0] < data[1]:
    lowest = data[0]
    nextLowest = data[1]
else:
    lowest = data[1]
    nextLowest = data[0]

# DYNAMICALLY update cache as-you-go
# ATTN: to == cases for FULL COVERAGE on REPEATED integers!
for num in data:
    if num > nextLowest:
        # DO NOTHING!
        pass
    elif (num > lowest) and (num <= nextLowest):
        nextLowest = num
    elif num <= lowest:
        nextLowest = lowest
        lowest = num

sumTwoMin = lowest + nextLowest

print sumTwoMin
"""

# ********* NOW PACKAGE into Function! ************************

def sumTwoMin(data):

    # print "INPUT data:  {}".format(data)

    # CACHE first two values
    if data[0] < data[1]:
        lowest = data[0]
        nextLowest = data[1]
    else:
        lowest = data[1]
        nextLowest = data[0]

    # print "INIT Lowest:  {} then {}".format(lowest, nextLowest)

    # DYNAMICALLY update cache as-you-go
    # ATTN: to == cases for FULL COVERAGE on REPEATED integers!
    # ATTN - BUG:  iterate PAST SLICE of FIRST two initialized values!
    for num in data[2:]:
        # print "ITER new item:  {}".format(num)
        if num > nextLowest:
            # DO NOTHING!
            pass
        elif (num > lowest) and (num <= nextLowest):
            nextLowest = num
        elif num <= lowest:
            nextLowest = lowest
            lowest = num
        # print "Updated Lowest:  {} then {}".format(lowest, nextLowest)

    result = lowest + nextLowest

    return result

# ***** DRIVER SCRIPT! *****

# data1 = [19,5,42,2,77]
data2 = [5, 8, 12, 18, 22]

print sumTwoMin(data2)








