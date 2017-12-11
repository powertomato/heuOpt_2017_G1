from solvers.evolution.Population import Population
import random, math

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
            c = self.population.specimen[s1].recombine(self.population.specimen[s2])
            children.append(c)
        return children
    
    def mutate(self, children):
        for i in range(self.mutationsize):    
            c = children[i]
            for j in range( math.ceil(math.log(c.num_nodes_fac)/math.log(2)) ):
                if random.random() < 0.05:
                    c.nodegene = c.nodegene ^ (1 << j)
                    # mutations
            for j in range(random.randint(0,len(c.edgegene)-1)):
                if random.random() < 0.05:
                    c.edgegene[random.randint(0,len(c.edgegene)-1)] = random.randint(0,c.pageNumber-1)