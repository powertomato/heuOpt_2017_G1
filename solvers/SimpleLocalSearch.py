
from solvers.neighborhoods.Neighborhood import *

class SimpleLocalSearch(object):

    def __init__(self, neighborhood, evaluator):
        self.neighborhood = neighborhood
        self.evaluator = evaluator
        a = Neighborhood
        
    def doSolve(self, x):
        while not self.evaluator.criteriaReached(x) or self.improvmentCriterion():
            x_prim = self.neighborhood.chooseOne(x)
            if self.evaluator.compare(x_prim, x):
                x = x_prim
                self.lastStepImproved = True 
            else:
                self.lastStepImproved = False
                
    def improvmentCriterion(self):
        if self.neighborhood.stepFunction == stepFunctionBestImprovment or \
            self.neighborhood.stepFunction == stepFunctionNextImprovment:
            return self.lastStepImroved
        return False