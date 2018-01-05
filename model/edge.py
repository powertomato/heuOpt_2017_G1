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
    
    def __lt__(self,other):
        if self.graph.nodeIdToIndex[self.node1] == self.graph.nodeIdToIndex[other.node1]:
            return self.graph.nodeIdToIndex[self.node2] < self.graph.nodeIdToIndex[other.node2]
        return self.graph.nodeIdToIndex[self.node1] < self.graph.nodeIdToIndex[other.node1]
        
    def __gt__(self,other):
        if self.graph.nodeIdToIndex[self.node1] == self.graph.nodeIdToIndex[other.node1]:
            return self.graph.nodeIdToIndex[self.node2] > self.graph.nodeIdToIndex[other.node2]
        return self.graph.nodeIdToIndex[self.node1] > self.graph.nodeIdToIndex[other.node1]
