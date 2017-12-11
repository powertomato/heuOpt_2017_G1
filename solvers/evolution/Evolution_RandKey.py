from solvers.evolution.Population import Population
import random, math
import numpy as np

class GeneticAlgorithm:
    def __init__(self, graph, size, replacements, selectionsize, mutationsize, evaluator):
        self.replacements = replacements 
        self.populationsize = size
        self.mutationsize = mutationsize
        self.selectionsize = selectionsize
        self.evaluator = evaluator
        assert(size>=replacements)
        assert(replacements>=mutationsize)
        assert(size>=selectionsize)
        self.population = Population(graph, size)
    
    def evolve(self):
        while not self.evaluator.criteriaReached(x):
            self.doStep()
            
    def doStep(self):
        selection = self.select()
        children = self.recombine(selection)
        self.mutate(children)
        self.population.specimen = self.population.specimen[:self.populationsize-self.replacements] 
        for c in children:
            self.population.insertSorted(c)
        
    def select(self):
        selection = []
        for i in range(self.selectionsize):
            i,s = self.population.selectSingleTournament(10)
            selection.append(i)
        return selection
    
    def recombine(self, selection):
        tmp = len(selection)-1
        children = []
        for i in range(self.replacements):
            s1 = random.randint(0,tmp)
            s2 = random.randint(0,tmp)
            #print("before recombine:", self.population.specimen[s1].nodegene, self.population.specimen[s2].nodegene)
            c = self.population.specimen[s1].recombine(self.population.specimen[s2])
            #print("after recombine:", c.nodegene)
            children.append(c)
        return children
    
    def mutate(self, children):
        for i in range(self.mutationsize):    
            c = children[i]
            # TODO: better mutation for nodes
            #if random.random() < 0.05:
                #random.shuffle(c.nodegene)
            for j in range( len(c.nodegene)-1):
                if random.random() < 0.1:
                    #c.nodegene[j] = c.nodegene[j+1]
                    c.nodegene.insert(random.randint(0, len(c.nodegene)-1), c.nodegene.pop(j))
                    # mutations
            for j in range(random.randint(0,len(c.edgegene)-1)):
                if random.random() < 0.05:
                    c.edgegene[random.randint(0,len(c.edgegene)-1)] = random.randint(0,c.pageNumber-1)