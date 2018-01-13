
from solvers.neighborhoods import Neighborhood


class RVNS(object):
    
    def __init__(self, neighborhoods, evaluator, searchStrategy):
        self.neighborhoods = neighborhoods
        self.evaluator = evaluator
        self.searchStrategy = searchStrategy
            
    def optimize(self, x):
        self.setStrategy(x)
        
        while not self.evaluator.criteriaReached(x):
            l = 0
            while l<len(self.neighborhoods):
                x_prim = self.neighborhoods[l].chooseNext(x)
                
                if x_prim == None:
                    #neighborhood exhausted!
                    l+=1
                    continue
                
                if self.evaluator.compare(x_prim, x):
                    x = x_prim
                    for neighb in self.neighborhoods:
                        neighb.reset(x)
                    l = 0
        return x
    
    def setStrategy(self,x):
        for neighb in self.neighborhoods:
            neighb.reset(x,Neighborhood.RANDOM)