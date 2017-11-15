import csv
import os
import numpy as np


class Page(object):
    
    def __init__(self, graph):
        self.graph = graph
        self.edges = list()
        self.crossings = {}
        
    def addEdge(self, edge, calcCrossing):
        self.edges.append(edge)

        if calcCrossing:
            for other in self.edges:
                if(self.graph.areEdgesCrossing(edge, other)):
                    self.addCrossing(edge, other)


    def addCrossing(self, edge1, edge2):
        if(edge1.id not in self.crossings):
            self.crossings[edge1.id] = {}

        if(edge2.id not in self.crossings):
            self.crossings[edge2.id] = {}

        self.crossings[edge1.id][edge2.id] = 1
        self.crossings[edge2.id][edge1.id] = 1

    def removeCrossing(self, edge1, edge2):
        if(self.crossings[edge1.id][edge2.id] == 1):
            del self.crossings[edge1.id][edge2.id]

        if(self.crossings[edge2.id][edge1.id] == 1):
            del self.crossings[edge2.id][edge1.id]

    def numCrossings(self):
        num = 0

        for _, c in self.crossings.items():
            for _, c2 in c.items():
                num += 1

        out = num//2
        print(num)
        assert(num%2 == 0)
        return out
        
    def removeEdge(self, edge):
        toDelete = list()
        if edge in self.edges:
            self.edges.remove(edge)
            if edge.id in self.crossings.keys():
                del self.crossings[edge.id]
            for k, cr in self.crossings.items():
                if edge.id in cr.keys():
                    del cr[edge.id]
                if len(cr.values()) == 0:
                    toDelete.append(k)

        for k in toDelete:
            del self.crossings[k]
                        
    def getEdges(self):
        return self.edges
    