
from solvers.evaluators import Evaluator
from solvers.neighborhoods import Neighborhood
from solvers.LocalSearch.VariableNeighborhoodDescent import VND


class GVNS(object):
    
    def __init__(self, neighborhoods, evaluator):
        self.neighborhoods = neighborhoods
        self.evaluator = evaluator
        self.nocriteriaEvaluator = Evaluator()
            
    def optimize(self, x):
        #self.setStrategy(x, Neighborhood.RANDOM)
        
        while not self.evaluator.criteriaReached(x):
            l = 0
            while l<len(self.neighborhoods) and not self.evaluator.criteriaReached(x):
                x_prim = x.copy()
                self.neighborhoods[l].reset(x_prim, Neighborhood.RANDOM)
                x_candidate = self.neighborhoods[l].step()
                x_candidate.graphUpdate()

                search = VND(self.neighborhoods, self.nocriteriaEvaluator)
                x_prim = search.optimize(x_prim)
                
                if x_prim == None:
                    #neighborhood exhausted!
                    l+=1
                    continue
                
                if self.evaluator.compareStrict(x_prim, x):
                    
                    print("GVNS new best " + str(x_prim.numCrossings()))
                    #print("%d %d" %(x.numCrossings(), x_prim.numCrossings()))
                    x = x_prim
                    for i in range(l+1):
                        self.neighborhoods[i].reset(x)
                    l = 0
                else:
                    l+=1
        return x
    
    def setStrategy(self,x, strategy):
        for neighb in self.neighborhoods:
            neighb.reset(x, strategy)