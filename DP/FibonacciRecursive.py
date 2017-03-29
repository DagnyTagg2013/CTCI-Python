
# SUPERBAD complexity:
# - exponential complexity
# - 2-branch TREE, with overlapping subproblems with 2^n nodes at each level, starting with root level 0
#   so complexity counts ALL nodes:
#   => O(2^n) for asymptotic as 50% nodes are at the LEAF level

def fib(n):

    if (n <= 1):
        return n

    result = fib(n-1) + fib(n-2)

    return result

# Driver
n = 5
print fib(n)