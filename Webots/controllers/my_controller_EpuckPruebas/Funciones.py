import numpy as np


def bearing(compassValues):
    radian = np.arctan2(compassValues[0],compassValues[1])
    deg = radian*180/3.14
    return deg
