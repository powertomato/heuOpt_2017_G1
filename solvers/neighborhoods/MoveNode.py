
from solvers.neighborhoods.Neighborhood import Neighborhood
import math
import itertools, random
from collections import Counter

class MoveNodeCandidate(object):
    def __init__(self, graph, nodeIdx, target):
        self.nodeIdx = nodeIdx
        self.target = target
        self.graph = graph
    
    def _calcIndexAfterMove(self, idx):
        
        if idx == self.nodeIdx:
                return self.target
        
        if self.target > self.nodeIdx:
            if idx > self.nodeIdx and idx <= self.target:
                return idx - 1
        else:
            if idx < self.nodeIdx and idx >= self.target:
                return idx + 1
            
        return idx
    
    def _calcEdgeIndexAfterMove(self, edge):
        return ( self._calcIndexAfterMove(self.graph.nodeIdToIndex[edge.node1]), 
                self._calcIndexAfterMove(self.graph.nodeIdToIndex[edge.node2]) )
        
    def _areEdgesCrossing(self, e1Idx, e2Idx):
        if (e1Idx[0] > e1Idx[1]):
            e1Idx = (e1Idx[1], e1Idx[0])
        
        if (e2Idx[0] > e2Idx[1]):
            e2Idx = (e2Idx[1], e2Idx[0])
        
        if e1Idx[0]>e2Idx[0]:
            e1Idx, e2Idx = e2Idx, e1Idx
            
        return e1Idx[0] < e2Idx[0] < e1Idx[1] < e2Idx[1]
        
    def numCrossings(self):
        numNewCrossings = 0
        numResolvedCrossings = 0
        movenode = self.graph.getNodeByIndex(self.nodeIdx)
        
        for edge in movenode.edges:
            edgeId = edge.id
            e1Idx = self._calcEdgeIndexAfterMove(edge)
            page = edge.pageId
            
            for edgeId2 in self.graph.getCrossingSetForPage(page,edgeId):
                edge2 = self.graph.edgeList[edgeId2]
            
                e2Idx = self._calcEdgeIndexAfterMove(edge2)

                if not self._areEdgesCrossing(e1Idx,e2Idx):
                    numResolvedCrossings+=1
                    
        if self.nodeIdx < self.target:
            noderange = range(self.nodeIdx+1, self.target+1)
        else:
            noderange = range(self.target, self.nodeIdx)
        
        for nodeIdx in noderange:
            node = self.graph.getNodeByIndex(nodeIdx)
                      
            for edge in movenode.edges:
                e1Idx = self._calcEdgeIndexAfterMove(edge)

                page = edge.pageId
                
                for edge2 in node.edges:
                    if page != edge2.pageId:
                        continue
                    e2Idx = self._calcEdgeIndexAfterMove(edge2)
                    
                    if self._areEdgesCrossing(e1Idx,e2Idx):
                        numNewCrossings+=1
        
        return self.graph.numCrossings() - numResolvedCrossings + numNewCrossings
    
    def graphUpdate(self):
        movenode = self.graph.getNodeByIndex(self.nodeIdx)
        
        for edge in movenode.edges:
            edgeId = edge.id
            e1Idx = self._calcEdgeIndexAfterMove(edge)

            page = edge.pageId
            crossings = self.graph.getCrossingSetForPage(page,edgeId)
            
            toremove = set()
            for edgeId2 in crossings:
                edge2 = self.graph.edgeList[edgeId2]
            
                e2Idx = self._calcEdgeIndexAfterMove(edge2)
                
                crossings2 = self.graph.getCrossingSetForPage(page,edgeId2)
                
                if not  self._areEdgesCrossing(e1Idx,e2Idx):
                    toremove.add(edgeId2)
                    crossings2.remove(edgeId)
                    
            crossings.difference_update(toremove)
                    
        if self.nodeIdx < self.target:
            noderange = range(self.nodeIdx+1, self.target+1)
        else:
            noderange = range(self.target, self.nodeIdx)
        
        for nodeIdx in noderange:
            node = self.graph.getNodeByIndex(nodeIdx)
                      
            for edge in movenode.edges:
                edgeId = edge.id
                e1Idx = self._calcEdgeIndexAfterMove(edge)

                page = edge.pageId
                crossings = self.graph.getCrossingSetForPage(page,edgeId)
                
                for edge2 in node.edges:
                    edgeId2 = edge2.id
                    
                    if page != edge2.pageId:
                        continue
                    e2Idx = self._calcEdgeIndexAfterMove(edge2)
                    
                    crossings2 = self.graph.getCrossingSetForPage(page,edgeId2)
                    
                    if self._areEdgesCrossing(e1Idx,e2Idx):
                        crossings.add(edgeId2)
                        crossings2.add(edgeId)
        
        if self.nodeIdx < self.target:
            noderange = range(self.nodeIdx+1, self.target+1)
            indexShift = -1
        else:
            noderange = range(self.target, self.nodeIdx)
            indexShift = 1
        for i in noderange:
            node = self.graph.getNodeByIndex(i)
            self.graph.nodeIdToIndex[node.id] = i+indexShift

        node = self.graph.getNodeByIndex(self.nodeIdx)
        self.graph.nodeIdToIndex[node.id] = self.target

        if self.nodeIdx < self.target:
            a = self.graph.nodes
            i = self.nodeIdx
            t = self.target
            self.graph.nodes = a[0:i] + a[i+1:t+1] + [a[i]] + a[t+1:]
        else:
            a = self.graph.nodes
            i = self.nodeIdx
            t = self.target
            self.graph.nodes = a[0:t] + [a[i]] + a[t:i] + a[i+1:]

class MoveNode(Neighborhood):
    def __init__(self, strategy, evaluator):
        super(MoveNode, self).__init__(strategy, evaluator)
        
    def generateRandom(self, x):
        while True:
            n1 = random.randint(0, len(x.nodes)-1)
            n2 = -1
            while n1==n2:
                n2 = random.randint(0, len(x.nodes)-1)
            
            yield MoveNodeCandidate(x, n1, n2)
        
    def generateSingle(self, x):
        for n1 in range(len(x.nodes)):
            for n2 in range(len(x.nodes)):
                if n1==n2:
                    continue
                yield MoveNodeCandidate(x, n1, n2)