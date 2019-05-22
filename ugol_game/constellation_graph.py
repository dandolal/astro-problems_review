from .constellation import Constellation
from queue import Queue


class ConstellationGraph:

    def __init__(self, constellation_dict):
        self.constellation_dict = constellation_dict

    def bfs(self, start_constellation, target_constellation):
        queue = Queue()
        for constellation in self.constellation_dict.values():
            constellation.bfs_marked = False
            constellation.bfs_deepness = 0
            constellation.bfs_previous = None
        start_constellation.bfs_marked = True
        queue.put(start_constellation)
        while not queue.empty():
            current_constellation = queue.get()
            if current_constellation.name == target_constellation.name:
                return current_constellation.bfs_deepness
            for constellation in current_constellation.get_neighbors().values():
                if constellation.is_possible_next_bfs():
                    constellation.bfs_marked = True
                    constellation.bfs_deepness = current_constellation.bfs_deepness + 1
                    constellation.bfs_previous = current_constellation
                    queue.put(constellation)

    @staticmethod
    def get_first_in_bfs(target_constellation):
        current_constellation = target_constellation
        while current_constellation.bfs_previous is not None:
            current_constellation = current_constellation.bfs_previous
        return current_constellation

    def get_constellation_by_index(self, ind):
        return list(self.constellation_dict.values())[ind]


def csv_to_constellation_graph(filename):
    file = open(filename, 'r', encoding='UTF8')
    constellation_dict = {}
    for line in file:
        data = line[:-1].split(',')
        current_constellation = Constellation(data[1], data[0])
        constellation_dict.update({current_constellation.name: current_constellation})
    file.close()
    file = open(filename, 'r', encoding='UTF8')
    for line in file:
        data = line[:-1].split(',')
        current_constellation = constellation_dict[data[1]]
        neighbors = []
        for constellation_name in data[3:]:
            neighbors.append(constellation_dict[constellation_name])
        current_constellation.set_neighbors(neighbors)
    file.close()
    return ConstellationGraph(constellation_dict)
