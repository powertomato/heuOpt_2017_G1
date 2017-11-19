from model.graph import *
from numpy import random
import operator

def constructSolutionGreedyLeastCrossings(graph, randomized):
    unassigned = None

    if(randomized):
        unassigned = random.permutation(graph.getEdges())
    else:
        # edge sorting (testing showed no clear improvement)
        # lengths = {}
        # i = 0
        # for edge in graph.getEdges():
        #     lengths[i] = edge.length()
        #     i += 1
        #
        # sorted_lengths = sorted(lengths.items(), key=operator.itemgetter(1))
        # sorted_lengths.reverse()
        #
        # unassigned = []
        # edges = graph.getEdges()
        # for l in sorted_lengths:
        #     unassigned.append(edges[l[0]])
        #     print(l[0], l[1])

        unassigned = graph.getEdges() # dont sort


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

