import os

from model.graph import Graph
from solvers.evolution.Evolution import GeneticAlgorithm
from visualization.GA_plot import *

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



graph.read( os.path.join(os.getcwd(), "instances", "instance-04.txt"), False )
print(graph.numCrossings())
GA = GeneticAlgorithm(graph, 100, 90, 100, 2, 25, 0.8, 0.1, 0.1, None)
plot = GAPlot()

LS_Interval = 60

for i in range(200):
    LS = False
    GA.population.printPopulation(True)
    if i%LS_Interval == LS_Interval-1:
        LS = True
    GA.doStep(LS)
    plot.add_specimens(i, 0, GA.population.specimen)
    print("#####")
    
GA.population.printPopulation()
plot.plot()

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

