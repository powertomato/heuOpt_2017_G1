from solvers.evolution.Population import Population
import random, math
import numpy as np
from solvers.evolution.Chromosome import *
from solvers.evaluators.Evaluator import *
from solvers.LocalSearch.SimpleLocalSearch import SimpleLocalSearch
from solvers.neighborhoods.EdgePageMove import EdgePageMove
from solvers.neighborhoods.EdgePageMove import EdgePageMoveCandidate
from solvers.neighborhoods.MoveNode import MoveNode
from solvers.neighborhoods.MoveNode import MoveNodeCandidate


from solvers.neighborhoods.Neighborhood import Neighborhood

class GeneticAlgorithm:
    def __init__(self, graph, size, replacements, selectionsize, tournamentsize, mutationsize, evaluator):
        self.replacements = replacements 
        self.populationsize = size
        self.mutationsize = mutationsize
        self.selectionsize = selectionsize
        self.tournamentsize = tournamentsize
        self.evaluator = evaluator
        assert(size>=replacements)
        assert(replacements>=mutationsize)
        assert(size>=selectionsize)
        self.population = Population(graph, size)
    
    def evolve(self):
        while not self.evaluator.criteriaReached(x):
            self.doStep()
            
    def doStep(self, doLocalSearch):
        selection = self.select()
        children = self.recombine(selection)
        self.mutate(children)
        self.population.specimen = self.population.specimen[:self.populationsize-self.replacements]
        for s in self.population.specimen:
            s.chType = ChType.ELITE
        for c in children:
            if doLocalSearch:
                self.doLocalSearch(c)
            self.population.insertSorted(c)

    def doLocalSearch(self, specimen):
        evaluator = TimedEvaluator(datetime.timedelta(seconds=0.1))
        step = Neighborhood.NEXT
        neighborhood = EdgePageMove(step, evaluator)
        #neighborhood = MoveNode(step, evaluator)

        search = SimpleLocalSearch(neighborhood, evaluator)
        graph = specimen.getGraph()
        neighborhood.reset(graph, step)
        x = search.optimize(graph)
        specimen.edgegene = x.getPageAssignment()

    def select(self):
        selection = []
        for i in range(self.selectionsize):
            i,s = self.population.selectSingleTournament(self.tournamentsize)
            selection.append(i)
        return selection
    
    def recombine(self, selection, ratio=0.5):
        tmp = len(selection)-1
        children = []
        for i in range(self.replacements):
            s1 = random.choice(selection)
            s2 = random.choice(selection)
            while s2 == s1:
                s2 = random.choice(selection)
            #print("before recombine:", self.population.specimen[s1].nodegene, self.population.specimen[s2].nodegene)
            c = self.population.specimen[s1].recombine(self.population.specimen[s2], ratio)
            c.chType = ChType.RECOMBINED
            #print("after recombine:", c.nodegene)
            children.append(c)
        return children
    
    def mutate(self, children):
        for i in range(self.mutationsize):    
            c = children[i]
            # TODO: better mutation for nodes
            if random.random() < 1.0:
                c.nodegene = [random.random() for x in range(c.num_nodes)]
                c.chType=ChType.MUTATED
            #for j in range( len(c.nodegene)-1):
                #if random.random() < 0.1:
                    #c.nodegene[j] = c.nodegene[j+1]
                    #c.nodegene.insert(random.randint(0, len(c.nodegene)-1), c.nodegene.pop(j))
                    #c.chType = ChType.MUTATED
                    # mutations
            c.edgegene = [random.randint(0, c.pageNumber-1) for x in range(len(c.edgegene))]