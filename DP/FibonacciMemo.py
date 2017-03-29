
# ALGO:  - TOP-DOWN;
#        - DEPTH-FIRST recursion with MEMO Lookup
#        - this then eliminates overlapping subtree calls!
#

def fib(n):

    #ATTN:  this requires ADDITONAL STORAGE space
    memo = [None] * (n + 1)  #NOTE:  +1 is for the 0th element

    _fib(n, memo)

    return memo

def _fib(n, memo):

    if (n <= 1):
        return n


