from .Constellation import Constellation
from queue import Queue


class ConstellationGraph:

    def __init__(self, constellationDict):
        self.constellationDict = constellationDict

    def bfs(self, startConstellation, targetConstellation):
        queue = Queue()
        for constellation in self.constellationDict.values():
            constellation.BFSMarked = False
            constellation.BFSDeepness = 0
            constellation.BFSPrevious = None
        startConstellation.BFSMarked = True
        queue.put(startConstellation)
        while not queue.empty():
            currentConstellation = queue.get()
            if currentConstellation.name == targetConstellation.name:
                return currentConstellation.BFSDeepness
            for constellation in currentConstellation.getNeighbors().values():
                if constellation.isPossibleNextBFS():
                    constellation.BFSMarked = True
                    constellation.BFSDeepness = currentConstellation.BFSDeepness + 1
                    constellation.BFSPrevious = currentConstellation
                    queue.put(constellation)

    @staticmethod
    def getFirstInBFS(targetConstellation):
        currentConstellation = targetConstellation
        while currentConstellation.BFSPrevious is not None:
            currentConstellation = currentConstellation.BFSPrevious
        return currentConstellation

    def getConstellationByIndex(self, ind):
        return list(self.constellationDict.values())[ind]


def CSVtoConstellationGraph(filename):
    file = open(filename, 'r', encoding='UTF8')
    constellationDict = {}
    for line in file:
        data = line[:-1].split(',')
        # print(data)
        currentConstellation = Constellation(data[1], data[0])
        constellationDict.update({currentConstellation.name: currentConstellation})
    file.close()
    file = open(filename, 'r', encoding='UTF8')
    for line in file:
        data = line[:-1].split(',')
        currentConstellation = constellationDict[data[1]]
        neighbors = []
        for constellationName in data[3:]:
            neighbors.append(constellationDict[constellationName])
        currentConstellation.setNeighbors(neighbors)
    file.close()
    return ConstellationGraph(constellationDict)
