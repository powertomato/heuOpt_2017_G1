from model.graph import *

def constructSolutionGreedyLeastCrossings(graph):
    unassigned = graph.getEdges()
    count = 0
    for edge in unassigned:
        count +=1
        page = 0
        lp = leastCrossingPage(graph, edge)
        if(count % 100 == 0):
            print(count)
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

