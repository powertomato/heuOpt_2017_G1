import csv
import os
import numpy as np


class Page(object):
    
    def __init__(self, graph, id):
        self.id = id
        self.graph = graph
        self.edges = set()
        
    def addEdge(self, edge):
        self.edges.add(edge)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def numCrossings(self):
        doubledCrossings = 0
        for edge in self.edges:
            doubledCrossings += len(edge.perPageCrossedEdges[self.id])
        return doubledCrossings

    def getEdges(self):
        return self.edges
    