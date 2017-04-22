__author__ = 'dagnyt'

# PROBLEM:  find n such that SUM of Nexp3, (N-1)exp3 ... 1exp3 equals given m
# ATTN:  CAREFUL to REUSE prior-calculated result, to NOT recompute!

def find_nb(m):
    memoBelowVol = 0
    for guess in xrange(1, m):
        # if (m == getStackVolume(guess)):
        guessTowerVolume = buildTowerVolumeFromMemo(memoBelowVol, guess)
        if (m == guessTowerVolume):
            break
        memoBelowVol = guessTowerVolume
    return guess

def buildTowerVolumeFromMemo(towerBelowVol, buildLevel):
    levelVol = buildLevel ** 3
    towerVol = towerBelowVol + levelVol
    print "Building Tower from Memo with Memo:{}, current Level:{} = Total:{}".format(towerBelowVol, levelVol, towerVol)
    return towerVol

"""
def getStackVolume(n):
    towerVol = 0
    # ATTN:  xrange EXCLUDEs TERMINATING value, so need to specify ONE-PAST!
    # ATTN:  need to specify to STOP at 1 instead of down to 0-default!
    for i in xrange(n, 0, -1):
        # http://stackoverflow.com/questions/30148740/how-do-i-do-exponentiation-in-python
        levelVol = i ** 3
        towerVol += levelVol
        print "{}:{}:{}".format(i, levelVol, towerVol)
    return towerVol

# TESTING!
print getStackVolume(3)
"""

result = find_nb(1071225)
print "Found best-guess n is:  {}".format(result)