#
# ALGO:
# - letter occurrences via map
#
# DICTIONARY usage:
# - http://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python
# - http://stackoverflow.com/questions/11041405/why-dict-getkey-instead-of-dictkey
# - comparing ditionary values
def normWordToCode(word):

    # init dictionary
    code = {}

    # NOTE: iterable word!
    for aChar in word:

        # ATTN:  to protect against KeyError, provide DEFAULT NONE
        currCount = code.get(aChar, None)
        # currCount = code[aChar]

        if (currCount == None):
            code[aChar] = 1
        else:
            code[aChar] += 1

    return code

def isAnagram(word1, word2):

    # ATTN:  handle case and weird chars!
    lhs = word1.strip().lower()
    rhs = word2.strip().lower()

    code1 = normWordToCode(lhs)

    code2 = normWordToCode(rhs)

    return code1 == code2


# main script code here!

# TEST 1:  anagrams
word1 = 'amp'
word2 = 'pam'
test1 = isAnagram(word1, word2)
print test1

# TEST 2: NOT anagrams
word1 = "base"
word2 = "camp"
test2 = isAnagram(word1, word2)
print test2

# TEST 3:  see entries
code2 = normWordToCode(word2)
keys = code2.keys()
values = code2.values()
entries = code2.items()

for x in entries:
    print x

# NOTE:  could also use OrderedDict!

