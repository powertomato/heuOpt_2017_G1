import csv
import os
import numpy as np

class Graph(object):
    def __init__(self):
        self.nodes = list()
        self.nodeIdToIndex = {}
        self.pages = list()
        self.pageNumber = 0
        self.edgeMatrix = None #positive values (
        self.edgeList = list()

    #only called when reading
    def addNode(self,id):
        node = Node(self, id)
        self.nodeIdToIndex[node.id] = len(self.nodes)
        self.nodes.append(node)

    #only called when reading
    def addEdge(self,n1Id,n2Id,p):
        edge = Edge(len(self.edgeList), n1Id, n2Id, p)

        page = self.pages[p]

        page.addEdge(edge, False)
        self.edgeList.append(edge)

        n1 = self.getNodeByID(n1Id)
        n1.neighbours.add(n2Id)

        n2 = self.getNodeByID(n2Id)
        n2.neighbours.add(n1Id)

        #for other in self.edgeList:
            #if(self.areEdgesCrossing(edge, other)):
                #self.edgeMatrix[edge.id, other.id] = p+1
                #self.edgeMatrix[other.id, edge.id] = p+1

    def moveEdgeToPage(self, edge, page):
        oldPage = self.pages[edge.page]
        oldPage.removeEdge(edge)
        self.pages[page].addEdge(edge, True)
        edge.page = page

    def setEdgeCrossings(self, n1Id, n2Id, p):
        edges = self.pages[p].edges

        for edge in edges:
            pass

        self.edgeMatrix[(n1Id, n2Id)]

    def areEdgesCrossing(self, e1, e2):
        e1Idx = (self.getNodeIndex(e1.node1), self.getNodeIndex(e1.node2))
        e2Idx = (self.getNodeIndex(e2.node1), self.getNodeIndex(e2.node2))
        if e1Idx[0]>e2Idx[0]:
            tmp = e1Idx
            e1Idx = e2Idx
            e2Idx = tmp
        return e1Idx[0] < e2Idx[0] < e1Idx[1] < e2Idx[1]

    def numCrossingsIfAddedToPage(self, edge, p):
        crossings = 0
        for other in self.pages[p].getEdges():
            if self.areEdgesCrossing(edge, other):
                crossings += 1

        return crossings

    def numCrossings(self):
        num = 0
        for p in self.pages:
            num += p.numCrossings()

        return num

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
        self.nodes = [self.nodes[i] for i in newOrdering]
        for i in range(len(self.nodes)):
            self.nodeIdToIndex[self.nodes[i].id] = i

    
    def read(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            tmp = next(reader)
            tmp = next(reader)
            tmp = next(reader)
            self.pageNumber = int(next(reader)[0])
            for _ in range(self.pageNumber):
                self.pages.append(Page(self))

            edges = list()
            for row in reader:
                if row[0][0] is '#':
                    continue
                elif len(row) is 1:
                    self.addNode(int(row[0])) 
                else:
                    edge = Edge(len(edges), int(row[0]), int(row[1]),int(row[2][1:-1]))
                    edges.append(edge)

            self.edgeMatrix = np.zeros((len(edges), len(edges)), dtype=np.byte)

            for edge in edges:
                self.addEdge(edge.node1, edge.node2, edge.page)
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

    def __init__(self, id, n1Id, n2Id, p):
        self.id = id
        self.node1 = min(n1Id, n2Id)
        self.node2 = max(n1Id, n2Id)
        self.page = p

    def __eq__(self, other):
        return self.id == other.id

class Page(object):
    
    def __init__(self, graph):
        self.graph = graph
        self.edges = list()
        self.crossings = {}
        
    def addEdge(self, edge, calcCrossing):
        self.edges.append(edge)

        if calcCrossing:
            for other in self.edges:
                if(self.graph.areEdgesCrossing(edge, other)):
                    self.addCrossing(edge, other)


    def addCrossing(self, edge1, edge2):
        if(edge1.id not in self.crossings):
            self.crossings[edge1.id] = {}

        if(edge2.id not in self.crossings):
            self.crossings[edge2.id] = {}

        self.crossings[edge1.id][edge2.id] = 1
        self.crossings[edge2.id][edge1.id] = 1

    def removeCrossing(self, edge1, edge2):
        if(self.crossings[edge1.id][edge2.id] == 1):
            del self.crossings[edge1.id][edge2.id]

        if(self.crossings[edge2.id][edge1.id] == 1):
            del self.crossings[edge2.id][edge1.id]

    def numCrossings(self):
        num = 0

        for _, c in self.crossings.items():
            for _, c2 in c.items():
                num += 1

        out = num//2
        print(num)
        assert(num%2 == 0)
        return out
        
    def removeEdge(self, edge):
        toDelete = list()
        if edge in self.edges:
            self.edges.remove(edge)
            if edge.id in self.crossings.keys():
                del self.crossings[edge.id]
            for k, cr in self.crossings.items():
                if edge.id in cr.keys():
                    del cr[edge.id]
                if len(cr.values()) == 0:
                    toDelete.append(k)

        for k in toDelete:
            del self.crossings[k]
                        
    def getEdges(self):
        return self.edges
    