import numpy as np


class Constellation:
    def __init__(self, name, bname):
        self.name = name
        self.__neighbors = {}
        self.neighborsCount = 0
        self.baierName = bname
        self.isVisited = False
        self.isPossible = True
        self.isTarget = False
        # for BFS
        self.BFSMarked = False
        self.BFSDeepness = 0
        self.BFSPrevious = None
        # for nextTurn
        self.temporaryVisited = False

    def __str__(self):
        return self.name

    def setNeighbors(self, constellationList):
        for constellation in constellationList:
            self.__neighbors.update({constellation.name: constellation})
        self.neighborsCount = len(self.__neighbors)

    def getNeighbors(self):
        return self.__neighbors

    def areAllNeighborsVisited(self):
        visitedNeighborsCount = 0
        for neighborConstellation in self.getNeighbors().values():
            if neighborConstellation.isVisited:
                visitedNeighborsCount += 1
        return visitedNeighborsCount == self.neighborsCount

    def isPossibleNextTurn(self):
        return not self.isVisited and not self.temporaryVisited

    def isPossibleNextBFS(self):
        return self.isPossibleNextTurn() and not self.BFSMarked
