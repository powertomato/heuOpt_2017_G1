import csv
import os
import numpy as np
import copy
import bisect
from model.node import *
from model.edge import *
from model.page import *
import numpy as np

class Graph(object):
    def __init__(self):
        self.nodes = list()
        self.nodeIdToIndex = {}
        self.pageNumber = 0
        self.edgeList = list()
        self.doubled_crossings = 0
        self.doubled_crossings_valid = True

    #only called when reading
    def addNode(self,id):
        node = Node(self, id, self.pageNumber)
        self.nodeIdToIndex[node.id] = len(self.nodes)
        self.nodes.append(node)

    #only called when reading
    def addEdge(self,n1Id,n2Id,p, updateCrossings):
        if n2Id > n1Id:
            n1Id,n2Id=n2Id,n1Id
        edge = Edge(self, len(self.edgeList), n1Id, n2Id, p)
        
        self.edgeList.append(edge)

        n1Idx = self.nodeIdToIndex[n1Id]
        n2Idx = self.nodeIdToIndex[n2Id]
        dist = abs(n2Idx - n1Idx)

        n1 = self.getNodeByID(n1Id)
        n1.addNeighbor(n2Id,dist,p)
        n1.edges.add(edge)
        #bisect.insort(n1.getNeighborIdx(p),n2Idx)

        n2 = self.getNodeByID(n2Id)
        n2.addNeighbor(n1Id,dist,p)
        n2.edges.add(edge)
        #bisect.insort(n2.getNeighborIdx(p),n1Idx)
                    
    def moveEdgeToPage(self, edge, oldPageId, newPageId):
        n1Id = edge.node1
        n2Id = edge.node2

        n1Idx = self.nodeIdToIndex[n1Id]
        n2Idx = self.nodeIdToIndex[n2Id]
        dist = abs(n2Idx - n1Idx)

        n1 = self.getNodeByID(n1Id)
        n1.moveNeighbor(n2Id, dist, oldPageId, newPageId)

        n2 = self.getNodeByID(n2Id)
        n2.moveNeighbor(n1Id, dist, oldPageId, newPageId)

        edge.pageId = newPageId

    def getPageAssignment(self):
        p = []
        for edge in self.edgeList:
            p.append(edge.pageId)

        return p

    def numCrossings(self):
        num = 0
        for p in range(self.pageNumber):
            
            ends = []
            for idx,node in enumerate(self.nodes):
                #remove "finished" edges
                tmp = bisect.bisect(ends, idx)
                if tmp!=0:
                    ends = ends[tmp:]
                indices = []
                for nid in node.neighbours[p].keys():
                    indices.append(self.nodeIdToIndex[nid])
                toAdd = []
                for idx2 in indices:
                    if idx2 < idx:
                        continue
                    # how many edge ends are smaller than the current index? -> each one is a crossing
                    num += bisect.bisect_left(ends,idx2)
                    # add the end of the edge-end list
                    toAdd.append(idx2)
                for idx2 in toAdd:
                    bisect.insort(ends,idx2)
                    
        return num
#         num = 0
#         for page in self.pages:
#             num += page.numCrossings()
#         return num//2

    def getEdges(self):
        return self.edgeList
    
    def getEdge(self, id):
        return self.edgeList[id]

    def getNodeByID(self,id):
        return self.nodes[self.nodeIdToIndex[id]]

    def getNodeByIndex(self,idx):
        return self.nodes[idx]

    def getDistance(self,n1Id,n2Id):
        i1 = self.nodeIdToIndex[n1Id]
        i2 = self.nodeIdToIndex[n2Id]
        return abs(i1-i2)

    def reorder(self, newOrdering):
        self.nodes = [self.nodes[i] for i in newOrdering]
        for i in range(len(self.nodes)):
            self.nodeIdToIndex[self.nodes[i].id] = i

        for edge in self.edgeList:
            edge.resetCrossings()

        for edge in self.edgeList:
            self.initCrossingsForEdge(edge)
    
    def read(self, filepath, updateCrossings=False):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            first = next(reader)
            while first[0] == "#":
                first = next(reader)

            first = next(reader) # skip node number
            pagenum = int(first[0])

            edges = list()
            nodes = list()
            for row in reader:
                if row[0][0] is '#':
                    continue
                elif len(row) is 1:
                    nodes.append( int(row[0]) ) 
                else:
                    edges.append( (int(row[0]), int(row[1]), int(row[2][1:-1])) ) 
            
            self.initFromLists(pagenum, nodes, edges, updateCrossings)

                
    def initFromLists(self, pagenum, nodelist, edgelist, updateCrossings=False):
        self.pageNumber = pagenum

        for n in nodelist:
            self.addNode( n )
        for e in edgelist:
            self.addEdge( e[0], e[1], e[2], updateCrossings )
    
    def write(self, filepath,normal=True):
        with open(filepath,"w") as writefile:
            writefile.write("# cathegory: solved\n")
            writefile.write("# problem: no problem\n")
            writefile.write("# numcrossings:"+ str(self.numCrossings())+"\n")
            writefile.write("%d\n" % len(self.nodes))
            writefile.write("%d\n" % self.pageNumber)
            
            for node in self.nodes:
                writefile.write("%d\n" % node.id)
            
            if normal:
                for edge in self.getEdges():
                    writefile.write("%d %d [%d]\n" % edge.toTuple())
            else:
                for edge in self.getEdges():
                    writefile.write("{%d}: %d %d [%d] {" % (edge.id, edge.node1, edge.node2, edge.pageId))
                    for page, crossings in edge.perPageCrossedEdges.items():
                        writefile.write("(%d:" %page)
                        for crossing in crossings:
                            writefile.write("%d " % crossing)
                        writefile.write(") ")
                    writefile.write("}\n")
    
    def copy(self):
        return copy.deepcopy(self)
    
    def __eq__(self, other):
        if type(other)==Graph:
            return self.edgeList == other.edgeList
        return False
    
    def __ne__(self, other):
        return not self == other
