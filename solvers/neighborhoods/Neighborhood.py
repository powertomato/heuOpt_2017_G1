
import random

class Neighborhood(object):
    
    def __init__(self, stepFunction, evaluator):
        self.stepFunction = stepFunction
        self.evaluator = evaluator
        
    def chooseOne(self, x):
        return self.stepFunction(self,x)
        
    def choose(self, x, num):
        raise Exception("Abstract: not implemented")
    
    def size(self, x):
        raise Exception("Abstract: not implemented")

def stepFunctionRandom(neighborhood, x):
    n = neighborhood.size(x)-1
    return neighborhood.choose(x, random.randint(1,n))
        
def generateStepFunctionRandom(bestOfN=1):
    if bestOfN == 1:
        return stepFunctionRandom
    def f(neighborhood, x):
        for n in range(0, bestOfN):
            proposed = stepFunctionRandom(neighborhood, x)
            if neighborhood.evaluator.compare(proposed, x):
                x = proposed
        return x
    return f
        
        

def stepFunctionBestImprovment(neighborhood, x):
    for n in range(1, neighborhood.size(x)):
        proposed = neighborhood.choose(n)
        if neighborhood.evaluator.compare(proposed, x):
            x = proposed
    return x
  
def stepFunctionNextImprovment(neighborhood, x):
    for n in range(1, neighborhood.size(x)):
        proposed = neighborhood.choose(n)
        if neighborhood.evaluator.compare(proposed, x):
            return proposed
    return x