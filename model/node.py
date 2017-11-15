import csv
import os
import numpy as np
                    
class Node(object):
    def __init__(self, graph, id):
        self.id = id
        self.graph = graph
        self.neighbours = set()
        self.neighboursMarked = set()
        
    def markNeighbour(self, n):
        if n in self.neighbours:
            e = self.neighbours
            self.neighboursMarked.add(n)
            self.neighbours.remove(n)
            
    def clearMarkings(self, n):
        self.neighbours.update(self.neighboursMarked)
        self.neighboursMarked.clear()
        
    def getDistances(self, onlyUnmarked=True): 
        distances = []
        for otherId in self.neighbours:
            dist = self.getDistance(otherId,id)
            distances.Add((otherId, dist))
            self._insertionSort(distances)
        if not onlyUnmarked:
            for otherId in self.neighboursNarked:
                dist = self.getDistance(otherId,id)
                distances.Add((otherId, dist))
                self._insertionSort(distances)
                
        return distances

    def getNeighbours(self):
        neighbours = list()
        for otherId in self.neighbours:
            neighbours.append(self.graph.getNodeByID(otherId))
        return neighbours
            
    def _insertionSort(self,alist):
        for index in range(1,len(alist)):
    
            currentvalue = alist[index]
            position = index
    
            while position>0 and alist[position-1][0]>currentvalue[0]:
                alist[position]=alist[position-1]
                position = position-1
    
            alist[position]=currentvalue

    def copy(self, graph=None):
        if(graph==None):
            graph = self.graph
        new = Node(graph, self.id)
        new.neighbours = set(self.neighbours)
        new.neighboursMarked = set(self.neighboursMarked)
                
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return not self == other