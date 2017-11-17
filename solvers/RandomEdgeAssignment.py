from model.graph import *
from numpy import random

def constructRandomEdgeAssignment(graph):
    unassigned = graph.getEdges()
    count = 0
    for edge in unassigned:
        count +=1
        rp = randomPage(graph)
        if(count % 100 == 0):
            print(count)
        graph.moveEdgeToPage(edge, rp)

def randomPage(graph):
    pages = graph.pageNumber

    return random.choice(range(pages))

