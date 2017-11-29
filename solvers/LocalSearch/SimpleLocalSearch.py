
from solvers.neighborhoods.Neighborhood import *

class SimpleLocalSearch(object):

    def __init__(self, neighborhood, evaluator):
        self.neighborhood = neighborhood
        self.evaluator = evaluator
        self.step = 0
        
    def optimize(self, x):
        while not self.evaluator.criteriaReached(x):
            x_prim = self.neighborhood.step()
            
            if x_prim == None:
                #neighborhood exhausted!
                break
            
            if self.evaluator.compare(x_prim, x):
                self.step += 1
                x = x_prim.graphUpdate()
                self.neighborhood.reset(x)
        print("local search steps: %d" % self.step)
        return x
                
