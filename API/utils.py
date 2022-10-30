import math

import numpy as np


def get_filename(file_name: str):
    return file_name.split(".")[0]


def get_file_content(file_path):
    with open(file_path, "r") as f:
        file = f.read()
    return file


def get_extension(file_name: str):
    return file_name.split(".")[-1]


def convert_coordinates_to_int(coordinates_in_string: str):
    return np.array(list(map(float, (coordinates_in_string.split()))))


def pop_char(string: str, pos) -> str:
    li = list(string)
    li.pop(pos)
    return "".join(li)


def lerp(p0, p1, t):
    """

    :param p0:
    :param p1:
    :param t:
    :return:
    """
    return (1 - t) * p0 + t * p1


def two_d_dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

if __name__ == "__main__":
    print(get_filename("2022-10-18 16/26/40.864833.png"))