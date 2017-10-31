
from solvers.neighborhoods.Neighborhood import Neighborhood
import math
import itertools, random
from collections import Counter

class SwitchNNodes(Neighborhood):
    def __init__(self, strategy, evaluator, N):
        self.N = N
        super(SwitchNNodes, self).__init__(strategy, evaluator)
        
    def generateRandom(self, x):
        while True:
            n = len(x.nodes)
            
            nlist = [-1]*self.N
            while self._notAllEqual(nlist) or self._sorted(nlist):
                for i in range(len(nlist)):
                    nlist[i] = n2 = random.randint(0, n-1)
            sorted = list(nlist)
            sorted.sort()
            yield self._shuffle(x, sorted, nlist)
        
    def generateSingle(self, x):
        n = len(x.nodes)
        for nodes in itertools.combinations(range(n),self.N):
            sorted = None
            for shuffle in itertools.permutations(nodes):
                if sorted == None:
                    sorted = shuffle
                    continue
                yield self._shuffle(x, sorted, shuffle)
            
    def _shuffle(self, x, sorted, shuffle):
        ret = x.copy()
        ret.shuffleNodes(sorted,shuffle)
        return ret
            
    def _sorted(self,nlist):
        for i in range(len(nlist)-1):
            if nlist[i]>nlist[i+1]:
                return False
        return True
    
    def _notAllEqual(self, nlist):
        counter = Counter(nlist)
        for val in counter:
            if counter[val] != 1:
                return True
        return False