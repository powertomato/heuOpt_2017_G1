import csv
import os

class Graph(object):
    def __init__(self):
        self.nodes = list()
        self.nodeIdToIndex = {}
        self.pages = {}
        self.pageNumber = 1

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
        self.pageNumber = max(self.pageNumber, p)
        
        if not p in self.pages:
            self.pages[p] = set()
        page = self.pages[p]
        
        n1Id,n2Id = self._normalizeEdge(n1Id,n2Id)
        
        if self.hasEdge(n1Id,n2Id):
            return
        
        page.add((n1Id, n2Id))
        
        n1 = self.getNodeByID(n1Id)
        n1.neighbours.add(n2Id)
        
        n2 = self.getNodeByID(n2Id)
        n2.neighbours.add(n1Id)
        
    def areEdgesCrossing(self, e1, e2):
        e1Idx = (self.getNodeIndex(e1[0]), self.getNodeIndex(e1[1]))
        e2Idx = (self.getNodeIndex(e2[0]), self.getNodeIndex(e2[1]))
        if e1Idx[0]>e2Idx[0]:
            tmp = e1Idx
            e1Idx = e2Idx
            e2Idx = tmp
        return e2Idx[0] < e1Idx[1] and e2Idx[1] > e1Idx[1]
        
    def canAddToPage(self,n1Id, n2Id, p):
        if not p in self.pages:
            return True
        toCheck = self._normalizeEdge(n1Id,n2Id)
        if toCheck in self.pages[p]:
            return False
        for edge in self.pages[p]:
            if self.areEdgesCrossing(toCheck, edge):
                return False
        return True
        
    def getEdges(self):
        for page in self.pages:
            for edge in self.pages[page]:
                yield (edge[0], edge[1], page)
        
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
    
    def read(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            tmp = next(reader)
            tmp = next(reader)
            tmp = next(reader)
            self.pageNumber = int(next(reader)[0])
            for row in reader:
                if row[0][0] is '#':
                    continue
                elif len(row) is 1:
                    self.addNode(int(row[0])) 
                else:
                    self.addEdge(int(row[0]), int(row[1]),int(row[2][1:-1]))
    
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
            
    def _insertionSort(self,alist):
        for index in range(1,len(alist)):
    
            currentvalue = alist[index]
            position = index
    
            while position>0 and alist[position-1][0]>currentvalue[0]:
                alist[position]=alist[position-1]
                position = position-1
    
            alist[position]=currentvalue
                