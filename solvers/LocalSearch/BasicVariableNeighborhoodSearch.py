
from solvers.neighborhoods.Neighborhood import Neighborhood
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch
from solvers.evaluators.Evaluator import Evaluator

class BVNS(object):
    
    def __init__(self, neighborhoods, evaluator, searchStrategy):
        self.neighborhoods = neighborhoods
        self.evaluator = evaluator
        self.searchStrategy = searchStrategy
        self.nocriteriaEvaluator = Evaluator()
    def optimize(self, x):
        self.setStrategy(x)
        
        while not self.evaluator.criteriaReached(x):
            l = 0
            while l<len(self.neighborhoods):
                x_prim = self.neighborhoods[l].chooseNext(x)
                
                self.neighborhoods[l].reset(x,self.searchStrategy)
                search = SimpleLocalSearch(self.neighborhoods[l], self.nocriteriaEvaluator)
                x_prim = search.optimize(x_prim)
                
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