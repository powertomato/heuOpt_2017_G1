import os
import sys
import time
import random
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from model.graph import Graph
from solvers.evolution.Evolution import GeneticAlgorithm
from visualization.GA_plot import *

DEBUG = True

def main(argv=None): # IGNORE:C0111
    #print("asdf")
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
        parser.add_argument('configid', type=int, nargs=1)
        parser.add_argument('instanceid', type=int, nargs=1)
        parser.add_argument('seed', type=int, nargs=1)
        parser.add_argument('input_file', type=str, nargs=1)
        parser.add_argument("-p", "--popsize", dest="population_size", action="store", type=int, help="Population Size")
        parser.add_argument("-s", "--selratio", dest="selection_ratio", action="store", type=float, help="Selection Size")
        parser.add_argument("-t", "--tournsize", dest="tournament_size", action="store", type=int, help="Tournament Size")
        parser.add_argument("-r", "--replratio", dest="replacement_ratio", action="store", type=float, help="Replacement Size")
        parser.add_argument("-m", "--mutratio", dest="mutation_ratio", action="store", type=float, help="Mutation Size")
        parser.add_argument("-mir", "--mutimmratio", dest="mut_imm_ratio", action="store", type=float, help="Mutation/Immigration Ratio")
        parser.add_argument("-mr", "--mutrate", dest="mutation_rate", action="store", type=float, help="Mutation Rate")

        starttime = time.time()

        args = parser.parse_args()

        random.seed(args.seed[0])

        graph = Graph()
        graph.read(os.path.join(os.getcwd(), "Instances", args.input_file[0]), False)
        #print(graph.numCrossings())

        pop_size = args.population_size
        sel_size = int(pop_size * args.selection_ratio)
        tourn_size = args.tournament_size
        repl_size = int(pop_size * args.replacement_ratio)
        mut_size = int(pop_size * args.mutation_ratio)
        mut_imm_ratio = args.mut_imm_ratio
        mutrate = args.mutation_rate

        GA = GeneticAlgorithm(graph, pop_size, repl_size, sel_size, tourn_size, mut_size, mut_imm_ratio, mutrate, 0.1, None)
        #plot = GAPlot()

        LS_Interval = 60


        for i in range(200):
            LS = False
            #GA.population.printPopulation(True)
            if i % LS_Interval == LS_Interval - 1:
                LS = True
            GA.doStep(LS)
            #plot.add_specimens(i, 0, GA.population.specimen)

        print(GA.population.bestResult(), int(time.time()-starttime))
        #plot.plot()

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