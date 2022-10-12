from config import *


def get_filename(file_name: str):
    return file_name.split(".")[0]


def get_extension(file_name: str):
    return file_name.split(".")[-1]


def convert_coordinates_to_int(coordinates_in_string: str):
    return np.array(list(map(float, (coordinates_in_string.split()))))


def pop_char(string: str, pos):
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
