import os
from tkinter import *

from BEP_Visualizer.BEP_visualizer import View
from model.graph import Graph
from solvers.neighborhoods.MoveNode import MoveNodeCandidate

# g1 = Graph()
# g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove01.txt"), True )
# candidate = MoveNodeCandidate(g1, 1, 2)
# assert( candidate.numCrossings()==0 )
# candidate.graphUpdate()
# assert( g1.numCrossings()==0 )
# 
# g1 = Graph()
# g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove02.txt"), True )
# assert(g1.numCrossings()==1)
# 
# g2 = g1.copy()
# g3 = g1.copy()
# g4 = g1.copy()
# g_ = g1.copy()
# 
# candidate = MoveNodeCandidate(g1, 3, 0)
# assert(candidate.numCrossings()==2)
# g1 = candidate.graphUpdate()
# assert(g1.numCrossings()==2)
#   
# candidate = MoveNodeCandidate(g2, 6, 1)
# assert(candidate.numCrossings()==0)
# candidate.graphUpdate()
# assert(g2.numCrossings()==0)
#  
# candidate = MoveNodeCandidate(g3, 2, 6)
# assert(candidate.numCrossings()==2)
# candidate.graphUpdate()
# assert(g3.numCrossings()==2)
#  
# candidate = MoveNodeCandidate(g4, 1, 6)
# assert(candidate.numCrossings()==2)
# candidate.graphUpdate()
# assert(g4.numCrossings()==2)
#  
# g1 = Graph()
# g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove03.txt"), True )
# assert(g1.numCrossings()==1)
#   
# g2 = g1.copy()
# g3 = g1.copy()
# g4 = g1.copy()
# g_ = g1.copy()
#    
# candidate = MoveNodeCandidate(g1, 4, 7)
# assert(candidate.numCrossings()==2)
# candidate.graphUpdate()
# assert(g1.numCrossings()==2)
#    
# candidate = MoveNodeCandidate(g2, 1, 6)
# assert(candidate.numCrossings()==0)
# candidate.graphUpdate()
# assert(g2.numCrossings()==0)
#   
# candidate = MoveNodeCandidate(g3, 5, 1)
# assert(candidate.numCrossings()==2)
# candidate.graphUpdate()
# assert(g3.numCrossings()==2)
#   
# candidate = MoveNodeCandidate(g4, 6, 1)
# assert(candidate.numCrossings()==2)
# candidate.graphUpdate()
# assert(g4.numCrossings()==2)
#  
#  
# E = Evaluator()
# N1 = MoveNode(Neighborhood.BEST, E)
# N1.reset(g3)
# x = N1.step()
#  
# g_ = g3.copy()
# assert(x.numCrossings()==0)
# x.graphUpdate()
 
g1 = Graph()
g1.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove04.txt"), True )

candidate = MoveNodeCandidate(g1, 0, 3)
#assert(candidate.numCrossings()==1)
a = candidate.numCrossings()
candidate.graphUpdate()


g2 = Graph()
g2.read( os.path.join(os.getcwd(), "instances", "testinstances", "testMove05.txt"), True )
g_ = g2.copy()
moves = [(7, 1), (5, 0), (0, 7), (7, 0), (6, 2), (3, 4), (7, 4), (8, 5)]
i=0
for m in moves:
    candidate = MoveNodeCandidate(g2, m[0], m[1])
    a = candidate.numCrossings()
    candidate.graphUpdate()
    g2.write("out_test" + str(i))
    i+=1
    print("%d %d" % (a, g2.numCrossings()))
    break
     
 
def draw(event):
    view.draw(graph)
  
def click(event):
    global i, graph
    i = (i + 1) % len(graphs)
    graph = graphs[i]
    draw(None)
 
graphs = [g_]
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
