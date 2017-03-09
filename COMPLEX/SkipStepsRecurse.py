


#!/bin/python

import sys
import os

# RECURSIVE PATH-POSSIBILITIES
# - n is MAX TOTAL number of moves
# - @ each move can STAY at current step (start from 0) or hop (+i) where i is current move number
# - returns MAX step reached across ALL possible move paths
# - e.g. 2,2 =>
#   e.g. 3,3 => 5
def  maxStep(n, k):

    currStep = 0;  # POSITION is 0th step
    currMove = 1;  # MOVE is DELTA from currStep to get to nextStep

    (validPath, maxStepForPath) = maxStepRecurse(currMove, currStep, k, n)

    return maxStepForPath

# *******************************************************************************************************
# STAB2:  ITERATIVE DRIVER of OUTER-LOOP function
# * DECISION TREE:  EACH move offers TWO choices;
# - STAY
# - or HOP up Num Steps EQUAL to current Move Number
# * 2 EXP N FINAL path possibilities at LEAVes
# - ELIMINATE intermediate paths via CHECK against blockedStep
# * recursion can BLOW-UP the STACK on EXPONENTIAL complexity for LARGE N!
#   SO INSTEAD use WHILE iterate through EACH CHOICE BRANCHING-POINT; LIMIT to maxNumMoves
# - RETURN TUPLEs with UPDATED state for NEXT iteration
# * DUNNO: look into reuse/memoization of CACHE-MAP of prior-calculated results to
# BLOCK REDUNDANT PATHs on EXPONENTIAL CHOICE-TREE!
# eg reuse of prior CUMULATIVE state (like SUM) from SUBSET of problem-space
# * ISSUE:  LOCAL optima does NOT imply GLOBAL optima; i.e. for N=3; maxVal at i=1; 0 < 1
#           BUT; maxVal at i=3; 5 > 4 (0, 2, 5; vs 1, 1, 4)
# * SOLUTION:  - represent each possible path via 2expN Bit Array
#              - accumulate CURRENT STEP; OR -1 for Bit Array; as progressing through MOVES from 1 to N
#              - FINAL LOOP through ALL results to see MAXIMUM; since local MAXIMUM of subset does NOT determine OVERALL MAXIMUM!

"""
def iterPathsToMaxFinalStep(maxNumMoves, blockedStep):

    # STEP 1:
    # initialize STARTing States, and iteration vars
    # THEN ID Iteration Variables
    currStep = 0;  # POSITION is 0th step
    currMove = 1;  # MOVE is DELTA from currStep to get to nextStep


    # STEP2:  ACCUMULATE FINAL STEP POSITION RESULTs;
    #         INDEXED-BY BIT-ARRAY of PATH-NAV-CHOICES; (0 to STAY, 1 to GO at position X)
    #         STARTING index 1
    #         - or 2 EXP N possible paths
    cacheFinalStepByMovePath = {}

    # DUNNO:  START from END; then step BACK; or START at START, go FORWARD?
    while (currMove <= maxNumMoves):

        # STEP3:  DECIDE on NEXT SKIP MOVE on PATH; then eliminate all BAD DOWNSTREAM DECISION PATHs!

        # STEP 4: DECIDE REMAIN at current position, then eleminate all BAD DOWNSTREAM DECISION PATHs!
        # TODO:  set all cacheFinalStepByMovePath elements to currStep
        # - where bit is 1 for decision to SKIP steps at index currMove
        # - where bit is 0 for decision to STAY at index currMove

        # STEP5:  ITERATE control-variables where currStep ALREADY handled!
        currMove = currMove + 1


    # STEP 6:  TWO-PASS APPROACH to now scan ACROSS LOWEST-GRANULARITY-CUMULATIVE RESULTs;
    #          to derive MAX-STEP! or 2 exp N LEAVEs of FINAL Decision Tree!

}
"""

