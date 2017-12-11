import math,random,copy
from model.graph import Graph
import copy

class Chromosome(object):
    def __init__(self,population,nodegene=-1,edgegene=-1):
        self.population = population
        self.num_nodes = population.getGraphSize()
        self.num_nodes_fac = math.factorial(self.num_nodes)
        self.pageNumber = self.population.getPageNumber()
        self.num_edges = len(self.population.getEdgeList())
        
        if nodegene==-1:
            self.nodegene = random.randint(0,self.num_nodes_fac-1)
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
         
    def recombine(self, other):
        newNodegene = self.recombineNodeGene(other)
        newEdgegene = self.recombineEdgeGene(other)
        return Chromosome(self.population, newNodegene, newEdgegene)
        
        
    def recombineNodeGene(self, other):
        if random.randint(0,1):
            newNodegene = self.nodegene
        else:
            newNodegene = other.nodegene               
        return newNodegene
    
    def recombineEdgeGene(self, other):
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
    
    def getGraph(self):
        if self.graph == None:
            
            self.graph = Graph()
            self.graph.initFromLists(self.pageNumber, self.node_lehmer_generator(), self.edge_generator())
        return self.graph
        
    def node_lehmer_generator(self):
        for i in self.perm_from_int(range(self.num_nodes), self.nodegene):
            yield i
            
    def perm_from_code(self, base, code):
        perm = list(base)
        for i in range(len(base) - 1):
            j = code[i]
            perm[i], perm[i+j] = perm[i+j], perm[i]
    
        return perm

    def perm_from_int(self, base, num):
        code = self.code_from_int(len(base), num)
        return self.perm_from_code(base, code)   
    
    def code_from_int(self, size, num):
        code = []
        for i in range(size):
            num, j = divmod(num, size - i)
            code.append(j)
        return code     
            
    def edge_generator(self):
        num = self.num_edges
        #pages = self.ibase(self.edgegene, self.pageNumber, self.num_edges)
        for i,edge in enumerate(self.population.getEdgeList()):
            yield (edge[0], edge[1], self.edgegene[i])
             
    
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