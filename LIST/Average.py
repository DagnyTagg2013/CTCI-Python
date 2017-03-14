
import numpy as np

# calculate the running average of a STREAM of numbers modeled as a list
# ATTN:  cache SUM, not AVG; as LOSE precision if calc from running AVG!
# http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# ATTN:  use EXTEND
# http://stackoverflow.com/questions/14446128/python-append-vs-extend-efficiency
# ATTN:  Use Python SLICE specifying one PAST END index NOT Length!
# ATTN:  EXTEND takes ITERABLE as input so [], or just use += to extend!
# ATTN:  PRE-ALLOCATE
# - http://stackoverflow.com/questions/983699/initialise-a-list-to-a-specific-length-in-python
# ATTN:  print elements in List
# - http://stackoverflow.com/questions/15769246/pythonic-way-to-print-list-items

# ATTN:  CLUNKY CLASS
class RunningAvg1:

    # ATTN:  need to specify THIS ptr!
    def __init__(self, first):
        # only need to save running SUM
        self.sum = first
        self.count = 1

    def calcLatest(self, newItem):
        self.sum += newItem
        self.count += 1
        # ATTN: multiply by 1.0 to get DECIMAL!
        avg = self.sum * 1.0/self.count
        return avg

# TODO:  debug w numpy!
# ATTN:  with numpy
def RunningAvg2(data):

    count = len(data)
    # ATTN:  initialization!
    sum = np.zeros(count)
    avg = np.zeros(count)
    for i in range(count):
        sum[i] = np.sum(data[0:(i+1)])
        # ATTN:  Scalar multiply on ONE element, NOT vector!
        avg[i] = 1.0 * sum[i] * 1/(i+1)
    return avg

# ATTN: via list input and output format
def RunningAvg3(data):

    # capture len ONCE!
    countAll = len(data)
    # initialize FIRST!
    total = []
    count = []
    avg = []
    # ATTN:  extend takes ITERABLE, so pass in []
    total.extend([data[0]])
    count.extend([1])
    avg.append(total[0]/count[0])
    for i in range(1, countAll):
        # ATTN:  SLICE takes SECOND arg as one PAST end Idx, THIRD arg is STEP
        total.extend([sum(data[0:(i+1)])])
        count.append(count[i-1] + 1)
        # ATTN:  get decimal
        avg.append(total[i] * 1.0/count[i])
    return avg

# ATTN: via list input and output format, PREALLOCATED
def RunningAvg4(data):

    countAll = len(data)

    # ATTN:  initialization syntax!
    total = countAll * [-1]
    count = countAll * [-1]
    average = countAll * [-1]

    total[0] = data[0]
    count[0] = 1
    average[0] = data[0]

    for i in range(1, countAll):
        total[i] = total[i-1] + data[i]
        count[i] = count[i-1] + 1
        average[i] = (total[i] * 1.0)/count[i]
        # ATTN:  debug with print statement for STRING
        print "DEBUG"
        print average[i]

    return average


# DRIVER Script
print "TRY1"
driver = RunningAvg1(1)
print driver.calcLatest(2)
print driver.calcLatest(3)

print "\nTRY2"
data = [1, 2, 3]
print RunningAvg2(data)

print "\nTRY3"
print RunningAvg3(data)


print "\nTRY4"
print RunningAvg4(data)

print "\nTRY PRINTING TRICKS FOR LIST!"
# ATTN:  convert list to string! for string vs non-string elements
# string elements
for p in data: print p

# non-string elements
valueStr = ','.join(str(p) for p in data)
print "\n" + valueStr

