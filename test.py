from solvers.neighborhoods.Neighborhood import Neighborhood
from solvers.neighborhoods.SwitchTwoNodes import SwitchTwoNodes
from solvers.neighborhoods.SwitchNNodes import SwitchNNodes

from solvers.neighborhoods.EdgePageMove import EdgePageMove
from solvers.neighborhoods.EdgePageMove import EdgePageMoveCandidate
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch
from solvers.evaluators.Evaluator import Evaluator
from model.graph import Graph
import random
import os,sys
# 
# class F(object):
#     def __init__(self, n):
#         self.nodes = list(range(n))
#         random.shuffle(self.nodes)
#     def __str__(self):
#         return str(self.nodes)
#         
# class E(object):
#     
#     def evaluate(self, x):
#         v = 0
#         for i in range(len(x.nodes)-1):
#             v += x.nodes[i]-x.nodes[i+1]
#         return v
#     
#     def compare(self, proposed, current):
#         return self.evaluate(proposed) <= self.evaluate(current)
#     def compareStrict(self, proposed, current):
#         return self.evaluate(proposed) < self.evaluate(current)
#     
#     def criteriaReached(self, x):
#         if self.evaluate(x)==0:
#             return True
#         return False
        
        

# N1 = SwitchTwoNodes(Neighborhood.BEST, E())
# def testSwitch(x,n1,n2):
#     return (n1,n2)
# 
# 
# N1._switch = testSwitch
# 
# for n in N1.generateSingle(F(4)):
#     print(n)
#     
# i = 0
# gen = N1.generateRandom(F(10))
# while i<10:
#     n = next(gen)
#     print(n)
#     i+=1
# del n
#     
# print("--------------------")
# def testSwitch2(x,n1,n2):
#     copy = F(len(x.nodes))
#     copy.nodes = list(x.nodes)
#     tmp = copy.nodes[n1]
#     copy.nodes[n1] = copy.nodes[n2]
#     copy.nodes[n2] = tmp
#     return copy
# 
# E1 =  E()
# N2 = SwitchTwoNodes(Neighborhood.BEST, E1)
# N2._switch = testSwitch2
# x = F(6)
# N2.reset(x)
# 
# print(str(x)+" "+str(E1.evaluate(x)))
# x = N2.step()
# print(str(x)+" "+str(E1.evaluate(x)))
# 
# print("--------------------")
# N2.reset(x)
# search = SimpleLocalSearch(N2, E1)
# x = search.optimize(x)
# 
# print(str(x)+" "+str(E1.evaluate(x)))
# print("--------------------")
# x = F(6)
# x.nodes = [5,2,1,0,3,4]
# N2.reset(x)
# for n in N2.generateSingle(x):
#     print(str(n)+" "+str(E1.evaluate(n)))
# print("--------------------")

# N3 = SwitchNNodes(Neighborhood.BEST, E(), 2)
# def testShuffle(x,sorted,shuffle):
#     copy = F(len(x.nodes))
#     copy.nodes = list(x.nodes)
#     nodes = []
#     for idx in shuffle:
#         nodes.append(copy.nodes[idx])
#     for idx,node in enumerate(nodes):
#         copy.nodes[sorted[idx]] = node
#     return copy
# N3._shuffle = testShuffle
# x = F(3)
# x.nodes.sort()
# for n in N3.generateSingle(x):
#     print(str(n)+" "+str(E().evaluate(n)))
# print("--------------------")
# x = F(50)
# N3.reset(x, Neighborhood.NEXT)
# search = SimpleLocalSearch(N3, E())
# x = search.optimize(x)
# print(x)


graph = Graph()
graph.read( os.path.join(os.getcwd(), "instances", "testinstances", "testEdge01.txt") )
assert(graph.numCrossings()==1)
candidate1 = EdgePageMoveCandidate(graph, 4, 0, 1)
assert(candidate1.numCrossings()==0)
candidate2 = EdgePageMoveCandidate(graph, 2, 0, 1)
assert(candidate2.numCrossings()==1)
assert(candidate1.graphUpdate()==graph)
assert(graph.numCrossings()==0)

graph = Graph()
graph.read( os.path.join(os.getcwd(), "instances", "testinstances", "testEdge01.txt") )
assert(graph.numCrossings()==1)

E = Evaluator()
N1 = EdgePageMove(Neighborhood.BEST, E)
N1.reset(graph)
x = N1.step()

assert(x.numCrossings()==0)
assert(graph.numCrossings()==0)
