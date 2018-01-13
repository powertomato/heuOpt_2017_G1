
from solvers.neighborhoods import Neighborhood


class VND(object):

    def __init__(self, neighborhoods, evaluator):
        self.neighborhoods = neighborhoods
        self.evaluator = evaluator
            
    def optimize(self, x):
        self.setStrategy(x)
        
        l = 0
        while l<len(self.neighborhoods) and not self.evaluator.criteriaReached(x):
            x_prim = self.neighborhoods[l].step()
            
            if x_prim == None:
                #neighborhood exhausted!
                l+=1
                print("VND neighborhood done")
                continue
            
            if self.evaluator.compareStrict(x_prim, x):

                x = x_prim.graphUpdate()
                for i in range(l+1):
                    self.neighborhoods[i].reset(x)
                l = 0
        print("VND step " + str(x.numCrossings()))
        return x
                
    def setStrategy(self,x):
        for neighb in self.neighborhoods:
            neighb.reset(x,Neighborhood.BEST)
