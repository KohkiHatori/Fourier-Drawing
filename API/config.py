import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# The step of t. t goes from 0 to 1, so the number of steps is the reciprocal of DT.
DT = 0.0001
# The number of rotating vectors used in the drawing
NUM = 100

# _______________________________________________________________________________________________________________________
# Constants
E = math.e
PI = math.pi
COS = math.cos
SIN = math.sin
