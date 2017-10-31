def constructSolutionFast(graph):
    unassigned = graph.getEdges()
    graph.pages = {}
    graph.pageNumber = 0
    for edge in unassigned:
        page = 0
        while not graph.canAddToPage(edge[0],edge[1], page):
            print("crossings:", graph.numCrossingsIfAddedToPage(edge[0],edge[1], page), "page:", page)
            page += 1
        graph.addEdge(edge[0],edge[1],page)
    