# *******************************************************************************************************
# STAB1:  RECURSIVE FUNCTION
# * PROBLEM:  recursive BLOWS-UP STACK for large N
# * - captures BRANCHing-DECISIONs @ EACH STEP-ITERATION
# * - increments progress of decision-tree-level "curr" values;
#   OR exits when BLOCKED POSITION arrived at;
#   OR exits when maxNumMoves made!
# * - RETURNs tuple of (Boolean, currMaxStepForPath) for a VALID PATH while not hitting BLOCKED STEP
def maxStepRecurse(currMoveNum, currStep, blockedStep, maxNumMoves):

   isValidPath = True

   # CHOICE 1:  can STAY on currentStep
   # - IFF Blocked Spot:  EXIT as INVALID PATHWAY, AND return UNCHANGED currStep
   # - IFF NOT Blocked Spot:  PROCEED as VALID PATHWAY
   if ((currStep + 0) == blockedStep):
       # EXITs path as hit BLOCKED spot
       # TODO:  SAVE this to 2 exp N results Map
       print "\nA maxStep reached on unique BLOCKed Path:  {0}\n".format(currStep)
       return (False, currStep)
   else:
       currMoveNum = currMoveNum + 1
       # EXIT if maxNumMoves made!
       if (currMoveNum > maxNumMoves):
            # TODO:  SAVE this to 2 exp N results Map
            print "\nA LEAF reached on unique Path with maxStep:  {0}\n".format(currStep)
            return (True, currStep)
       else:
            # PROCEED, as VALID PATH!
            (isValidPath, currStep) = maxStepRecurse(currMoveNum, currStep, blockedStep, maxNumMoves)


   # CHOICE 2:  can SKIP num steps matching currMoveNum
   # - IFF Blocked Spot:  EXIT as INVALID PATHWAY, AND return UNCHANGED currStep
   # - IFF not Blocked Spot: PROCEED as VALID PATHWAY
   if ((currStep + currMoveNum) == blockedStep):
       # TODO:  SAVE this to 2 exp N results Map
       print "\nA LEAF reached on unique Path with maxStep:  {0}\n".format(currStep)
       return (False, currStep)
   else:
       currMoveNum = currMoveNum + 1
       # EXIT if maxNumMoves made!
       if (currMoveNum > maxNumMoves):
            # TODO:  SAVE this to 2 exp N results Map
            print "\nA LEAF reached on unique Path with maxStep:  {0}\n".format(currStep)
            return (True, currStep)
       else:
            # PROCEED, along VALID PATH!
            currStep = currStep + currMoveNum
            (isValidPath, currStep) = maxStepRecurse(currMoveNum, currStep, blockedStep, maxNumMoves)

   return (isValidPath, currStep)

def main(args):

    maxStepForPath = maxStep(2, 2)


# ATTN:  this only executes when file executes as a SCRIPT, not when it's imported!
# http://stackoverflow.com/questions/22492162/understanding-the-main-method-of-python
if __name__ == '__main__':
    main(sys.argv)

# *****************************************************************************
# TODO:  read input from STDIN; then write result of trial to output file!

"""
def readInput():

    print "Enter matrix dimensions!"

    # ATTN:  cast to int!
    maxRows, maxCols = map(int, sys.stdin.readline().split(','))

    # ATTN THIS WON'T work for initial space allocation!

    # matrix = []
    # for i in range(0, maxRows):
    #     matrix[i] = list(map(int, sys.stdin.readline().split(',')))

    # allocate space here!
    matrix = numpy.zeros((maxRows, maxCols))

    print "Enter matrix data by CSV integer rows!!"
    for i in range(0, maxRows):
        row_data = list(map(int, sys.stdin.readline().split(',')))
        for j in range(0, maxCols):
            matrix[i][j] = row_data[j]

    print matrix

    return matrix

"""

# *******************************************************************************************************
# TODO:  read input from STDIN; then write result of trial to output file FROM THEIR FRAMEWORK CODE!

"""
    # Complete the function below.

    def  maxStep(n, k):

    f = open(os.environ['OUTPUT_PATH'], 'w')


    _n = int(raw_input());


    _k = int(raw_input());

    res = maxStep(_n, _k);
    f.write(str(res) + "\n")

    f.close()

"""


# *******************************************************************************************************
# TODO:  following is Java 1.8 boilerplate!

"""
    public static void main(String[] args) throws IOException{
        Scanner in = new Scanner(System.in);
        final String fileName = System.getenv("OUTPUT_PATH");
        BufferedWriter bw = new BufferedWriter(new FileWriter(fileName));
        int res;
        int _n;
        _n = Integer.parseInt(in.nextLine().trim());

        int _k;
        _k = Integer.parseInt(in.nextLine().trim());

        res = maxStep(_n, _k);
        bw.write(String.valueOf(res));
        bw.newLine();

        bw.close();
    }

"""