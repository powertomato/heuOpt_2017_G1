from solvers.neighborhoods.Neighborhood import Neighborhood

from solvers.neighborhoods.EdgePageMove import EdgePageMove
from solvers.neighborhoods.EdgePageMove import EdgePageMoveCandidate
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch
from solvers.evaluators.Evaluator import Evaluator
from model.graph import Graph
import random
import os,sys


import tkinter as tk
from tkinter import *
from BEP_Visualizer.BEP_visualizer import View

graph = Graph()
graph.read( os.path.join(os.getcwd(), "instances", "testinstances", "testEdge01.txt"), True )
assert(graph.numCrossings()==1)
candidate1 = EdgePageMoveCandidate(graph, 4, 0, 1)
assert(candidate1.numCrossings()==0)
candidate2 = EdgePageMoveCandidate(graph, 2, 0, 1)
assert(candidate2.numCrossings()==1)
assert(candidate1.graphUpdate()==graph)
assert(graph.numCrossings()==0)

graph = Graph()
graph.read( os.path.join(os.getcwd(), "instances", "testinstances", "testEdge01.txt"), True )
assert(graph.numCrossings()==1)

E = Evaluator()
N1 = EdgePageMove(Neighborhood.BEST, E)
N1.reset(graph)
x = N1.step()

assert(x.numCrossings()==0)
x.graphUpdate()
assert(graph.numCrossings()==0)

graph = Graph()
graph.read( os.path.join(os.getcwd(), "instances", "testinstances", "testEdge02.txt"), True )
assert(graph.numCrossings()==21)

N1.reset(graph)
x = N1.step()
x.graphUpdate()
print("0. %d" % (graph.numCrossings()))

N1.reset(graph)
x = N1.step()
x.graphUpdate()
print("1. %d" % (graph.numCrossings()))

graph = Graph()
graph.read( os.path.join(os.getcwd(), "instances", "testinstances", "testEdge02.txt"), True )
g_ = graph.copy()
assert(graph.numCrossings()==21)

N1.reset(graph, Neighborhood.BEST)
search = SimpleLocalSearch(N1, E)
x = search.optimize(graph)
print(x.numCrossings())





i=0
 
def draw(event):
    view.draw(graph)
  
def click(event):
    g1 = g_.copy()
    N1.reset(g1, Neighborhood.RANDOM)
    x = N1.step()
    x.graphUpdate()
    
    view.draw(g1)
 
root = Tk()
view = View(root)
 
root.bind("<Configure>", draw)
 
root.title="BEP Visualizer"
root.bind("<Button-1>", click)
root.deiconify()
root.mainloop()


import tkinter as tk
from tkinter import *
from BEP_Visualizer.BEP_visualizer import View
   

