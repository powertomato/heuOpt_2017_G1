
import datetime

class Evaluator(object):
    def __init__(self):
        pass
    
    def evaluate(self, graph):
        return graph.numCrossings()#
    
    def compare(self, proposed, current):
        return self.evaluate(proposed) <= self.evaluate(current)
    
    def compareStrict(self, proposed, current):
        return self.evaluate(proposed) < self.evaluate(current)
    
    def criteriaReached(self, x):
        return False
    
     
     
class TimedEvaluator(Evaluator):
    def __init__(self, timeoutDelta):
        self.timeoutTime = datetime.datetime.now()
        if type(timeoutDelta)==datetime.timedelta:
            self.timeoutTime += timeoutDelta
        elif type(timeoutDelta)==int:
            self.timeoutTime += datetime.timedelta(seconds=timeoutDelta)
        
    def criteriaReached(self, x):
        return self.timeoutTime < datetime.datetime.now()
        
    
    
class QualityBoundedTimedEvaluator(TimedEvaluator):
    def __init__(self,timeoutDelta, qualityBound):
        TimedEvaluator.__init__(timeoutDelta)
        self.qualityBound = qualityBound
        self.qualityReached = False
        
    def criteriaReached(self, x):
        self.qualityReached = x.numCrossings() <= self.qualityBound
        return TimedEvaluator.criteriaReached(self, x) or self.qualityReached
    
    def isQualityReached(self):
        return self.qualityReached
    
    