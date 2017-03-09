
# TODO:  test this in Python!
# ATTN:
# - QUICKSELECT or QUICKSORT in Python
# https://en.wikipedia.org/wiki/Quickselect

"""
 function partition(list, left, right, pivotIndex)
     pivotValue := list[pivotIndex]
     swap list[pivotIndex] and list[right]  // Move pivot to end
     storeIndex := left
     for i from left to right-1
         if list[i] < pivotValue
             swap list[storeIndex] and list[i]
             increment storeIndex
     swap list[right] and list[storeIndex]  // Move pivot to its final place
     return storeIndex

  // Returns the k-th smallest element of list within left..right inclusive
  // (i.e. left <= k <= right).
  // The search space within the array is changing for each round - but the list
  // is still the same size. Thus, k does not need to be updated with each round.
  function select(list, left, right, k)
     if left = right        // If the list contains only one element,
         return list[left]  // return that element
     pivotIndex  := ...     // select a pivotIndex between left and right,
                            // e.g., left + floor(rand() % (right - left + 1))
     pivotIndex  := partition(list, left, right, pivotIndex)
     // The pivot is in its final sorted position
     if k = pivotIndex
         return list[k]
     else if k < pivotIndex
         return select(list, left, pivotIndex - 1, k)
     else
         return select(list, pivotIndex + 1, right, k)
Note the resemblance to quicksort: just as the minimum-based selection algorithm is a partial selection sort, this is a partial quicksort, generating and partitioning only O(log n) of its O(n) partitions. This simple procedure has expected linear performance, and, like quicksort, has quite good performance in practice. It is also an in-place algorithm, requiring only constant memory overhead if tail-call optimization is available, or if eliminating the tail recursion with a loop:

 function select(list, left, right, k)
     loop
         if left = right
             return list[left]
         pivotIndex := ...     // select pivotIndex between left and right
         pivotIndex := partition(list, left, right, pivotIndex)
         if k = pivotIndex
             return list[k]
         else if k < pivotIndex
             right := pivotIndex - 1
         else
             left := pivotIndex + 1
"""