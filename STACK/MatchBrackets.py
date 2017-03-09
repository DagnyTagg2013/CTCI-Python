from collections import deque

# ATTN:
# deque is fast-implementation of Stack and Queue interface!
# - https://docs.python.org/2/library/collections.html
#
# TODO:
# - DOUBLY-LINKED LIST:  http://stackoverflow.com/questions/712429/plain-linked-and-double-linked-lists-when-and-why
# - Nobody mentioned my favorite linked list: circularly linked list with a pointer to the last element (AND prior to last for DEL)
# You get constant-time insertion and deletion at either end, plus constant-time destructive append.
# The only cost is that empty lists are a bit tricky.
# It's a sweet data structure: list, queue, and stack all in one.
# - Empty lists aren't tricky, you just have to waste an element in the circular list.
# That way you can always distinguish between an empty and full one.
from collections import deque
#
# ATTN:
# - Python DEQUE
# https://docs.python.org/2/library/collections.html#collections.deque
# http://stackoverflow.com/questions/5652278/python-2-7-how-to-check-if-a-deque-is-empty
# d[-1] peeks at RIGHTMOST item without removing it
# is not d essentially checks if empty

# - http://stackoverflow.com/questions/12548481/how-to-check-queue-length-in-python
# - Python has no switch statement:  http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
# - Python SET implementation:  http://www.python-course.eu/sets_frozensets.php
# - Python iteration over a String:  http://stackoverflow.com/questions/538346/iterating-over-a-string


# ALGO-TRICK: Use FIFO STACK to MATCH elements as they are read!
#             PUSH LEFT bracket
#             POP matched RIGHT bracket!
#             - ALSO, use DICTIONARY to get MATCH-PAIRs!

def isLeftBracket(aChar):
    # ATTN:  using SET!
    bracketSet = set("{([")
    return aChar in bracketSet

def isRightBracket(aChar):
    bracketSet = set("})]")
    return aChar in bracketSet

def is_matched(expression):

    # ATTN:  initializing dictionary or map!
    matchBrackets = {  '{':'}',
                       '[':']',
                       '(':')' }

    # ATTN:  allocate stackMatcher
    #        - using deque to append and pop from SAME side of queue for FIFO!
    stackMatcher = deque()
    discardNonBrackets = None
    isBalanced = True

    for aChar in expression:

        # determine when to PUSH LEFT brackets
        # TRICK:  IGNORE other chars we don't care to match on!
        if isLeftBracket(aChar):
            stackMatcher.append(aChar)

        # KEY POINT:  determine when to PEEK readOnly vs POP remove
        #             LEFT brackets ON FINDING match with CURRENT RIGHT bracket
        # ATTN: handle POP from EMPTY Stack case!
        if isRightBracket(aChar):

            # ATTN:  - simplest case is that LATEST stack item is a Bracket match;
            #        - OTHERWISE, have to keep POPPING until finding a LEFT bracket to TEST against
            #        - CAREFUL to CHECK for EMPTY stack BEFORE PEEK or POP on top element
            # while stackMatcher and not isLeftBracket(stackMatcher[-1]):
            #    discardNonBrackets = stackMatcher.pop()


            if not stackMatcher:
                # UNABLE to find any LEFT Bracket to match current RIGHT Bracket, EXIT
                isBalanced = False
                break

            if isLeftBracket(stackMatcher[-1]):
                if ( matchBrackets[stackMatcher[-1]] == aChar ):
                    # REMOVES this from consideration, as found BALANCED match
                    matchedLeftBracket = stackMatcher.pop()
                else:
                    # WRONG type of LEFT Bracket, non-matching, EXIT
                    isBalanced = False
                    break


        # ATTN: pass is Placeholder in Python!
        # pass

    # TRICK:
    # at the END of String, if we have maintained Balance AND consumed all matching brackets in stackMatcher, we are MATCHED
    # OTHERWISE, we are NOT
    isMatched = isBalanced and (not stackMatcher)

    return isMatched


# ATTN:  Simple Test Script!
print "\n***** TEST1:  {{]] isValid:\n"
print "{0}\n".format(is_matched("{{]]"))

print "\n***** TEST2:  {[]} isValid:\n"
print "{0}\n".format(is_matched("{[]}"))

print "\n***** TEST3:  EMPTY String isValid:\n"
print "{0}\n".format(is_matched(""))

print "\n***** TEST4:  [{ isValid:\n"
print "{0}\n".format(is_matched("[{"))

print "\n***** TEST5:  [ab{cd}] isValid:\n"
print "{0}\n".format(is_matched("[ab{cd}]"))

print "\n***** TEST6:  [ab{cd]} isValid:\n"
print "{0}\n".format(is_matched("[ab{cd]}"))

# ATTN:  raw_input() is stdin
# ATTN:  xrange() is lazy eval
# ATTN:  strip() is fast-clean
"""
t = int(raw_input().strip())
for a0 in xrange(t):
    expression = raw_input().strip()
    if is_matched(expression) == True:
        print "YES"
    else:
        print "NO"
"""