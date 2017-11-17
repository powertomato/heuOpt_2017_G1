from solvers.neighborhoods.Neighborhood import Neighborhood
from solvers.neighborhoods.SwitchTwoNodes import SwitchTwoNodes
from solvers.neighborhoods.SwitchNNodes import SwitchNNodes

from solvers.neighborhoods.MoveNode import MoveNodeCandidate
from solvers.neighborhoods.EdgePageMove import EdgePageMoveCandidate
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch
from solvers.evaluators.Evaluator import Evaluator
from model.graph import Graph
import random
import os,sys


import tkinter as tk
from tkinter import *
from BEP_Visualizer.BEP_visualizer import View


def draw(event):
    view.draw(graph)


def click(event):
    global i, graph
    i = (i + 1) % len(graphs)
    graph = graphs[i]
    draw(None)

g1 = Graph()
g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove01.txt"), True )
candidate = MoveNodeCandidate(g1, 1, 2)
assert( candidate.numCrossings()==0 )
g2 = g1.copy()
candidate.graphUpdate()

graphs = [g1,g2]
i=0

g3 = Graph()
g3.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove02.txt"), True )
a = MoveNodeCandidate(g3, 4, 0)
print(a.numCrossings())
#a.graphUpdate()
# print(graph.numCrossings())

root = Tk()
view = View(root)
graph = graphs[0]

root.bind("<Configure>", draw)

root.title="BEP Visualizer"
root.bind("<Button-1>", click)
root.deiconify()
root.mainloop()

#assert( MoveNodeCandidate(graph, 4, 0).numCrossings()==2 )