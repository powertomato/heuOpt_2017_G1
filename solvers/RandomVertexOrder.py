from model.graph import *
import numpy as np
from numpy import random

def constructVertexOrderRandom(graph):
    nodes = graph.nodes

    random_reordered = np.random.choice(range(len(nodes)), len(nodes), False)

    graph.reorder(random_reordered)

    return nodes