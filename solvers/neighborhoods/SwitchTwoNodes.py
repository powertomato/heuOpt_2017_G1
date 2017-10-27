
from solvers.neighborhoods.Neighborhood import Neighborhood
import math

class SwitchTwoNodes(Neighborhood):
    def __init__(self, stepFunction, evaluator):
        Neighborhood.__init__(stepFunction, evaluator)
        self.sizeCache = {}
    
    def choose(self, x, num):
        new = x.copy()
        
    def size(self, x):
        n = len(x.nodes)
        if not n in self.sizeCache:
            self.sizeCache[n] = math.factorial(n)/(math.factorial(2)*math.factorial(n-2))
        
        return self.sizeCache[n]
