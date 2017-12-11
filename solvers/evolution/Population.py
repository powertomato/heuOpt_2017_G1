from solvers.evolution.Chromosome_RandKey import Chromosome_RK
import numpy as np

import random, bisect

class Population(object):
    def __init__(self, graph, size):
        self.specimen = list()
        self.graph = graph
        self.edgeList = list()
        for edge in graph.edgeList:
            self.edgeList.append( edge.toTuple() )
        self.size = size
        for i in range(size):
            c = Chromosome_RK(self)
            self.insertSorted( c )
            
    
    def printPopulation(self, onlyBest=False):
        if not onlyBest:
            for i,c in enumerate( self.specimen):
                print("chromosome %d = (%s, %s) %d" % (i,str(np.argsort(c.nodegene)), str(c.edgegene), c.numCrossings() ) )
        else:
            c = self.specimen[0]
            print("chromosome %d = (%s, %s) %d" % (0,str(np.argsort(c.nodegene)), str(c.edgegene), c.numCrossings() ) )
            
    def insertSorted(self, x):
        bisect.insort_left(self.specimen, x)
            
    def selectSingleRoulette(self):
        raise Exception("Not implemented")
    
    def selectSingleTournament(self, k):
        n = len(self.specimen)
        bestFit = n
        for i in range(k):
            r = random.randint(0,n-1)
            if r < bestFit:
                bestFit = r
        return bestFit, self.specimen[bestFit]
        
    def getGraphSize(self):    
        return len(self.graph.nodes)
    
    def getEdgeList(self):
        return self.edgeList
    
    def getPageNumber(self):
        return self.graph.pageNumber