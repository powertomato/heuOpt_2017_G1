import math,random,copy
from model.graph import Graph
import copy
import numpy as np

class ChType:
    FIRSTGEN = -1
    ELITE = 0
    RECOMBINED = 1
    MUTATED = 2
    IMMIGRATED = 3

class Chromosome(object):
    def __init__(self,population,nodegene=-1,edgegene=-1, ch_type=-1):
        self.chType = ch_type
        self.population = population
        self.num_nodes = population.getGraphSize()
        self.pageNumber = self.population.getPageNumber()
        self.num_edges = len(self.population.getEdgeList())

        if(nodegene == -1):
            self.nodegene = [random.random() for x in range(self.num_nodes)]
        else:
            self.nodegene = nodegene

        if type(edgegene)==int and edgegene != -1:
            self.edgegene = self.ibase(edgegene, self.pageNumber, self.num_edges)
        elif edgegene == -1:
            self.edgegene = []
            for i in range(self.num_edges):
                self.edgegene.append( random.randint(0,self.pageNumber-1) )
        else:
            self.edgegene = edgegene
            
        #if edgegene==-1:
        #    self.edgegene = random.randint(0,self.pageNumber**self.num_edges-1)
            
        self._num_crossings = -1
        self.graph = None
         
    def recombine(self, other, ratio):
        newNodegene = self.recombineNodeGene(other, ratio)
        newEdgegene = self.recombineEdgeGene(other, ratio)
        return Chromosome(self.population, newNodegene, newEdgegene)
        
        
    def recombineNodeGene(self, other, ratio):
        n = round((len(self.nodegene)-1)*ratio)
        if random.random() < ratio:
            newNodegene = self.nodegene[:n] + other.nodegene[n:]
        else:
            newNodegene = other.nodegene[:n] + self.nodegene[n:]
        return newNodegene
    
    def recombineEdgeGene(self, other, ratio):
        n = random.randint(0,len(self.edgegene)-1)
        if random.randint(0,1):
            newEdgegene = self.edgegene[:n] + other.edgegene[n:] 
        else:
            newEdgegene = other.edgegene[:n] + self.edgegene[n:]
        return newEdgegene
        
         
    def numCrossings(self):
        if self._num_crossings == -1:
            self._num_crossings = self.getGraph().numCrossings()
        return self._num_crossings

    def node_rk_generator(self):
        indices = np.argsort(self.nodegene)
        for ind in indices:
            yield ind

    def edge_generator(self):
        num = self.num_edges
        #pages = self.ibase(self.edgegene, self.pageNumber, self.num_edges)
        for i,edge in enumerate(self.population.getEdgeList()):
            yield (edge[0], edge[1], self.edgegene[i])

    def getGraph(self):
        if self.graph == None:
            
            self.graph = Graph()
            self.graph.initFromLists(self.pageNumber, self.node_rk_generator(), self.edge_generator())
        return self.graph
             
    
#     def edge_generator(self):
#         edges = self.population.getEdgeList()
#         for edge in edges:
#             yield edge
            
    def ibase(self, n, radix, minlen):
        r = []
        while n:
            n,p = divmod(n, radix)
            r.append(p)
        r.reverse()
        r = [0]*(minlen-len(r)) + r
        return r
        
    def __lt__(self, other):
        return self.numCrossings() < other.numCrossings()
        
    def __gt__(self, other):
        return self.numCrossings() > other.numCrossings()