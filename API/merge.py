from utils import *
from itertools import chain


def merge(paths: list, num_set: int) -> list:
    num_edge = len(paths)
    if 0 < num_set < num_edge:
        num_merge = num_edge - num_set
        dists = {}
        for i in range(num_edge):
            path1 = paths[i]
            if i != len(paths) - 1:
                path2 = paths[i + 1]
            else:
                path2 = paths[0]
            dist = two_d_dist(path1[-1].points[-1], path2[0].points[0])
            dists.update({i: dist})
        merge_indices = [x for x, _ in sorted(dists.items(), key=lambda item: item[1])][:num_merge]
        paths = rearrange(paths, merge_indices)
        return paths
    elif num_set == 0 or num_edge == num_set:
        return paths
    else:
        raise IndexError("num_set must be between 1 and the number of edges")


def rearrange(paths: list, merge_indices: list):
    finished = False
    while not finished:
        merge_index = merge_indices[0]
        before_indices = check_neighbour(len(paths), merge_index, merge_indices, True)
        after_indices = check_neighbour(len(paths), merge_index, merge_indices, False)
        consecutive = set(before_indices + after_indices + [merge_index])
        head = min(consecutive)
        to_merge = []
        for index in sorted(consecutive, reverse=True):
            to_merge.append(paths[index])
            paths.pop(index)
            if index < head:
                head -= 1
        merged = list(chain.from_iterable(to_merge[::-1]))
        paths.insert(head, merged)
        merge_indices = list(set(merge_indices) - consecutive)
        for index, merge_ind in enumerate(merge_indices.copy()):
            num_smaller = len([ind for ind in list(consecutive) if ind < merge_ind])
            merge_indices[index] = merge_ind - (num_smaller - 1)
        if len(merge_indices) == 0:
            finished = True
    return paths


def check_neighbour(length: int, merge_index: int, merge_indices: list, before_after: bool):
    neighbour = (merge_index + (-1) ** before_after) % length
    if neighbour not in merge_indices:
        if not before_after:
            return [neighbour]
        else:
            return []
    else:
        return [neighbour, *check_neighbour(length, neighbour, merge_indices, before_after)]


