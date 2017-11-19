import csv
import os
import numpy as np

class Edge(object):

    def __init__(self, graph, id, n1Id, n2Id, pageId):
        self.graph = graph
        self.id = id
        self.node1 = min(n1Id, n2Id)
        self.node2 = max(n1Id, n2Id)
        self.pageId = pageId
        self.perPageCrossedEdges = dict()
        self.resetCrossings()
        
    def resetCrossings(self):
        for page in range(len(self.graph.pages)):
            self.perPageCrossedEdges[page] = set()

    def addCrossing(self, otherEdgeId):
        #totalDiff = 0
        otherEdge = self.graph.edgeList[otherEdgeId]
        pageId = otherEdge.pageId
        #if not otherEdgeId in self.getCrossingSetForPage(pageId):
        self.perPageCrossedEdges[pageId].add(otherEdgeId)
        #totalDiff += 1
        #if not self.id in otherEdge.getCrossingSetForPage(pageId):
        otherEdge.perPageCrossedEdges[self.pageId].add(self.id)
        #totalDiff += 1

        #return totalDiff

    def moveToPage(self, oldPageId, newPageId):
        for page, crossings in self.perPageCrossedEdges.items():
            for otherId in crossings:
                other = self.graph.edgeList[otherId]
                other.moveCrossing(self.id, oldPageId, newPageId)

    def moveCrossing(self, edgeId, oldPageId, newPageId):
        self.perPageCrossedEdges[oldPageId].remove(edgeId)
        self.perPageCrossedEdges[newPageId].add(edgeId)

    def getCrossingSetForPage(self, pageId):
        return self.perPageCrossedEdges[pageId]

    def toTuple(self):
        return (self.node1, self.node2, self.pageId)

    def length(self):
        return abs(self.graph.nodeIdToIndex[self.node1] - self.graph.nodeIdToIndex[self.node2])

#     def __eq__(self, other):
#         if type(other)==Edge:
#             otherid=other.id
#         return self.id == other

    def __hash__(self):
        return self.id
