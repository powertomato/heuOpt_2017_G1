#!/usr/bin/python3
# encoding: utf-8

import sys
import os
import copy

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from model.graph import Graph

from solvers.construction.DepthFirstVertexOrder import *
from solvers.construction.GreedyLeastPage import *
from solvers.construction.RandomEdgeAssignment import *
from solvers.construction.RandomVertexOrder import *

from solvers.evaluators.Evaluator import Evaluator
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch

from solvers.neighborhoods.Neighborhood import Neighborhood
from solvers.neighborhoods.MoveNode import MoveNodeCandidate
from solvers.neighborhoods.MoveNode import MoveNode
from solvers.neighborhoods.EdgePageMove import EdgePageMove
from solvers.neighborhoods.EdgePageMove import EdgePageMoveCandidate

from model.node import Node
from model.edge import Edge
from model.page import Page
from solvers.LocalSearch.VariableNeighborhoodDescent import *
from solvers.evaluators.Evaluator import *
from ThreadRunner import *
import multiprocessing as mp
import numpy as np
from multiprocessing import Process, Lock, Manager

try:
    import tkinter as tk
    from tkinter import *
    from BEP_Visualizer.BEP_visualizer import View
    VIEW=True
except:
    VIEW=False


DEBUG = True

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_usage = '''View or solve book embedding
USAGE
'''

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_usage, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('input', metavar='input-file', type=str, nargs=1, help="Book embedding input")
        parser.add_argument('output', metavar='output-file', type=str, nargs='?', help="Book embedding output file")
        parser.add_argument("-s", "--solve", dest="solve", action="store_true", help="Calculate solution")
        if VIEW:
            parser.add_argument("-v", "--view", dest="view", action="store_true", help="View input file")
        parser.add_argument("-c", "--construction", dest="construction", action="store", default="none", help="Choose construction heuristic")
        parser.add_argument("-r", "--heuristic", dest="heuristic", action="store", default="none", help="Choose meta heuristic")
        parser.add_argument("-n", "--neighborhood", dest="neighborhood", action="store", default="edgemove", help="Choose neighborhood (only for local search)")
        parser.add_argument("-t", "--step", dest="step", action="store", default="best", help="step function (only for local search)")


        #setup runs

        template = ("./instances/instance-01.txt ./results/vnd/instance-01.txt -s -c rnd")
        argstrings = []
        for i in range(1, 16):
            argstrings.append(template.replace("01", str(i).zfill(2)))

        for argstring in argstrings:
            # Process arguments
            args = parser.parse_args(argstring.split())

            graph = Graph()
            graph.read(args.input[0], False)

            with Manager() as manager:
                best_solution = manager.list()
                best_solution.append(100000000)
                best_solution.append(None)
                best_solution.append(-1)
                best_solution.append(0)
                best_solution.append(0)

                crossing_nums = manager.list()

                threads = []
                lock = mp.Lock()

                for _ in range(1):
                    tr1 = ThreadRunner(_*2+0, graph.copy(), best_solution, crossing_nums, ThreadRunner.N_DFS, ThreadRunner.E_GRD_RND, 1, lock, local_search=ThreadRunner.LS_VND, step=Neighborhood.NEXT, neighborhood=ThreadRunner.LS_EDGEMOVE)
                    #tr2 = ThreadRunner(_*2+1, graph.copy(), best_solution, crossing_nums, ThreadRunner.N_DFS, ThreadRunner.E_GRD, 100, lock, local_search=0, step=Neighborhood.NEXT, neighborhood=ThreadRunner.LS_EDGEMOVE)

                    # Start new Threads
                    tr1.start()
                    #tr2.start()

                    # Add threads to thread list
                    threads.append(tr1)
                    #threads.append(tr2)

                for t in threads:
                    t.join()

                print("best:", best_solution[0], "on thread", best_solution[2])

                best = best_solution[1]

                #np_nums = np.array(crossing_nums)
                #print("mean:", np.mean(np_nums), "stddev:", np.std(np_nums), "total runs:", best_solution[3])

                if args.output:
                    #best.write(args.output)
                    #stat_name = os.path.splitext(args.output)[0]+"_meanstd.txt"
                    stat_name = os.path.splitext(args.output)[0]+"_time.txt"
                    with open(stat_name, "w") as stat_file:
                        #outstring = "best: %f, mean: %f, stddev: %f, total runs: %d" % (best_solution[0], np.mean(np_nums), np.std(np_nums), best_solution[3])
                        outstring = "runtime: %f" % (best_solution[4])
                        stat_file.write(outstring)

            if VIEW and args.view:
                root = Tk()
                view = View(root)

                def draw( event):
                    view.draw(best)

                root.bind("<Configure>", draw)

                root.title="BEP Visualizer"
                root.deiconify()
                root.mainloop()

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())
