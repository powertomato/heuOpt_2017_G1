
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
        crossingsOld = self.graph.getCrossingSetForPage(self.oldpage, self.id)
        crossingsNew = self.graph.getCrossingSetForPage(self.newpage, self.id) 
        return self.graph.numCrossings() - len(crossingsOld) + len(crossingsNew)
    
    def graphUpdate(self):
        self.graph.pages[self.oldpage].removeEdge(self.graph.getEdge(self.id))
        self.graph.pages[self.newpage].addEdge(self.graph.getEdge(self.id))
        return self.graph
        

class EdgePageMove(Neighborhood):
    def __init__(self, strategy, evaluator):
        super(EdgePageMove, self).__init__(strategy, evaluator)
        
    def generateRandom(self, x):
        while True:
            p1 = random.randint(0, len(x.pages)-1)
            p2 = -1
            id = random.randint(0, len(x.edgeList)-1)
            while p1==p2:
                p2 = random.randint(0, len(x.pages)-1)
            
            yield EdgePageMoveCandidate(x, id, p1, p2)
        
    def generateSingle(self, x):
        for p1, page1 in enumerate(x.pages):
            for edgeId in range(len(page1.edges)):
                for p2,page2 in enumerate(x.pages):
                    if p1==p2:
                        continue
                    yield EdgePageMoveCandidate(x, edgeId, p1, p2)
                    