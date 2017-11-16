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

