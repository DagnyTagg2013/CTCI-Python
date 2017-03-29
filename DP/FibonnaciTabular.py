

# ALGO:  - BOTTOM-UP;
#        - LOOPING with look-back to refer to prior-saved values
#        - this then eliminates OVERLAPPING subtree calls!

def fibonacci(n):

    # array declaration -1
    f = [-1] * (n + 1)

    # base case assignments
    f[0] = 0
    f[1] = 1

    # NOTE:  need to GENERATE to range (n+1)
    for i in xrange(2, n + 1):
        f[i] = f[i-1] + f[i-2]

    return f

# DRIVER script:
n = 6
print(fibonacci(n))