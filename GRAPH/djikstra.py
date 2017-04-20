
__author__ = 'dagny t'

import logging

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
        #nextNearestPt = unvisitedPriorityQ[0]
        nextNearestPt = unvisitedPriorityQ.delMin()
        # TODO DEBUG:  need to find out why 0th point of internal heapArray not removed and set to nextNearestPt by Distance of 0!
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

    # print type(Graph)
    # print dir(Graph)

    # print type(Vertex)
    # print dir(Vertex)
    # help(Vertex.__init__)

    # print dir(PriorityQueue)

    vertex0 = Vertex(0)
    vertex0.setDistance(0)
    # print vertex0

    vertex1 = Vertex(1)
    # print vertex1

    vertex7 = Vertex(7)
    # print vertex7

    vertex2 = Vertex(2)
    # print vertex2

    graph1 = Graph()
    graph1.addVertex(vertex0)
    graph1.addVertex(vertex1)
    graph1.addVertex(vertex7)
    graph1.addVertex(vertex2)

    print 'Initialized Vertex Dump:'
    # for aVertex in graph1.getVertices():
    #     print aVertex

    print 'Initialized Edges Dump:'
    graph1.addEdge(vertex0, vertex1, 4)
    graph1.addEdge(vertex0, vertex7, 8)
    graph1.addEdge(vertex1, vertex2, 8)

    print 'Vertex Sequenced after Djikstra from starting point with key 0'
    try:
        dijkstra(graph1, vertex0)
        for aVertex in graph1.getVertices():
            print aVertex
    except Exception as ex:
        logging.exception("BURP!")

# NOTE:  use the following to permit in-module unit-testing!
# ATTENTION:  main entrypoint, for Python to emulate Java main entrypoint
if __name__ == '__main__':
    main(sys.argv)

