import csv
import os
import numpy as np
from model.node import *
from model.edge import *
from model.page import *

class Graph(object):
    def __init__(self):
        self.nodes = list()
        self.nodeIdToIndex = {}
        self.pages = list()
        self.pageNumber = 0
        self.edgeList = list()
        self.doubled_crossings = 0
        self.doubled_crossings_valid = True

    #only called when reading
    def addNode(self,id):
        node = Node(self, id)
        self.nodeIdToIndex[node.id] = len(self.nodes)
        self.nodes.append(node)

    #only called when reading
    def addEdge(self,n1Id,n2Id,p, updateCrossings):
        edge = Edge(self, len(self.edgeList), n1Id, n2Id, p)

        page = self.pages[p]

        page.addEdge(edge)
        self.edgeList.append(edge)

        n1 = self.getNodeByID(n1Id)
        n1.neighbours.add(n2Id)

        n2 = self.getNodeByID(n2Id)
        n2.neighbours.add(n1Id)

        if(updateCrossings):
            self.crossings_valid = True
            self.initCrossingsForEdge(edge)
        else:
            self.crossings_valid = False

    # use only for initialisation!
    def initCrossingsForEdge(self, edge):
        for other in self.edgeList:
            if other != edge:
                if self.areEdgesCrossing(edge, other):
                    edge.addCrossing(other.id)

    def moveEdgeToPage(self, edge, pageId):
        oldPage = self.pages[edge.pageId]
        assert edge.pageId == oldPage.id
        if(edge.pageId == pageId):
            return
        oldPage.removeEdge(edge)
        self.pages[pageId].addEdge(edge)
        edge.moveToPage(oldPage.id, pageId)
        edge.pageId = pageId

    def areEdgesCrossing(self, e1, e2):
        e1Idx = (self.getNodeIndex(e1.node1), self.getNodeIndex(e1.node2))
        sortedE1Idx = e1Idx
        if(e1Idx[0] > e1Idx[1]):
            sortedE1Idx = (e1Idx[1], e1Idx[0])
        e2Idx = (self.getNodeIndex(e2.node1), self.getNodeIndex(e2.node2))
        sortedE2Idx = e2Idx
        if(e2Idx[0] > e2Idx[1]):
            sortedE2Idx = (e2Idx[1], e2Idx[0])
        if sortedE1Idx[0]>sortedE2Idx[0]:
            tmp = e1Idx
            sortedE1Idx = sortedE2Idx
            sortedE2Idx = tmp

        return sortedE1Idx[0] < sortedE2Idx[0] < sortedE1Idx[1] < sortedE2Idx[1]

    def numCrossingsIfAddedToPage(self, edge, p):
        crossings = 0
        for other in self.pages[p].getEdges():
            if self.areEdgesCrossing(edge, other):
                crossings += 1

        return crossings

    def numCrossings(self):
        num = 0
        for page in self.pages:
            num += page.numCrossings()
            print("page:", page.id, "crossings:", page.numCrossings())

        numEdgelist = 0
        for edge in self.edgeList:
            page = edge.pageId
            numEdgelist += len(edge.perPageCrossedEdges[page])

        assert numEdgelist == num
        assert num % 2 == 0
        return num//2

    def getEdges(self):
        return self.edgeList

    def getNodeByID(self,id):
        return self.nodes[self.nodeIdToIndex[id]]

    def getNodeByIndex(self,idx):
        return self.nodes[idx]

    def getNodeIndex(self,id):
        return self.nodeIdToIndex[id]

    def getDistance(self,n1Id,n2Id):
        i1 = self.nodeIdToIndex[n1Id]
        i2 = self.nodeIdToIndex[n2Id]
        return abs(i1-i2)

    def reorder(self, newOrdering):
        print(newOrdering)
        self.nodes = [self.nodes[i] for i in newOrdering]
        for i in range(len(self.nodes)):
            self.nodeIdToIndex[self.nodes[i].id] = i

        for edge in self.edgeList:
            edge.perPageCrossedEdges = dict()
            print(edge.id, "p:", edge.pageId)

        for edge in self.edgeList:
            self.initCrossingsForEdge(edge)
    
    def read(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            tmp = next(reader)
            tmp = next(reader)
            tmp = next(reader)
            self.pageNumber = int(next(reader)[0])
            for _ in range(self.pageNumber):
                self.pages.append(Page(self, _))

            edges = list()
            for row in reader:
                if row[0][0] is '#':
                    continue
                elif len(row) is 1:
                    self.addNode(int(row[0])) 
                else:
                    edge = Edge(self, len(edges), int(row[0]), int(row[1]),int(row[2][1:-1]))
                    edges.append(edge)

            for edge in edges:
                self.addEdge(edge.node1, edge.node2, edge.pageId, True)
                print("c", edge.id)
    
    def write(self, filepath):
        with open(filepath,"w") as writefile:
            writefile.write("# cathegory: solved")
            writefile.write("# problem: no problem")
            writefile.write("%d\n" % len(self.nodes))
            writefile.write("%d\n" % self.pageNumber)
            
            for node in self.nodes:
                writefile.write("%d\n" % node.id)
            
            for edge in self.getEdges():
                writefile.write("%d %d [%d]\n" % edge)
    
    def copy(self):
        ret = Graph()
        
        ret.nodes = list()
        for node in self.nodes:
            new = node.copy(ret)
        ret.nodeIdToIndex = dict(self.nodeIdToIndex)
        ret.pages = {}
        for pageIdx in self.pages:
            ret.pages[pageIdx] = dict(self.pages[pageIdx])
        ret.pageNumber = ret.pageNumber
    
    def __eq__(self, other):
        return self.pages == other.pages
    
    def __ne__(self, other):
        return not self == other