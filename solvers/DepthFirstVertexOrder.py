from solvers.helper import _edges
from model.graph import *

def constructVertexOrderDFS(graph):
    nodes = []
    stack = [graph.nodes[0]]

    while stack:
        cur_node = stack[0]

        stack = stack[1:]
        if cur_node.id not in nodes:
            nodes.append(cur_node.id)

        rev = cur_node.getNeighbours()
        rev.reverse()
        for child in rev:
            if child.id not in nodes:
                stack.insert(0, child)

    print(nodes)

    constructSolutionGreedyLeastCrossings(graph)

    graph.reorder(nodes)

    constructSolutionGreedyLeastCrossings(graph)

    return nodes

def constructSolutionGreedyLeastCrossings(graph):
    unassigned = list(_edges(graph.pages))
    graph.pages = {}
    for i in range(graph.pageNumber):
        graph.pages[i] = set()
    count = 0
    for edge in unassigned:
        count +=1
        page = 0
        lp = leastCrossingPage(graph, edge)
        #print(lp, count, len(unassigned))
        graph.addEdge(edge[0],edge[1],lp)

    print("crossings:", graph.numCrossings())

def leastCrossingPage(graph, edge):
    page = 0
    minimum = graph.numCrossingsIfAddedToPage(edge[0],edge[1], page)
    for p in graph.pages:
        candidate = graph.numCrossingsIfAddedToPage(edge[0],edge[1], p)
        if candidate < minimum:
            minimum = candidate
            page = p

    return page

