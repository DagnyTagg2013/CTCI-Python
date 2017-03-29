

# ALGO:  - ITERATION with LOOK-BACK buffer for just TWO trailing elements
#        - BEATs EXPONENTIAL RECURSION!
#        - O(N) LINEAR complexity
def fibonacci(n):

    # Write your code here.
    f0 = 1
    f1 = 1

    # if n == 0 or 1, EXIT
    if (n == 0) or (n == 1):
        return 1

    # ATTN:  INITIALIZE FIRST TWO values to 1; then set index to START at 2,
    #        init fib result ALSO
    i = 2
    fib = -1

    # ATTN:  us for with xrange as more efficient to iterate!
    for i in xrange(2, n):
        fib = f0 + f1
        f0 = f1
        f1 = fib

    return fib

# n = int(raw_input())
n = 5
print(fibonacci(n))
