
from solvers.neighborhoods.Neighborhood import Neighborhood
import math
import itertools, random
from collections import Counter

class EdgePageMoveCandidate(object):
    def __init__(self, graph, id, oldpage, newpage):
        self.graph = graph
        self.id = id
        self.oldpage = oldpage
        self.newpage = newpage
        
    def numCrossings(self):
        crossingsOld = self.graph.edgeList[self.id].perPageCrossedEdges[self.oldpage]
        crossingsNew = self.graph.edgeList[self.id].perPageCrossedEdges[self.newpage] 
        return self.graph.numCrossings() - len(crossingsOld) + len(crossingsNew)
    
    def graphUpdate(self):
        self.graph.moveEdgeToPage(self.graph.getEdge(self.id), self.newpage)
        return self.graph
        

class EdgePageMove(Neighborhood):
    def __init__(self, strategy, evaluator):
        super(EdgePageMove, self).__init__(strategy, evaluator)
        
    def generateRandom(self, x):
        while True:
            p2 = random.randint(0, len(x.pages)-1)
            id = random.randint(0, len(x.edgeList)-1)
            p1 = x.edgeList[id].pageId
            
            yield EdgePageMoveCandidate(x, id, p2, p1)
        
    def generateSingle(self, x):
        for edge in x.edgeList:
            p1 = edge.pageId
            for p2, page1 in enumerate(x.pages):
                yield EdgePageMoveCandidate(x, edge.id, p1, p2)
                    