import csv
import os
import numpy as np
import operator
                    
class Node(object):
    def __init__(self, graph, id, pageNum):
        self.id = id
        self.graph = graph
        self.neighbours = []
        for i in range(pageNum):
            self.neighbours.append(dict())
        
        self.edges = set()

    def addNeighbor(self, otherId, dist, page):
        self.neighbours[page][otherId] = dist

    def getNeighbours(self):
        neighbours = list()
        for perPageNeighbors in self.neighbours:
            for otherId, len in perPageNeighbors.items():
                neighbours.append(self.graph.getNodeByID(otherId))
        return neighbours

    def getNeighboursSorted(self):
        out = list()
        for perPageNeighbors in self.neighbours:
            for key, value in sorted(perPageNeighbors.items(), key=operator.itemgetter(1)):
                out.append(self.graph.getNodeByID(key))

        return out
            
    def _insertionSort(self,alist):
        for index in range(1,len(alist)):
    
            currentvalue = alist[index]
            position = index
    
            while position>0 and alist[position-1][0]>currentvalue[0]:
                alist[position]=alist[position-1]
                position = position-1
    
            alist[position]=currentvalue
                
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return not self == other