#!/bin/python

import sys
import os

# RECURSIVE PATH-POSSIBILITIES
# - n is MAX TOTAL number of moves
# - @ each move can STAY at current step (start from 0) or hop (+i) where i is current move number
# - returns MAX step reached across ALL possible move paths
# - CANNOT land on BLOCKED step given by K
# - e.g. 2,2 => 3
#   e.g. 3,3 => 5
def  maxStep(n, k):

    currStep = 0;  # POSITION is 0th step
    currMove = 1;  # MOVE is DELTA from currStep to get to nextStep

    (validPath, maxStepForPath) = maxStepRecurse(currMove, currStep, k, n)

    return maxStepForPath

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