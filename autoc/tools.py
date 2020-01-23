import numpy as np
from common.constants import *

def convert_weighted(array : np.array) :
    """
    3D-array to 2D-array
    (R^2 + G^2 + B^2) / (R+G+B)
    """
    sqrd = array**2
    sqrd = sqrd.sum(axis = -1)
    norm = array.sum(axis = -1)
    return np.nan_to_num(sqrd/norm, nan=0)

def convert_min(array : np.array) :
    """
    3D-array to 2D-array
    min(R,G,B)
    """
    return array.min(axis = -1)

def convert_min_yellow(array : np.array) :
    """
    3D-array to 2D-array
    min(R,G)
    """
    after = np.empty((array.shape[0], array.shape[1]))
    for x in range(array.shape[0]) :
        for y in range(array.shape[1]) :
            after[x][y] = min(array[x][y][0], array[x][y][1])
    return after

def convert_single_color(array : np.array, color : int) :
    """
    3D-array to 2D-array
    RED(=0) or GREEN(=1) or BLUE(=2)
    """
    after = np.empty((array.shape[0], array.shape[1]))
    for x in range(array.shape[0]) :
        for y in range(array.shape[1]) :
            after[x][y] = array[x][y][color]
    return after

def convert_red(array : np.array) :
    return convert_single_color(array, RED)

def convert_green(array : np.array) :
    return convert_single_color(array, GREEN)

def convert_blue(array : np.array) :
    return convert_single_color(array, BLUE)
