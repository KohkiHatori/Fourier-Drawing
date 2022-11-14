from utils import *
from itertools import combinations
from coeff import Coefficient_calculator
from bezier import PolyBezier


class Merger:

    def __init__(self, paths, num_set):
        self.paths = paths
        self.num_set = num_set
        if num_set > 0:
            self.num_merge = len(paths) - num_set
        else:
            self.num_merge = 0

    def _get_shortest_combinations_of_paths(self, centres: list) -> list:
        combs_centres = list(combinations(range(len(centres)), 2))
        dists = {}
        for combination in combs_centres:
            dist = two_d_dist(centres[combination[0]], centres[combination[1]])
            dists.update({combination: dist})
        to_merge = [comb for comb, _ in sorted(dists.items(), key=lambda item: item[1])]
        return to_merge[:self.num_merge]

    def _get_shortest_combinations_of_points(self, combination):
        path1 = self.paths[combination[0]]
        path2 = self.paths[combination[1]]

    def _merge(self, combs):
        for combination in combs:
            merge_index = self._get_shortest_combinations_of_points(combination)


    def main(self) -> list:
        centres = [Coefficient_calculator(PolyBezier(path), 1).get_coefficient(0) for path in self.paths]
        to_merge = self._get_shortest_combinations_of_paths(centres)
        self._merge(to_merge)
        return self.paths

