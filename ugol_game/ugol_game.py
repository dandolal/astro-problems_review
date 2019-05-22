import numpy as np
from .constellation_graph import ConstellationGraph as CG


class HumanErrorException(Exception):
    pass


class UgolGame:

    def __init__(self, constellation_graph):
        self.constellation_graph = constellation_graph
        self.current_constellation = self.choose_random_constellation()
        self.target_constellation = self.choose_random_constellation()
        self.current_constellation.is_visited = True
        while self.current_constellation.name == self.target_constellation.name:
            self.target_constellation = self.choose_random_constellation()
        for constellation in self.target_constellation.get_neighbors().values():
            constellation.is_possible = False
            constellation.temporary_visited = False

    def choose_random_constellation(self):
        return self.constellation_graph.get_constellation_by_index(
            np.random.randint(len(self.constellation_graph.constellation_dict)))

    def start(self):
        for constellation in self.constellation_graph.constellationDict.values():
            print("'{}',".format(constellation.name))
            for neigh in constellation.get_neighbors().values():
                print(neigh, end=' ')
        print("Цель: {}".format(self.target_constellation))
        print(">> {}".format(self.current_constellation))
        while True:
            try:
                if self.process_turn(self.get_human_turn(), True):
                    return
            except HumanErrorException:
                continue
            if self.process_turn(self.next_ai_turn(), False):
                return

    def print_end_game_label(self):
        print("""
            --------------
            |            |
            | КОНЕЦ ИГРЫ |
            |            |
            --------------
        """)

    def process_turn(self, constellation, is_human):
        self.current_constellation = constellation
        self.current_constellation.is_visited = True
        result = 10
        if not is_human:
            print('>> {}'.format(self.current_constellation))
        if self.current_constellation == self.target_constellation:
            if is_human:
                result = 2
                self.print_end_game_label()
            else:
                result = 0
                self.print_end_game_label()
        if self.is_deadlock():
            self.print_end_game_label()
            result = 1
        return result

    def predict_next_turn(self, current_constellation):
        path_list = []
        for constellation in current_constellation.get_neighbors().values():
            if constellation.is_possible_next_turn():
                self.constellation_graph.bfs(constellation, self.target_constellation)
                path_list.append(
                    [self.target_constellation.bfs_deepness, CG.get_first_in_bfs(self.target_constellation)])
        return sorted(path_list, key=lambda x: int(x[0]))

    def next_ai_turn(self):
        self.constellation_graph.bfs(self.current_constellation, self.target_constellation)
        if self.target_constellation.bfs_deepness == 0 or self.target_constellation.bfs_previous is None:
            return self.next_random_turn()
        path_list = self.predict_next_turn(self.current_constellation)
        if path_list[0][-1].name == self.target_constellation.name:
            return path_list[0][-1]
        next_constellation_index = -1
        for i in range(len(path_list)):
            if path_list[i][0] % 2 == 0 and path_list[i][0] != 0:
                next_constellation_index = i
                next_constellation = path_list[next_constellation_index][1]
                next_constellation.temporary_visited = True
                human_path_list = self.predict_next_turn(next_constellation)
                human_next_constellation_index = -1
                for j in range(len(human_path_list)):
                    if human_path_list[j][0] % 2 == 0 and human_path_list[j][0] != 0:
                        human_next_constellation_index = j
                        human_next_constellation = human_path_list[human_next_constellation_index][1]
                        break
                if human_next_constellation_index == -1:
                    human_next_constellation = human_path_list[-1][1]
                for constellation in human_next_constellation.get_neighbors().values():
                    if constellation.is_possible_next_turn() and constellation.is_possible:
                        return next_constellation
        if next_constellation_index == -1:
            return path_list[-1][1]

    def next_random_turn(self):
        next_constellation = None
        for constellation in self.current_constellation.get_neighbors().values():
            if not constellation.is_visited:
                next_constellation = constellation
        if next_constellation is not None:
            return next_constellation

    def is_deadlock(self):
        is_dead_lock = True
        for constellation in self.current_constellation.get_neighbors().values():
            if not constellation.is_visited:
                is_dead_lock = False
        if is_dead_lock:
            print('Это тупик, братан...')
        return is_dead_lock

    def get_human_turn(self, constellation):
        error = 'Всё ок!'
        try:
            next_constellation = self.constellation_graph.constellation_dict[constellation]
            if next_constellation.is_visited:
                error = '!!! Ужe было !!!'
        except KeyError:
            error = '!!! Такого созвездия не сушествует !!!'
            return error
        if next_constellation not in self.current_constellation.get_neighbors().values():
            error = '!!! Ошибка !!!'
        return error

    def make_visited(self, constellation):
        constellation.is_visited = True

    def get_constellation(self, constellation):
        ans = self.constellation_graph.constellation_dict[constellation]
        return ans
