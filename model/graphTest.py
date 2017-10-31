import unittest
from model.graph  import Graph
from solvers.DepthFirstVertexOrder import *
from solvers.helper import _edges

class graphTester(unittest.TestCase):

    def setUp(self):
        self.inputfile = "./instances/automatic-0.txt"
        self.graph = Graph()
        self.graph.read(self.inputfile)

    def test_read(self):
        self.assertEqual(len(self.graph.nodes), 4)
        self.assertEqual(self.graph.pageNumber, 2)

        edges = list()
        for edge in self.graph.getEdges():
            edges.append(edge)

        self.assertEqual(len(edges), 7)

    def test_edges_helper(self):
        edges = list()
        for edge in _edges(self.graph.pages):
            edges.append(edge)
        self.assertEqual(len(edges), 7)

        edges = list()
        for edge in _edges(self.graph.pages[0:1]):
            edges.append(edge)
        self.assertEqual(len(edges), 4)


    def test_DFS(self):
        constructVertexOrderDFS(self.graph)

if __name__ == '__main__':
    unittest.main()
