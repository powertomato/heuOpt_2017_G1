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

    def addCrossing(self, otherEdgeId):
        totalDiff = 0
        otherEdge = self.graph.edgeList[otherEdgeId]
        pageId = otherEdge.pageId
        if not otherEdgeId in self.getCrossingSetForPage(pageId):
            self.getCrossingSetForPage(pageId).add(otherEdgeId)
            totalDiff += 1
        if not self.id in otherEdge.getCrossingSetForPage(pageId):
            otherEdge.getCrossingSetForPage(self.pageId).add(self.id)
            totalDiff += 1

        return totalDiff

    def moveToPage(self, oldPageId, newPageId):
        for page, crossings in self.perPageCrossedEdges.items():
            for otherId in crossings:
                other = self.graph.edgeList[otherId]
                other.moveCrossing(self.id, oldPageId, newPageId)

    def moveCrossing(self, edgeId, oldPageId, newPageId):
        self.getCrossingSetForPage(oldPageId).remove(edgeId)
        self.getCrossingSetForPage(newPageId).add(edgeId)

    def getCrossingSetForPage(self, pageId):
        if pageId not in self.perPageCrossedEdges:
            self.perPageCrossedEdges[pageId] = set()

        return self.perPageCrossedEdges[pageId]

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id