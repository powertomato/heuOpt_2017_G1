import random

from solvers.neighborhoods.EdgePageMove import *
from solvers.neighborhoods.Neighborhood import *
from solvers.evolution.Population import *
from solvers.LocalSearch.SimpleLocalSearch import *
from solvers.evaluators.Evaluator import *


class GeneticAlgorithm:
    def __init__(self, graph, size, replacements, selectionsize, tournamentsize, mutationsize, mut_imm_rate=0.8, mut_rate=0.1, localsearch_time=0.1, evaluator=None):
        self.replacements = replacements 
        self.populationsize = size
        self.mutationsize = mutationsize
        self.mut_imm_rate = mut_imm_rate
        self.mut_rate = mut_rate
        self.selectionsize = selectionsize
        self.tournamentsize = tournamentsize
        self.localsearch_time = localsearch_time
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
        children.extend(self.mutate(selection))

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
        children = []
        for i in range(self.replacements-self.mutationsize):
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
    
    def mutate(self, selection):
        children = []
        for i in range(self.mutationsize):
            c = copy.deepcopy(self.population.specimen[selection[i]])
            if(random.random() > self.mut_imm_rate):
                if random.random() < 1.0:
                   c.nodegene = [random.random() for x in range(c.num_nodes)]
                   c.chType=ChType.MUTATED
            else:
                for j in range( len(c.nodegene)-1):
                    if random.random() < self.mut_rate:
                        c.nodegene[j] = c.nodegene[j+1]
                        c.nodegene.insert(random.randint(0, len(c.nodegene)-1), c.nodegene.pop(j))
                        c.chType = ChType.MUTATED
                        #mutations
            if(random.random() < 0.5):
                c.edgegene = [random.randint(0, c.pageNumber-1) for x in range(len(c.edgegene))]
            children.append(c)

        return children