__author__ = 'dagny t'

# Implement MOST FREQUENTLY USED  (Prioritize by COUNT of Accesses)

# TODO:  use deque collection! with MOST FREQUENT ACCESSED on one side, LEAST FREQUENT ACCESSED on ANOTHER
# - https://docs.python.org/2/library/collections.html#collections.deque
# TODO:  OR use Priority Queue collection => this reduces time to FIND
# - http://boltons.readthedocs.io/en/latest/queueutils.
# TODO:  use Dict to MAP from KEY of Item direct to Node Element on the Queue!

# - Use a priority queue (for maintaining fast access to MFU item)
# => PYTHON COLLECTION for this missing:
# - http://boltons.readthedocs.io/en/latest/queueutils.html
# - then a hash map (for providing fast access to any item by its key)

class Node:

    # ATTN:
    # - remember __ for ctor
    # - remember self
    # - OK to just reference self elements for declaration
    def __init__(self, key, value):
        self.key = key
        self.numAccesses = 0
        self.value = value


