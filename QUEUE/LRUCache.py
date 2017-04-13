
# IMPLEMENT LAST RECENTLY USED CACHE (Prioritize by Timestamp)

# - http://softwareengineering.stackexchange.com/questions/70602/most-efficient-cache-replacement-algorithm
# - http://stackoverflow.com/questions/21117636/how-to-implement-a-least-frequently-used-lfu-cache
# - https://www.quora.com/What-is-the-best-way-to-Implement-an-LRU-Cache

"""
ADD - O(logN)

You need key for referring to an item. You need numAccesses as a key for priority queue.
You need currentPos to be able to quickly find a pq position of item by key.
Now you organize hash map (key(Integer) -> node(Node<T>)) to quickly access items a
nd min heap-based priority queue using number of accesses as priority. Now you can very quickly perform all operations
(access, add new item, update number of acceses, remove lfu).
You need to write each operation carefully, so that it maintains all the nodes consistent
(their number of accesses, their position in pq and there existence in hash map).
All operations will work with constant average time complexity which is what you expect from cache.

"""

