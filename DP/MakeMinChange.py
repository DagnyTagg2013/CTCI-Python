
"""
PROBLEM:  Find MIN Number of Coins to Make Exact Change
GIVEN:  Infinite 25 cent, 10 cent, 5 cent, 1 cent coins
INPUT:  Absolute Amount in cents for Change
OUTPUT:  Number of Each Type of Coin needed for MINIMUM number coins in exact change
"""

"""
SOLUTION:
 * NOTICE, it takes FEWER LARGE-denomination coins to make up change
 * Find DIV and REMAINDER successively to make change from LARGEST COIN to SMALLEST coin
 * SAVE RESULT for EACH STAGE/COIN DENOMINATION
 * STOP when REMAINDER is ZERO
"""

"""
TEST CASE APPROACH:
* 1 cent
* 5, 10, 25 cents
* 30 cents
* 35 cents
* 37 cents
* 0 cents
* -1 cents
* 1000 cents
"""

"""
AGILE-STAGE APPROACH:
* GIVEN (one) Coin type; FIND DIV and REMAINDER
* SETUP DESCENDING VALUE DENOMINATION COINS; and LOOP thru ABOVE; SAVING RESULTS
* TEST for Boundary Cases
"""

# ATTN:  RUN ON CMD LINE as 'python Username MyProgram.py InputFilename'
# using the sys import to retrieve cmd-line args!
import sys

# ATTN:  Python TUPLE return is NOT TYPED on method signature; but can be simulated by Java Map.Entry!
# ATTN:  def and colon needed for function declaration!
# ATTN:  multi and single-line comments!
def getNumCoinsAndRemainder(amountToChange, coinValue):

    print "\nCALLING getNumCoinsAndRemainder({0}, {1})\n".format(amountToChange, coinValue)
    #ATTN:  calling amountToChange for Python TYPE conversions!
    # print type(amountToChange)
    # print type(coinValue)

    numCoins = amountToChange / coinValue
    remainder = amountToChange % coinValue

    # print "\nTUPLE RETURNING ({0}, {1})".format(numCoins, remainder)

    return (numCoins, remainder)

def processMinChange(amountToChange, coinValues):

    # ATTN:  Python equivalent of MAP as dict
    exactChange = {}

    # ATTN:  iterate thru list in Python
    for aCoinValue in coinValues:

        numCoins, remainder = getNumCoinsAndRemainder(amountToChange, aCoinValue)

        # ATTN: BUILD-UP result, even with 0 number of coins!
        exactChange[aCoinValue] = numCoins

        print "\n Building-Up Exact Change for NUM Coins then Coin value {0}:{1}".format(numCoins, aCoinValue)

        # ATTN:  update NEXT value
        amountToChange = remainder

        # ATTN:  EARLY EXIT condition
        if 0 == remainder:
            break

    return exactChange

def main(args):

    # ATTN1:  String formatting for PYTHON DEFAULT ARG TYPE of STRING!
    print("\n\nMAKING CHANGE FOR {0}!   Makes change from SECOND cmd-line argument if given.\n".format(args[1]))
    amountToChange = int(args[1])
    # TODO:  validate only one numeric arg given!

    # ATTN:  Python Sorted List Usage, SQUARE brackets!
    coinValues = [1, 25, 5, 10]
    # coinValues.sort(reverse=True)
    descendingCoinValues = sorted(coinValues, key = int, reverse = True)
    print "\nDescending Coin Values Are:  {0}\n".format(descendingCoinValues)

    # ATTN:  Python TUPLE return is NOT TYPED on method signature; but can be simulated by Java Map.Entry!
    # TEST 1:  SIMPLEST ONE-SET OF DATA TESTING CORE FUNCTION
    # TODO:  Comment out TEST DATA
    amountToChange = 15
    numCoins, remainder = getNumCoinsAndRemainder(amountToChange, coinValues[2])
    print("\nTEST 1:  EXACT CHANGE FOUND WITH REMAINDER:  {0}, {1}\n".format(numCoins, remainder))

    # TEST 2:  OUTER-LOOP TEST
    # TODO:  Comment out TEST DATA
    # amountToChange = 15
    exactChange = processMinChange(amountToChange, descendingCoinValues)

    # ATTN:  print results in ORDER
    print "***** EXACT CHANGE FOUND *****"
    print "(in descending order by CoinValue: NumCoins)"
    # ATTN:  to early exit condition!
    print exactChange

"""
    for aCoinValue in coinValues:
        if aCoinValue in exactChange:
            print "\n{0} coins of value {1}\n".format(exactChange[aCoinValue], aCoinValue)
"""

# TODO:  review this variable notation again!
# ATTN:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    main(sys.argv)








