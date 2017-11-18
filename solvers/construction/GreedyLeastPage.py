from model.graph import *
from numpy import random

def constructSolutionGreedyLeastCrossings(graph, randomized):
    unassigned = None
    if(randomized):
        unassigned = random.permutation(graph.getEdges())
    else:
        unassigned = graph.getEdges()

    count = 0
    for edge in unassigned:
        count +=1
        page = 0
        lp = leastCrossingPage(graph, edge)
        graph.moveEdgeToPage(edge, lp)

def leastCrossingPage(graph, edge):
    page = 0

    numCrossings = graph.numCrossingsIfAddedToPage(edge, page)
    for p in range(graph.pageNumber):
        numCr = graph.numCrossingsIfAddedToPage(edge, p)
        numCrossings = min(numCrossings, numCr)
        if numCr == numCrossings:
            page = p
        if numCr == 0:
            return page

    return page

