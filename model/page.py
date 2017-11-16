import csv
import os
import numpy as np


class Page(object):
    
    def __init__(self, graph, id):
        self.id = id
        self.graph = graph
        self.edges = set()
        self.doubled_crossings = 0
        self.doubled_crossings_valid = True
        
    def addEdge(self, edge):
        self.edges.add(edge)
        self.doubled_crossings += len(edge.getCrossingSetForPage(self.id))

    def removeEdge(self, edge):
        self.edges.remove(edge)
        self.doubled_crossings -= len(edge.getCrossingSetForPage(self.id))

    def numCrossings(self):
        doubledCrossings = 0
        for edge in self.edges:
            doubledCrossings += len(edge.getCrossingSetForPage(self.id))

        return doubledCrossings

    def getEdges(self):
        return self.edges
    