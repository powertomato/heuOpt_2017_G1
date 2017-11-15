import csv
import os
import numpy as np

class Edge(object):

    def __init__(self, id, n1Id, n2Id, p):
        self.id = id
        self.node1 = min(n1Id, n2Id)
        self.node2 = max(n1Id, n2Id)
        self.page = p

    def __eq__(self, other):
        return self.id == other.id