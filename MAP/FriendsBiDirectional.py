__author__ = 'dagny t'

"""

APPROACH:
- scan employees into dictionary-map keyed by empId
- scan in friends links, and accumulate to the above
- scan in friends links again; but REVERSE the lookup in the other direction, to accumulate to the above

*** NOT SURE:  check complexities below on what to count!

TIME-COMPLEXITY:
O(M) + O(N)
- scan in Employees => DRIVER as can have None links for friendships!
- 2 x scan in Friends links for each direction (N)
- O(1) to lookup elements for association
HOWEVER N can equal Mexp2 in WORST case where each friend is friends with ALL other employees!

SPACE-COMPLEXITY:
O(M) + O(N)
- scan in Employees (M)
- scan in Friends links (N)
HOWEVER N can be as large as Mexp2 in WORST case where each friend is friends with ALL other employees!

"""

"""
def say_hello():
    print 'Hello, World'
"""

# for i in xrange(5):
#     say_hello()


#
# Your previous Plain Text content is preserved below:
#
# You have data for social network on who is friends with whom.
# You need to write a function that returns this data in the form of an adjacency list representation, i.e. a mapping of each employee ID to a list of his/her friends on the site
# #
# You have two input data sets to work with. The first data set is the employees at your company, and the second is all the pairs of employees who are virtually friends so far. It does not matter which employee's ID is in which column, the friendships are bidirectional.
#
# employees_input = [
#   "1,Richard,Engineering",
#   "2,Erlich,HR",
#   "3,Monica,Business",
#   "4,Dinesh,Engineering",
#   "6,Carla,Engineering",
# ]
#
# friendships_input = [
#   "1,2",
#   "1,3",
#   "2,4",
# ]
#
# Answers: (Format does not matter)
# 1: 2, 3
# 2: 1, 4
# 3: 1
# 4: 2
# 6: None
#

# def getAllFriendsByEmployee(employees, friendships):

employees = [
 "1,Richard,Engineering",
 "2,Erlich,HR",
 "3,Monica,Business",
 "4,Dinesh,Engineering",
 "6,Carla,Engineering",
]

friendships = [
  "1,2",
  "1,3",
  "2,4"
]

# TODO:  make a load function here!
allFriendsByEmp = {}

for employee in employees:
    emp_info = employee.split(',')
    print emp_info[0]
    allFriendsByEmp[int(emp_info[0])] = None

print allFriendsByEmp

"""
for edge in friendships:
    edge_info = edge.split(',')
    print edge_info[1]
    allFriendsForEmp = allFriendsByEmp.get(int(edge_info[0]), None)
    print "LIST found for BUCKET {} is:  {}".format(edge_info[0], allFriendsForEmp)
    if (allFriendsForEmp is None):
        allFriendsForEmp = [ int(edge_info[1]) ]
    else:
        # TODO: lookup if extend better
        allFriendsForEmp.append( int(edge_info[1]) )
    key = int(edge_info[0])
    # print "KEY is {}".format(key)
    allFriendsByEmp[key] = allFriendsForEmp

print allFriendsByEmp
"""

# source is KEY for emp to attach to
# to is friend
def accumFriendsAnyDir(accumMap, edges, source, dest):

    for edge in friendships:

        edge_info = edge.split(',')

        allFriendsForEmp = allFriendsByEmp.get(int(edge_info[source]), None)

        if (allFriendsForEmp is None):
            allFriendsForEmp = [ int(edge_info[dest]) ]
        else:
            # TODO: lookup if extend better
            allFriendsForEmp.append( int(edge_info[dest]) )
        key = int(edge_info[source])

        allFriendsByEmp[key] = allFriendsForEmp


# MAJOR BIG-DEAL:  this symmetrical mapping parameterizes the bi-directional friends relationship
accumFriendsAnyDir(allFriendsByEmp, friendships, 0, 1)
print allFriendsByEmp
accumFriendsAnyDir(allFriendsByEmp, friendships, 1, 0)
print allFriendsByEmp