__author__ = 'dagnyt'

#!/bin/python

# ATTN:  MAKE CHANGE
# http://www.geeksforgeeks.org/dynamic-programming-set-7-coin-change/
import sys

def printMemoTable(memoCount, rows):

    # ATTN:  print ENTIRE 1-D columns for EACH ROW
    for i in xrange(0, rows):
            # print i
            print memoCount[i]
            print "\n"
    print "\n"

def make_change(coins, amount):

    numCoins = len(coins)

    # BOTTOM-UP build of 2-D MemoTable of
    # TOTAL COUNTs of WAYs to make Total Dollar Amount from ANY number of coins given distinct denominations

    # ATTN:  PRE_ALLOCATE and INITIALIZE 2-D Matrix!
    # ROWs is from 0 to Amount; or N+1
    # COLs is from 0 to m-1; or for each coin denomination INDEX for m coins
    # BUG:  DEEP-initialize 2D Matrix in PYTHON WITHOUT
    #       SHALLOW-COPY of REFERENCE!
    """
    https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
    """
    # initRow = [0] * numCoins
    # memoCount = [initRow] * (amount + 1)
    # ATTN:  LIST COMPREHENSION to GENERATE DEEP-INIT values, NOT SHALLOW REFERENCE COPY as above!
    memoCount = [ [0 for cols in range(numCoins)]
                     for rows in range(amount + 1)]

    # ATTN: print Results!
    # print "\nCLEAR Memo Count is:  \n"
    # printMemoTable(memoCount, (amount + 1))


    # ATTN:
    # - for Amount TOTAL DOLLARS of 0 ACROSS Coins ==> 1 is Count Ways to NOT
    #   include Coin
    totalValue = 0
    for coinIdx in xrange(0, numCoins):
        memoCount[totalValue][coinIdx] = 1


    # ATTN: print Results!
    # print "\nINIT Memo Count is:  \n"
    # printMemoTable(memoCount, (amount + 1))

    for totalValue in xrange(1, amount + 1):

        for coinIdx in xrange(0, numCoins):

            # ATTN: DEBUG loop top; INDEX vs VALUE at index!
            # print "\nUPDATING Memo Count for Amount{} CoinValue{} CoinIdx{} is:  \n".format(totalValue, coins[coinIdx], coinIdx)

            # ATTN:  if Coin denomination > totalValue, then there are 0 ways
            #        to choose coin!
            remainder = (totalValue - coins[coinIdx])
            # print 'remainder:  {}'.format(remainder)
            # Count to INCLUDE current coin is derived from
            # including coin for LOWER dollar amount for current coin
            # chosen
            # (dollar amount MINUS value of current coin)
            # ATTN:  Ternary OP!
            # https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator
            if (remainder >= 0):
                countIncludeCoin = memoCount[remainder][coinIdx]
            else:
                countIncludeCoin = 0

            # Count to EXCLUDE current coin is derived from
            # excluding coin for dollar amount
            # IFF there is a PRIOR coin value to look at where coin >=1
            if (coinIdx >= 1):
                countExcludeCoin = memoCount[totalValue][(coinIdx-1)]
            else:
                countExcludeCoin = 0


            # SUM results from both options into CURRENT count
            memoCount[totalValue][coinIdx] = countIncludeCoin + countExcludeCoin

            # ATTN: print incremental Results!
            # printMemoTable(memoCount, (amount + 1))

    # return FINAL CUMULATIVE result
    return memoCount[amount][(numCoins-1)]


# DRIVER TEST SCRIPT!

print "\nTEST CASE 1"
n = 4
m = 3
coins = [1, 2, 3]
print 'total money {}: total coinTypes {}'.format(n, m)
print coins
print 'FINAL COUNT is (Expect 4): '
print make_change(coins, n)


print "\nTEST CASE 2"
n = 10
m = 4
coins = [2, 5, 3, 6]
print 'total money {}: total coinTypes {}'.format(n, m)
print coins
print 'FINAL COUNT is (Expect 5): '
print make_change(coins, n)