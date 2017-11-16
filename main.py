#!/usr/bin/python3
# encoding: utf-8

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from model.graph import Graph
from BEP_Visualizer.BEP_visualizer import View
from solvers.GreedyLongestChain import *
from solvers.FastGreedy import *
from solvers.DepthFirstVertexOrder import *
from model.node import Node
from model.edge import Edge
from model.page import Page

import tkinter as tk
from tkinter import *

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
        parser.add_argument("-v", "--view", dest="view", action="store_true", help="View input file")
        parser.add_argument("-c", "--construction", dest="construction", action="store", default="dfs", help="Choose construction heuristic")

        # Process arguments
        args = parser.parse_args()
        
        graph = Graph()
        graph.read(args.input[0])
        
        if args.solve:
            if  args.construction.lower() == "greedylongestchain":
                print("Creating initial solution using greedy longest chain method")
                constructSolutionGreedyLongestChain(graph)
            elif args.construction.lower() == "fastgreedy":
                print("Creating initial solution using fast greedy method")
                constructSolutionFast(graph)
            elif args.construction.lower() == "dfs":
                print("Creating initial vertex order using dfs method")
                constructVertexOrderDFS(graph)
                
        if args.output:
            graph.write(args.output)
            
        if args.view:
            root = Tk()
            view = View(root)

            def draw( event):
                view.draw(graph)
    
            root.bind("<Configure>", draw)
            
            root.title="BEP Visualizer"
            root.deiconify()
            root.mainloop()
        return 0
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