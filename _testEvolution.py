from solvers.neighborhoods.Neighborhood import Neighborhood

from solvers.neighborhoods.EdgePageMove import EdgePageMove
from solvers.neighborhoods.EdgePageMove import EdgePageMoveCandidate
from solvers.neighborhoods.MoveNode import *

from solvers.evolution.Chromosome_RandKey import Chromosome_RK
from solvers.evolution.Population import Population
from solvers.evolution.Evolution_RandKey import GeneticAlgorithm

from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch
from solvers.evaluators.Evaluator import Evaluator
from model.graph import Graph
import random
import os,sys


import tkinter as tk
from tkinter import *
from BEP_Visualizer.BEP_visualizer import View

graph = Graph()
#graph.read( os.path.join(os.getcwd(), "instances", "testinstances", "testEvolution01.txt"), False )
#p = Population(graph, 0)
#c = Chromosome(p)

print("----")
# for i in range(4*3*2*1):
#     c.nodegene = i
#     print(list(c.node_lehmer_generator()))
# 
# print("----")
# for i in range(4**4):
#     c.edgegene=i
#     print(list(c.edge_generator()))



graph.read( os.path.join(os.getcwd(), "instances", "instance-09.txt"), False )
print(graph.numCrossings())
GA = GeneticAlgorithm(graph, 200, 199, 50, 150, None)

for i in range(300):
    GA.population.printPopulation(True)
    GA.doStep()
    print("#####")
    
GA.population.printPopulation()

# graph.read( os.path.join(os.getcwd(), "instances", "instance-01.txt"), True )
# p = Population(graph, 100)
# 
# num = 0
# def draw(event):
#     global num
#     g = p.specimen[num].getGraph()
#     view.draw(g)
#     print( "%d %d" % (num, g.numCrossings() ))
#     num = (num+1) % len(p.specimen)
#    
# def click(event):
#     draw(None)
#   
# root = Tk()
# view = View(root)
#   
# root.bind("<Configure>", draw)
#   
# root.title="BEP Visualizer"
# root.bind("<Button-1>", click)
# root.deiconify()
# root.mainloop()

