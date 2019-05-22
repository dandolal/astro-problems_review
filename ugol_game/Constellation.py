import numpy as np


class Constellation:
    def __init__(self, name, bname):
        self.name = name
        self.__neighbors = {}
        self.neighborsCount = 0
        self.bayer_name = bname
        self.is_visited = False
        self.is_possible = True
        self.is_target = False
        # for BFS
        self.bfs_marked = False
        self.bfs_deepness = 0
        self.bfs_previous = None
        # for nextTurn
        self.temporary_visited = False

    def __str__(self):
        return self.name

    def set_neighbors(self, constellation_list):
        for constellation in constellation_list:
            self.__neighbors.update({constellation.name: constellation})
        self.neighborsCount = len(self.__neighbors)

    def get_neighbors(self):
        return self.__neighbors

    def are_all_neighbors_visited(self):
        visited_neighbors_count = 0
        for neighborConstellation in self.get_neighbors().values():
            if neighborConstellation.isVisited:
                visited_neighbors_count += 1
        return visited_neighbors_count == self.neighborsCount

    def is_possible_next_turn(self):
        return not self.is_visited and not self.temporary_visited

    def is_possible_next_bfs(self):
        return self.is_possible_next_turn() and not self.bfs_marked
