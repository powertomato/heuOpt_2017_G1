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
from solvers.evaluators.Evaluator import Evaluator
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch

from solvers.neighborhoods.Neighborhood import Neighborhood
from solvers.neighborhoods.MoveNode import MoveNodeCandidate
from solvers.neighborhoods.MoveNode import MoveNode
from solvers.neighborhoods.EdgePageMove import EdgePageMove
from solvers.neighborhoods.EdgePageMove import EdgePageMoveCandidate
import time
class ThreadRunner():

    N_DFS = 1
    N_RND = 2

    E_GRD = 1
    E_RND = 2
    E_GRD_RND = 3

    LS_LS = 1
    LS_VND = 2
    LS_GVNS = 3

    LS_NODEMOVE = 1
    LS_EDGEMOVE = 2

    def __init__(self, threadID, graph, best_solution, crossing_nums, node_construction, edge_construction, iterations, lock, local_search=0, step=0, neighborhood=0):
        self.threadID = threadID
        self.graph = graph
        self.best_solution = best_solution
        self.crossing_nums = crossing_nums
        self.node_construction = node_construction
        self.edge_construction = edge_construction
        self.local_search = local_search
        self.step = step
        self.neighborhood = neighborhood
        self.iterations = iterations
        self.process = Process(target=self.run, args=())
        self.lock = lock

    def stop(self):
        self.should_stop = True

    def start(self):
        self.process.start()

    def join(self):
        self.process.join()

    def run(self):
        self.start_time = time.clock()
        #for _ in range(self.iterations):
        while time.clock() - self.start_time < 900:
            #print("Thread:", self.threadID, "iteration:", _)
            if(self.node_construction == ThreadRunner.N_DFS):
                constructVertexOrderDFS(self.graph)
            elif(self.node_construction == ThreadRunner.N_RND):
                constructVertexOrderRandom(self.graph)

            if(self.edge_construction == ThreadRunner.E_GRD):
                constructSolutionGreedyLeastCrossings(self.graph, False)
            elif(self.edge_construction == ThreadRunner.E_RND):
                constructRandomEdgeAssignment(self.graph)
            elif(self.edge_construction == ThreadRunner.E_GRD_RND):
                constructSolutionGreedyLeastCrossings(self.graph, True)

            if(self.local_search == ThreadRunner.LS_LS):
                evaluator = Evaluator()
                if self.neighborhood == ThreadRunner.LS_EDGEMOVE:
                    neighborhood = EdgePageMove(self.step, evaluator)
                elif self.neighborhood == ThreadRunner.LS_NODEMOVE:
                    neighborhood = MoveNode(self.step, evaluator)

                search = SimpleLocalSearch(neighborhood, evaluator)
                neighborhood.reset(self.graph, self.step)
                x = search.optimize(self.graph)

            elif(self.local_search == ThreadRunner.LS_VND):
                evaluator = Evaluator()

                n1 = EdgePageMove(Neighborhood.BEST, evaluator)
                n2 = MoveNode(Neighborhood.BEST, evaluator)
                vndsearch = VND([n1, n2], evaluator)
                x = vndsearch.optimize(self.graph)

            if(self.compare_to_best() == 0):
                return

    def compare_to_best(self):
        self.lock.acquire()
        num = self.graph.numCrossings()
        self.crossing_nums.append(num)
        self.best_solution[3] += 1
        self.best_solution[4] = time.clock() - self.start_time
        if(num < self.best_solution[0]):
            self.best_solution[0] = num
            self.best_solution[1] = self.graph.copy()
            self.best_solution[2] = self.threadID
            print("new best:", num, "on thread:", self.threadID)

        if(self.best_solution[0] == 0):
            self.lock.release()
            return 0

        self.lock.release()
        return num