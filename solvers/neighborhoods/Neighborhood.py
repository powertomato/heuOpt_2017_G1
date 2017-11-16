
import random

class Neighborhood(object):
    
    RANDOM = 1
    NEXT = 2
    BEST = 3
    
    def __init__(self, strategy, evaluator):
        self.strategy = strategy
        self.evaluator = evaluator
        self.neighborGenerator = None
        self.stepGenerator = None
        
    def step(self):
        return self._traverseGenerator(self.stepGenerator)
    
    def _chooseNext(self):
        return self._traverseGenerator(self.neighborGenerator)
        
    def _traverseGenerator(self, generator):
        if generator == None:
            return None
        try: 
            return next(generator)
        except StopIteration:
            generator = None
            return None
        
    def reset(self, x, strategy=None):
        if strategy != None:
            self.strategy = strategy
        if self.strategy == self.RANDOM:
            self.neighborGenerator = self.generateRandom(x)
        elif self.strategy == self.NEXT or self.strategy == self.BEST:
            self.neighborGenerator = self.generateSingle(x)
            
        if self.strategy == self.RANDOM:
            self.neighborGenerator = self.generateRandom(x)
            self.stepGenerator = self.stepRandom()
        elif self.strategy == self.NEXT:
            self.neighborGenerator = self.generateSingle(x)
            self.stepGenerator = self.stepNext(x)
        elif self.strategy == self.BEST:
            self.neighborGenerator = self.generateSingle(x)
            self.stepGenerator = self.stepBest(x)
        
    def stepBest(self, x):
        improved = False
        proposed = self._chooseNext()
        while proposed != None:
            if self.evaluator.compareStrict(proposed, x):
                improved = True
                x = proposed
            proposed = self._chooseNext()
        if improved:
            yield x
        else:
            return
        
    def stepNext(self, x):
        proposed = self._chooseNext()
        while proposed != None:
            if self.evaluator.compareStrict(proposed, x):
                yield proposed.
            proposed = self._chooseNext()
        return
    
    def stepRandom(self):
        while True:
            yield self._chooseNext()
        
    def generateRandom(self, x):
        yield from ()
    
    def generateSingle(self, x):
        yield from ()