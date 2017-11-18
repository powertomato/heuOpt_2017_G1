from solvers.neighborhoods.Neighborhood import Neighborhood

from solvers.neighborhoods.MoveNode import MoveNodeCandidate
from solvers.neighborhoods.MoveNode import MoveNode
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch
from solvers.evaluators.Evaluator import Evaluator
from model.graph import Graph
import random
import os,sys


import tkinter as tk
from tkinter import *
from BEP_Visualizer.BEP_visualizer import View



g1 = Graph()
g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove01.txt"), True )
candidate = MoveNodeCandidate(g1, 1, 2)
assert( candidate.numCrossings()==0 )
candidate.graphUpdate()
assert( g1.numCrossings()==0 )

g1 = Graph()
g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove02.txt"), True )
assert(g1.numCrossings()==1)

g2 = g1.copy()
g3 = g1.copy()
g4 = g1.copy()
g_ = g1.copy()

candidate = MoveNodeCandidate(g1, 3, 0)
assert(candidate.numCrossings()==2)
g1 = candidate.graphUpdate()
assert(g1.numCrossings()==2)
  
candidate = MoveNodeCandidate(g2, 6, 1)
assert(candidate.numCrossings()==0)
candidate.graphUpdate()
assert(g2.numCrossings()==0)
 
candidate = MoveNodeCandidate(g3, 2, 6)
assert(candidate.numCrossings()==2)
candidate.graphUpdate()
assert(g3.numCrossings()==2)
 
candidate = MoveNodeCandidate(g4, 1, 6)
assert(candidate.numCrossings()==2)
candidate.graphUpdate()
assert(g4.numCrossings()==2)
 
g1 = Graph()
g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove03.txt"), True )
assert(g1.numCrossings()==1)
  
g2 = g1.copy()
g3 = g1.copy()
g4 = g1.copy()
g_ = g1.copy()
   
candidate = MoveNodeCandidate(g1, 4, 7)
assert(candidate.numCrossings()==2)
candidate.graphUpdate()
assert(g1.numCrossings()==2)
   
candidate = MoveNodeCandidate(g2, 1, 6)
assert(candidate.numCrossings()==0)
candidate.graphUpdate()
assert(g2.numCrossings()==0)
  
candidate = MoveNodeCandidate(g3, 5, 1)
assert(candidate.numCrossings()==2)
candidate.graphUpdate()
assert(g3.numCrossings()==2)
  
candidate = MoveNodeCandidate(g4, 6, 1)
assert(candidate.numCrossings()==2)
candidate.graphUpdate()
assert(g4.numCrossings()==2)
 
 
E = Evaluator()
N1 = MoveNode(Neighborhood.BEST, E)
N1.reset(g3)
x = N1.step()
 
g_ = g3.copy()
assert(x.numCrossings()==0)
x.graphUpdate()
 
 
def draw(event):
    view.draw(graph)
  
def click(event):
    global i, graph
    i = (i + 1) % len(graphs)
    graph = graphs[i]
    draw(None)
 
graphs = [g_,g1]
i=0
 
root = Tk()
view = View(root)
graph = graphs[0]
 
root.bind("<Configure>", draw)
 
root.title="BEP Visualizer"
root.bind("<Button-1>", click)
root.deiconify()
root.mainloop()

#assert( MoveNodeCandidate(graph, 4, 0).numCrossings()==2 )
