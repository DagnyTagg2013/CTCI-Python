
# NOTE: TRICKY for PYTHON!
# http://stackoverflow.com/questions/3463746/in-place-string-modifications-in-python
# need to use MUTABLE LIST or BYTE array!

print "TEST1:  reverse one word, without given indices"
# CASE 1:  Single Word, Odd Num chars
def reverseOneString(aString):

    revString = [None] * len(aString)
    endIdx = len(aString) - 1
    startIdx = 0

    while (startIdx <= endIdx):
        # recall Python SWAP
        tmp = aString[startIdx]
        revString[startIdx] = aString[endIdx]
        revString[endIdx] = tmp
        startIdx += 1
        endIdx -= 1

    return ''.join(revString)

print "TEST1a: reverse odd-char word"
test1 = "one"
print test1
rev1 = reverseOneString(test1)
print rev1

print "TEST1b:  reverse even-char word"
test2 = "four"
print test2
rev2 = reverseOneString(test2)
print rev2

print "TEST2: find breaks in sentence with two words, one space sep"
# ATTN:  parameterize separator!
def findWordBreaks(sentence, sep):
    currStartIdx = 0
    currEndIdx = 0
    for aChar in sentence:
        if (aChar == sep):
            print (currStartIdx, (currEndIdx - 1))
            currStartIdx = (currEndIdx + 1)
        currEndIdx += 1
    print (currStartIdx, (currEndIdx - 1))

test3 = "one four"
print test3
findWordBreaks(test3, ' ')

print "TEST3:  reverse one String by index delimiters within large string"
# ATTN:  - need to return a SINGLE WORD, rather than WHOLE-STRING each time with just the ONE segment reversed;
#          as need to re-assemble later!
def reverseOneStringByIdx(aString, startIdx, endIdx):

    # ATTN:  Python need to CONVERT to LIST or BYTE ARRAY for MUTABILITY!
    # revChars = list(aString)
    # with ''.join(revChars) to CONVERT
    revChars = bytearray(aString[startIdx:(endIdx + 1)])

    # ATTN:  Idx for revChars tracked SEPARATELY! to get SEPARATE sub-word!
    revStartIdx = 0
    revEndIdx = (endIdx - startIdx)
    while (startIdx <= endIdx):
        # recall Python SWAP
        tmp = aString[startIdx]
        revChars[revStartIdx] = aString[endIdx]
        revChars[revEndIdx] = tmp
        startIdx += 1
        endIdx -= 1
        revStartIdx += 1
        revEndIdx -= 1

    # ATTN:  conversion of bytearray to String!
    return str(revChars)

test4 = "abc one def"
print test4
rev4 = reverseOneStringByIdx(test4, 4, 6)
print 'reverse one string by Idx:  ' + rev4

print "TEST4:  reverse full sentence"
def revSentence(sentence, lambdaOpOnWord, sep):

    # REVERSED SENTENCE
    revResult = []

    # FIRST REV WHOLE SENTENCE
    wholeRev = reverseOneString(sentence)
    print wholeRev

    # FIND EACH BREAK, then apply REVERSE on EACH Word by Idx Bounds
    currStartIdx = 0
    currEndIdx = 0
    for aChar in wholeRev:
        if (aChar == ' '):
            # print (currStartIdx, (currEndIdx - 1))
            revWord = lambdaOpOnWord(wholeRev, currStartIdx, (currEndIdx - 1))
            print revWord
            # ATTN: add space-sep!
            # TODO:  detect FIRST SPACE is not needed
            revResult.append(sep)
            revResult.append(revWord)
            currStartIdx = (currEndIdx + 1)
        currEndIdx += 1

    revWord = lambdaOpOnWord(wholeRev, currStartIdx, (currEndIdx - 1))
    revResult.append(sep)
    revResult.append(revWord)

    return ''.join(revResult)

test5 = "the quick brown fox"
print test5
rev5 = revSentence(test5, reverseOneStringByIdx, ' ')
print rev5