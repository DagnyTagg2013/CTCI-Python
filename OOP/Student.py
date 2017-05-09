
# ATTN:
# 1) SLICE is a SHALLOW-COPY of List CONTAINER
# - see Stack Overflow:  Python how-to-clone-or-copy-a-list (including CONTENTs)
# 2) Python acts like:
#    - call by REFERENCE when MUTABLE argument passed in (CALLER var contents CHANGED on function return)
# ---- call by VALUE when IMMUTABLE type passed in (CALLER var contents UNCHANGED on function return)
# - see Jeff Knupp:  is-python-callbyvalue-or-callbyreference-neither
# 3) Python


from copy import deepcopy

class Student:

    # ATTN:  DEEP COPY vs REFERENCE-to-SAME!  Need to EXPLICITLY Call ctor to construct!
    def __init__(self, id, first, last, scores):
        self.id = int(id)
        self.firstName = str(first)
        self.lastName = str(last)
        # note:  following is needed to copy INTERNAL data ini addtion to above!
        self.scores = deepcopy(scores)

