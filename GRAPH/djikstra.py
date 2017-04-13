__author__ = 'dagny t'


# FUNDAMENTALs of DJIKSTRA:
# - http://www.geeksforgeeks.org/greedy-algorithms-set-6-dijkstras-shortest-path-algorithm/
# PYTHON COLLECTIONS:
# - http://interactivepython.org/courselib/static/pythonds/Graphs/DijkstrasAlgorithm.html
# IDEA INSTALLING PACKAGES:
# - https://www.jetbrains.com/help/pycharm/2016.3/installing-uninstalling-and-upgrading-packages.html
# - FILE/DEFAULT SETTINGS/PROJECT INTERPRETER/+/pythonds
# - https://pypi.python.org/pypi/pythonds

# ATTN:  needed COLLECTION classes with simplified APIs!
# TODO:  check if usage of 'collections' package is better!
import sys
from pythonds.graphs import PriorityQueue, Graph, Vertex

def dijkstra(aGraph, originPt):

    unvisitedPriorityQ = PriorityQueue()
    originPt.setDistance(0)
    # init with TUPLE of CUMULATIVE distance from Origin TO given unvisited point
    unvisitedPriorityQ.buildHeap([(unvisitedPt.getDistance(),unvisitedPt) for unvisitedPt in aGraph])

    while not unvisitedPriorityQ.isEmpty():
        # ATTN:  next nearest point can be attached to ANY point in already VisitedShortestPathPoints
        #        where MULTIPLE PARALLEDLSHORTEST PATHs from ORIGIN are supported;
        #        and which has the MIN Cumulative distance calculated from Origin SO FAR!
        # ATTN:  this just CONSUMEs next nearest point; SHRINKING unVisited points set!
        nextNearestPt = unvisitedPriorityQ.delMin()
        for adjacentPt in nextNearestPt.getConnections():
            # ATTN:  *.getWeight() gets weight on EDGE between points
            #        *.getDistance() gets CUMULATIVE distance from Origin TO point
            nextAdjacentPtUpdatedCumDist =  nextNearestPt.getDistance() \
                                          + nextNearestPt.getWeight(adjacentPt)
            # ATTN:  only update cumulative distance on adjacent Point to priority NEXT NEAREST POINT IFF
            #        cumulative distance from origin to this adjacent Point is LESS than current cum dist on adjacent Point!
            if  nextAdjacentPtUpdatedCumDist < adjacentPt.getDistance():
                adjacentPt.setDistance( nextAdjacentPtUpdatedCumDist)
                # ATTN:  - sets predecessor to BUILD one PARALLEL SHORTEST PATH LINKs!
                adjacentPt.setPred(nextNearestPt)
                # ATTN:  - this adjusts cumulative distance on adjacent point to new-calculated MIN,
                #          then heapifies it to maintain Priority Queue property!
                # ESSENTIALLY:  the ITERATIVE UPDATE of STATE before considering NEXT Unvisited Point by Cumulative Distance Priority
                unvisitedPriorityQ.decreaseKey(adjacentPt, nextAdjacentPtUpdatedCumDist)

def main(args):

    # TODO:  add proper TESTs to initialize Graph and Vertex with example from GeeksForGeeks!
    x = 1

# NOTE:  use the following to permit in-module unit-testing!
# ATTENTION:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    main(sys.argv)