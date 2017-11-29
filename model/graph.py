import csv
import os
import numpy as np
import copy
import bisect
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
        node = Node(self, id, self.pageNumber)
        self.nodeIdToIndex[node.id] = len(self.nodes)
        self.nodes.append(node)

    #only called when reading
    def addEdge(self,n1Id,n2Id,p, updateCrossings):
        if n2Id > n1Id:
            n1Id,n2Id=n2Id,n1Id
        edge = Edge(self, len(self.edgeList), n1Id, n2Id, p)

        page = self.pages[p]
        
        self.edgeList.append(edge)
        #bisect.insort(self.edgeList, edge)
        if(updateCrossings):
            self.crossings_valid = True
            self.initCrossingsForEdge(edge)
        else:
            self.crossings_valid = False
    
        page.addEdge(edge)

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

    def initEdgeIds(self):
        for i,edge in enumerate(self.edgeList):
            edge.id = i

    # use only for initialisation!
    def initCrossingsForEdge(self, edge):
        for other in self.edgeList:
            if other != edge:
                #areEdgesCrossing
                e1Idx = (self.nodeIdToIndex[edge.node1], self.nodeIdToIndex[edge.node2])
                if(e1Idx[0] > e1Idx[1]):
                    e1Idx = (e1Idx[1], e1Idx[0])
                    
                e2Idx = (self.nodeIdToIndex[other.node1], self.nodeIdToIndex[other.node2])
                if(e2Idx[0] > e2Idx[1]):
                    e2Idx = (e2Idx[1], e2Idx[0])
                if e1Idx[0]>e2Idx[0]:
                    if e2Idx[0] < e1Idx[0] < e2Idx[1] < e1Idx[1]:
                        edge.addCrossing(other.id)
                elif e1Idx[0] < e2Idx[0] < e1Idx[1] < e2Idx[1]:
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
        e1Idx = (self.nodeIdToIndex[e1.node1], self.nodeIdToIndex[e1.node2])
        if(e1Idx[0] > e1Idx[1]):
            e1Idx = (e1Idx[1], e1Idx[0])
            
        e2Idx = (self.nodeIdToIndex[e2.node1], self.nodeIdToIndex[e2.node2])
        if(e2Idx[0] > e2Idx[1]):
            e2Idx = (e2Idx[1], e2Idx[0])
        if e1Idx[0]>e2Idx[0]:
           return e2Idx[0] < e1Idx[0] < e2Idx[1] < e1Idx[1]
       
        return e1Idx[0] < e2Idx[0] < e1Idx[1] < e2Idx[1]

    def numCrossingsIfAddedToPage(self, edge, p):
        crossings = 0
        for other in self.pages[p].getEdges():
            #if self.areEdgesCrossing(edge, other): 
            e1Idx = (self.nodeIdToIndex[edge.node1], self.nodeIdToIndex[edge.node2])
            if(e1Idx[0] > e1Idx[1]):
                e1Idx = (e1Idx[1], e1Idx[0])
                
            e2Idx = (self.nodeIdToIndex[other.node1], self.nodeIdToIndex[other.node2])
            if(e2Idx[0] > e2Idx[1]):
                e2Idx = (e2Idx[1], e2Idx[0])
            if e1Idx[0]>e2Idx[0]:
                if e2Idx[0] < e1Idx[0] < e2Idx[1] < e1Idx[1]:
                    crossings += 1
            elif e1Idx[0] < e2Idx[0] < e1Idx[1] < e2Idx[1]:
                crossings += 1

        return crossings

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
    
    def getCrossingSetForPage(self, pageid, edgeid):
        return self.edgeList[edgeid].getCrossingSetForPage(pageid)

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
            self.pageNumber = int(first[0])
            for _ in range(self.pageNumber):
                self.pages.append(Page(self, _))

            #edges = list()
            for row in reader:
                if row[0][0] is '#':
                    continue
                elif len(row) is 1:
                    self.addNode( int(row[0]) ) 
                else:
                    self.addEdge( int(row[0]), int(row[1]), int(row[2][1:-1]), updateCrossings) 
                                  
            if updateCrossings:
                self.initEdgeIds()
    
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
            return self.pages == other.pages
        return False
    
    def __ne__(self, other):
        return not self == other
