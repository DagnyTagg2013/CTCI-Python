"""
PROBLEM:  For all 7-digit phone numbers; find the valid word phrases which can be created from it (Order Matters)
GIVEN:    Dict/Map of Number to Letter Set (on Phone Pad); then Dict/Map of Valid Words
INPUT:    NONE; generate all permutations of 7-digit phone numbers
OUTPUT:   Valid word phrases
"""

"""

SOLUTION:

 - DATA STRUCTURE:  NESTED MAP/DICT modeling each Digit position as a Node, with Children corresponding to number of individual letters that Digit maps to
 - ALGO:  BREADTH-first recursive search, TEST against words found, ABORT recursion for PATH if INVALID word found
 - TEST against dictionary to determine if word found; APPEND foundSentence for THAT specific path, OR keep looking for valid word!
 - STEP down each Digit position to ITERATIVELY-BUILD EACH possible partial-phrase
 - STOP when 7th position processed

CASES:

 - SIMPLEST CASE: GIVEN a KNOWN 7-digit number
 - GENERAL CASE:  GENERATE all permutations of 7-digit numbers
 - STRUCTURE:  TRIE or Map of Nested Maps; FIRST dimension corresponds to Digit Position in phone number, and SECOND dimension corresponds to Letter Sets for Digit

CLARIFICATIONS:

 - zero and one do not map to Letters
 - DUPLICATE letters are allowed
 - ORDER is important
 - must use ALL letters in Number for VALID words, otherwise DISCARD as INVALID

SIMPLIFYING ASSUMPTIONS:

 - what to do if longer word found AFTER shorter word?  SIMPLIFY to find MAX Word length allowed, before starting to find the NEXT word

PROBLEMS:

EXPONENTIAL possibilities!

- what to do if MULTTIPLE POSSIBLE words found AFTER found for CURRENT word; THEN need to CACHE ALL POSSIBLE SENTENCES by WORD possibilities?
- CRAZY EXPONENTIAL time complexity; and instead handle with iteration?

ONLINE:
 - http://www.geeksforgeeks.org/find-possible-words-phone-digits/
 - https://www.careercup.com/question?id=13027671
 - https://www.careercup.com/question?id=15423772

"""

"""
TODO on PYTHON:
- https://learnpythonthehardway.org/book/ex40.html
- http://stackoverflow.com/questions/3961007/passing-an-array-list-into-python
- http://www.thegeekstuff.com/2013/06/python-list/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+TheGeekStuff+(The+Geek+Stuff)
- http://softwareengineering.stackexchange.com/questions/306092/what-are-class-methods-and-instance-methods-in-python
- http://stackoverflow.com/questions/6990099/explaining-the-python-self-variable-to-a-beginner
- http://stackoverflow.com/questions/22492162/understanding-the-main-method-of-python
- http://stackoverflow.com/questions/132988/is-there-a-difference-between-and-is-in-python
- http://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-pytho
- http://stackoverflow.com/questions/2225038/determine-the-type-of-a-python-object (IS-INSTACE vs TYPE)
- http://stackoverflow.com/questions/1316887/what-is-the-most-efficient-string-concatenation-method-in-python
- https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/
- http://stackoverflow.com/questions/104420/how-to-generate-all-permutations-of-a-list-in-python
- http://www.openbookproject.net/books/bpp4awd/ch03.html
- http://stackoverflow.com/questions/625083/python-init-and-self-what-do-they-do
- http://stackoverflow.com/questions/1323410/has-key-or-in
- http://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index-in-python
"""

import sys


class PhoneWords:

    # ATTN:  IDENTIFY CONST INPUT DATA STRUCTURES
    MAX_NUM_LENGTH = 3  # where currentDigit STARTs from 0
    MAX_WORD_LENGTH = 3

    # ATTN:  initialize Numeric Pad to Letters
    noneLetters = None
    twoLetters = ['A', 'B', 'C']
    threeLetters = ['D', 'E', 'F']
    fourLetters = ['G', 'H', 'I']
    fiveLetters = ['J', 'K', 'L']
    sixLetters = ['M', 'N', 'O']
    sevenLetters = ['P', 'Q', 'R', 'S']
    eightLetters = ['T', 'U', 'V']
    nineLetters = ['W', 'X', 'Y', 'Z']

    numToBatchLetters = {
        0: noneLetters,
        1: noneLetters,
        2: twoLetters,
        3: threeLetters,
        4: fourLetters,
        5: fiveLetters,
        6: sixLetters,
        7: sevenLetters,
        8: eightLetters,
        9: nineLetters
    }

    # ATTN:  initialize ValidWords
    validWords = {'BAT': 1,
                  'FED': 2,
                  'RUB': 3,
                  'A': 4,
                  'THE': 5,
                  'ROCKS': 6,
                  'ON': 7
                  }

    # instance method, ctor
    def __init__(self):
        self.numValidWordsFound = 0

    # ATTN:  Python does NOT have a function return type!
    # instance method
    def generateWords(self, phoneNumber, currentDigit, accumWord):

        # EXIT recursion at LAST digit
        if (currentDigit == PhoneWords.MAX_NUM_LENGTH):
            builtWord = ''.join(accumWord)
            if builtWord in PhoneWords.validWords:
                print "ACCEPT TEST WORD:  {}".format(builtWord)
                return accumWord
            else:
                print "REJECT TEST WORD:  {}".format(builtWord)
                return None

        # ITERATE through EACH of the LETTER possibilities for currentDigit
        lettersPossible = PhoneWords.numToBatchLetters[phoneNumber[currentDigit]]
        for aLetter in lettersPossible:
            accumWord.extend(aLetter)
            # ATTN:  Python doesn't support postincr!
            currentDigit += 1
            self.generateWords(phoneNumber, currentDigit, accumWord)
            # BACK OUT currentDigit AND accumWord for NEXT loop iteration!
            currentDigit -= 1
            accumWord.pop(currentDigit)



# @staticmethod
def main(args):

    print ("WELCOME TO PHONE NUMBER MARKET PHRASES!")


    # ONE:  IDENTIFY BUILD DATA STRUCTURES
    # NOTE:  need to do ''.join(testPhrase) to generate String from Letter sequence!
    accumPhrases = {}
    MAX_PHONE_NUM_LENGTH = 7


    # EZ CASE 1:
    # - ASSUME 3 digit phone number length
    # - MAX letters for a valid word is @classmethod
    # - RETURN VALID WORD FOUND, or None
    phoneNumber = [2, 2, 8]
    accumWord = []
    currentDigit = 0
    # ATTN:  Python hasn't got CONST vars, and this can be modified as below
    PhoneWords.MAX_WORD_LENGTH = 3

    # invocation of instance method
    foundValidWord = PhoneWords().generateWords(phoneNumber, currentDigit, accumWord)


# TODO:  review this variable notation again!
# ATTN:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    # invocation of static class method
    # PhoneWords.main(sys.argv)
    main(sys.argv)
