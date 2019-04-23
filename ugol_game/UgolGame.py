import numpy as np
from .ConstellationGraph import ConstellationGraph as CG


class HumanErrorException(Exception):
    pass


class UgolGame:

    def __init__(self, constellationGraph):
        self.constellationGraph = constellationGraph
        self.currentConstellation = self.chooseRandomConstellation()
        self.targetConstellation = self.chooseRandomConstellation()
        # self.currentConstellation = self.constellationGraph.constellationDict['Цефей']
        # self.targetConstellation = self.constellationGraph.constellationDict['Большая Медведица']
        self.currentConstellation.isVisited = True
        while self.currentConstellation.name == self.targetConstellation.name:
            self.targetConstellation = self.chooseRandomConstellation()
        for constellation in self.targetConstellation.getNeighbors().values():
            constellation.isPossible = False
            constellation.temporaryVisited = False

    def chooseRandomConstellation(self):
        return self.constellationGraph.getConstellationByIndex(np.random.randint(88))

    def start(self):
        # self.printEndGameLabel()
        for constellation in self.constellationGraph.constellationDict.values():
            print("'{}',".format(constellation.name))
            for neigh in constellation.getNeighbors().values():
                print(neigh, end=' ')
        print("Цель: {}".format(self.targetConstellation))
        print(">> {}".format(self.currentConstellation))
        while True:
            try:
                if self.processTurn(self.getHumanTurn(), True):
                    return
            except HumanErrorException:
                continue
            if self.processTurn(self.nextAITurn(), False):
                return

    def printEndGameLabel(self):
        print("""
            --------------
            |            |
            | КОНЕЦ ИГРЫ |
            |            |
            --------------
        """)

    def processTurn(self, constellation, isHuman):
        self.currentConstellation = constellation
        self.currentConstellation.isVisited = True
        result = 10
        if not isHuman:
            print('>> {}'.format(self.currentConstellation))
        if self.currentConstellation == self.targetConstellation:
            if isHuman:
                result = 2
                self.printEndGameLabel()
            else:
                result = 0
                self.printEndGameLabel()
        if self.isDeadlock():
            self.printEndGameLabel()
            result = 1
        return result

    def predictNextTurn(self, currentConstellation):
        pathList = []
        for constellation in currentConstellation.getNeighbors().values():
            if constellation.isPossibleNextTurn():
                self.constellationGraph.bfs(constellation, self.targetConstellation)
                pathList.append([self.targetConstellation.BFSDeepness, CG.getFirstInBFS(self.targetConstellation)])
        return sorted(pathList, key=lambda x: int(x[0]))

    def nextAITurn(self):
        self.constellationGraph.bfs(self.currentConstellation, self.targetConstellation)
        if self.targetConstellation.BFSDeepness == 0 or self.targetConstellation.BFSPrevious is None:
            return self.nextRandomTurn()
        pathList = self.predictNextTurn(self.currentConstellation)
        if pathList[0][-1].name == self.targetConstellation.name:
            return pathList[0][-1]
        nextConstellationIndex = -1
        for i in range(len(pathList)):
            if pathList[i][0] % 2 == 0 and pathList[i][0] != 0:
                nextConstellationIndex = i
                nextConstellation = pathList[nextConstellationIndex][1]
                nextConstellation.temporaryVisited = True
                humanPathList = self.predictNextTurn(nextConstellation)
                humanNextConstellationIndex = -1
                for j in range(len(humanPathList)):
                    if humanPathList[j][0] % 2 == 0 and humanPathList[j][0] != 0:
                        humanNextConstellationIndex = j
                        humanNextConstellation = humanPathList[humanNextConstellationIndex][1]
                        break
                if humanNextConstellationIndex == -1:
                    humanNextConstellation = humanPathList[-1][1]
                for constellation in humanNextConstellation.getNeighbors().values():
                    if constellation.isPossibleNextTurn() and constellation.isPossible:
                        return nextConstellation
        if nextConstellationIndex == -1:
            return pathList[-1][1]

    def nextRandomTurn(self):
        nextConstellation = None
        for constellation in self.currentConstellation.getNeighbors().values():
            if not constellation.isVisited:
                nextConstellation = constellation
        if nextConstellation is not None:
            return nextConstellation

    def isDeadlock(self):
        isDeadLock = True
        for constellation in self.currentConstellation.getNeighbors().values():
            if not constellation.isVisited:
                isDeadLock = False
        if isDeadLock:
            print('Это тупик, братан...')
        return isDeadLock

    def getHumanTurn(self, constellation):
        error = 'Всё ок!'
        try:
            nextConstellation = self.constellationGraph.constellationDict[constellation]
            if nextConstellation.isVisited:
                error = '!!! Ужe было !!!'
        except KeyError:
            error = '!!! Такого созвездия не сушествует !!!'
            return error
        if nextConstellation not in self.currentConstellation.getNeighbors().values():
            error = '!!! Ошибка !!!'
        # raise HumanErrorException
        return error

    def make_visited(self, constellation):
       constellation.isVisited = True


    def get_constellation(self, constellation):
        ans = self.constellationGraph.constellationDict[constellation]
        return ans
