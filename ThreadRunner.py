from multiprocessing import Process, Lock
import sys
import os
import copy

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from model.graph import Graph
from BEP_Visualizer.BEP_visualizer import View
from solvers.construction.DepthFirstVertexOrder import *
from solvers.construction.GreedyLeastPage import *
from solvers.construction.RandomEdgeAssignment import *
from solvers.construction.RandomVertexOrder import *
from model.node import Node
from model.edge import Edge
from model.page import Page
from solvers.LocalSearch.VariableNeighborhoodDescent import *
from solvers.evaluators.Evaluator import *

class ThreadRunner():

    N_DFS = 1
    N_RND = 2

    E_GRD = 1
    E_RND = 2

    LS_LS = 1
    LS_VND = 2
    LS_GVNS = 3

    def __init__(self, threadID, graph, best_solution, node_construction, edge_construction, local_search, iterations, lock):
        self.threadID = threadID
        self.graph = graph
        self.best_solution = best_solution
        self.node_construction = node_construction
        self.edge_construction = edge_construction
        self.local_search = local_search
        self.iterations = iterations
        self.process = Process(target=self.run, args=())
        self.lock = lock

    def start(self):
        self.process.start()

    def join(self):
        self.process.join()

    def run(self):
        for _ in range(self.iterations):
            if(self.node_construction == ThreadRunner.N_DFS):
                constructVertexOrderDFS(self.graph)
            elif(self.node_construction == ThreadRunner.N_RND):
                constructVertexOrderRandom(self.graph)

            if(self.edge_construction == ThreadRunner.E_GRD):
                constructSolutionGreedyLeastCrossings(self.graph, True)
            elif(self.edge_construction == ThreadRunner.E_RND):
                constructRandomEdgeAssignment(self.graph)

            self.compare_to_best()

    def compare_to_best(self):
        num = self.graph.numCrossings()
        self.lock.acquire()
        if(num < self.best_solution[0]):
            self.best_solution[0] = num
            self.best_solution[1] = self.graph.copy()
            print("new best:", num, "on thread:", self.threadID)

        self.lock.release()