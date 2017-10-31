import csv
import os
import numpy as np

class Graph(object):
    def __init__(self):
        self.nodes = list()
        self.nodeIdToIndex = {}
        self.pages = list()
        self.pageNumber = 0
        self.edgeMatrix = None

    def addNode(self,id):
        node = Node(self, id)
        self.nodeIdToIndex[node.id] = len(self.nodes)
        self.nodes.append(node)

    def hasEdge(self,n1Id,n2Id):
        assert n1Id < n2Id
        for pageIdx in self.pages:
            if (n1Id,n2Id) in self.pages[pageIdx]:
                return True
            return False
    def _normalizeEdge(self,n1Id,n2Id):
        if(n1Id>n2Id):
            tmp = n1Id
            n1Id = n2Id
            n2Id = tmp
        return n1Id,n2Id

    def addEdge(self,n1Id,n2Id,p):
        page = self.pages[p]

        n1Id,n2Id = self._normalizeEdge(n1Id,n2Id)

        page.addEdge(n1Id, n2Id)

        n1 = self.getNodeByID(n1Id)
        n1.neighbours.add(n2Id)

        n2 = self.getNodeByID(n2Id)
        n2.neighbours.add(n1Id)

    def setEdgeCrossings(self, n1Id, n2Id, p):
        edges = self.pages[p].edges

        for edge in edges:


        self.edgeMatrix[(n1Id, n2Id)]

    def areEdgesCrossing(self, e1, e2):
        e1Idx = (self.getNodeIndex(e1[0]), self.getNodeIndex(e1[1]))
        e2Idx = (self.getNodeIndex(e2[0]), self.getNodeIndex(e2[1]))
        if e1Idx[0]>e2Idx[0]:
            tmp = e1Idx
            e1Idx = e2Idx
            e2Idx = tmp
        return e1Idx[0] < e2Idx[0] < e1Idx[1] < e2Idx[1]

    def numCrossingsIfAddedToPage(self, n1Id, n2Id, p):
        crossings = 0

        if not p in self.pages:
            return 0
        toCheck = self._normalizeEdge(n1Id,n2Id)
        if toCheck in self.pages[p]:
            return 0
        for edge in self.pages[p]:
            if self.areEdgesCrossing(toCheck, edge):
                crossings += 1
        return crossings

    def numCrossings(self):
        crossings = 0

        for p in self.pages:
            for edge1 in self.pages[p]:
                for edge2 in self.pages[p]:
                    if self.areEdgesCrossing(edge1, edge2):
                        crossings += 1

        return crossings / 2

    def getEdges(self):
        count = 0
        for page in self.pages:
            for key, edges in page.edges.items():
                for edge in edges:
                    yield (key, edge, count)
            count += 1

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
        self.nodes = [self.nodes[i] for i in newOrdering]
        for i in range(len(self.nodes)):
            self.nodeIdToIndex[self.nodes[i].id] = i

        edges = self.getEdges()
        copiedEdges = list()
        for edge in edges:
            copiedEdges.append(edge)

        self.pages = list()

        for edge in copiedEdges:
            self.addEdge(edge[0], edge[1], 0)

    
    def read(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            tmp = next(reader)
            tmp = next(reader)
            tmp = next(reader)
            self.pageNumber = int(next(reader)[0])
            for _ in range(self.pageNumber):
                self.pages.append(Page())

            numEdges = 0
            for row in reader:
                if row[0][0] is '#':
                    continue
                elif len(row) is 1:
                    self.addNode(int(row[0])) 
                else:
                    self.addEdge(int(row[0]), int(row[1]),int(row[2][1:-1]))
                    numEdges += 1

            self.edgeMatrix = np.zeros((numEdges, numEdges), dtype=np.byte)
    
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
        
                    
class Node(object):
    def __init__(self, graph, id):
        self.id = id
        self.graph = graph
        self.neighbours = set()
        self.neighboursMarked = set()
        
    def markNeighbour(self, n):
        if n in self.neighbours:
            e = self.neighbours
            self.neighboursMarked.add(n)
            self.neighbours.remove(n)
            
    def clearMarkings(self, n):
        self.neighbours.update(self.neighboursMarked)
        self.neighboursMarked.clear()
        
    def getDistances(self, onlyUnmarked=True): 
        distances = []
        for otherId in self.neighbours:
            dist = self.getDistance(otherId,id)
            distances.Add((otherId, dist))
            self._insertionSort(distances)
        if not onlyUnmarked:
            for otherId in self.neighboursNarked:
                dist = self.getDistance(otherId,id)
                distances.Add((otherId, dist))
                self._insertionSort(distances)
                
        return distances

    def getNeighbours(self):
        neighbours = list()
        for otherId in self.neighbours:
            neighbours.append(self.graph.getNodeByID(otherId))
        return neighbours
            
    def _insertionSort(self,alist):
        for index in range(1,len(alist)):
    
            currentvalue = alist[index]
            position = index
    
            while position>0 and alist[position-1][0]>currentvalue[0]:
                alist[position]=alist[position-1]
                position = position-1
    
            alist[position]=currentvalue

    def copy(self, graph=None):
        if(graph==None):
            graph = self.graph
        new = Node(graph, self.id)
        new.neighbours = set(self.neighbours)
        new.neighboursMarked = set(self.neighboursMarked)
                
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return not self == other

class Edge(object):

    def __init__(self, id, n1Id, n2Id):
        self.id = id
        self.node1 = min(n1Id, n2Id)
        self.node2 = max(n1Id, n2Id)
        self.page = 0

class Page(object):
    
    def __init__(self):
        self.edges = {}
        self.redges = {}
        self.crossings = 0
        
    def addEdge(self,id1,id2):
        id1,id2 = self._normalizeEdge(id1, id2)
        if not id1 in self.edges:
            self.edges[id1] = set()

        if not id2 in self.redges:
            self.redges[id2] = set()
            
        self.edges[id1].add(id2)
        self.redges[id2].add(id1)
        
    def removeEdge(self,id1,id2):
        id1, id2 = self._normalizeEdge(id1,id2)
        if id1 in self.edges:
            myset = self.edges[id1]
            del myset[id2]
                
            myset = self.redges[id2]    
            del myset[id1]
                        
    def getAllEdges(self):
        for id1 in self.edges:
            for id2 in self.edges[id1]:
                yield (id1,id2)
            
    def getEdges(self, startId):
        for id2 in self.edges[startId]:
            yield (startId,id2)
                
        
    def _normalizeEdge(self,n1Id,n2Id):
        if(n1Id>n2Id):
            tmp = n1Id
            n1Id = n2Id
            n2Id = tmp
        return n1Id,n2Id
    