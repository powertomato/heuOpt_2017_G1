
from solvers.neighborhoods.Neighborhood import Neighborhood
import math
import itertools, random

class SwitchTwoNodes(Neighborhood):
    
    def generateRandom(self, x):
        while True:
            n = len(x.nodes)
            n1 = random.randint(0,n-1)
            n2 = n1
            while n2 == n1:
                n2 = random.randint(0, n-1)
            yield self._switch(x, n1, n2)
            
    def generateSingle(self, x):
        n = len(x.nodes)
        for nodes in itertools.combinations(range(n),2):
            yield self._switch(x, nodes[0], nodes[1])
            
    def _switch(self, x, n1, n2):
        ret = x.copy()
        ret.switchNodes(n1,n2)
        return ret
            