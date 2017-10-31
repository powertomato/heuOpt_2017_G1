import unittest
from model.graph  import Graph
from solvers.DepthFirstVertexOrder import *

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

    def test_move(self):
        edge = self.graph.getEdges()[2]
        self.graph.moveEdgeToPage(edge, 1)
        self.assertEqual(edge.page, 1)
        self.graph.moveEdgeToPage(edge, 0)
        self.assertEqual(edge.page, 0)

    def test_DFS(self):
        constructVertexOrderDFS(self.graph)
        self.assertEqual(1, 1)

    def test_Crossings(self):
        self.assertEqual(self.graph.numCrossings(), 0)
        edge = self.graph.getEdges()[1]
        self.graph.moveEdgeToPage(edge, 0)
        self.assertEqual(self.graph.numCrossings(), 1)
        self.graph.moveEdgeToPage(edge, 1)
        self.assertEqual(self.graph.numCrossings(), 0)
        self.graph.moveEdgeToPage(edge, 0)
        self.assertEqual(self.graph.numCrossings(), 1)

if __name__ == '__main__':
    unittest.main()
