
from solvers.neighborhoods.Neighborhood import Neighborhood
from solvers.LocalSearch.VariableNeighborhoodDescent import VND
from solvers.evaluators.Evaluator import Evaluator

class GVNS(object):
    
    def __init__(self, neighborhoods, evaluator, searchStrategy):
        self.neighborhoods = neighborhoods
        self.evaluator = evaluator
        self.searchStrategy = searchStrategy
        self.nocriteriaEvaluator = Evaluator()
            
    def optimize(self, x):
        self.setStrategy(x, Neighborhood.RANDOM)
        
        while not self.evaluator.criteriaReached(x):
            l = 0
            while l<len(self.neighborhoods):
                x_prim = self.neighborhoods[l].chooseNext(x)
                
                self.setStrategy(x_prim, Neighborhood.BEST)
                search = VND(self.neighborhoods, self.evaluator)
                x_prim = search.optimize(x_prim)
                self.setStrategy(x, Neighborhood.RANDOM)
                
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
    
    def setStrategy(self,x, strategy):
        for neighb in self.neighborhoods:
            neighb.reset(x, strategy)