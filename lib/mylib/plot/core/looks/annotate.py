
from math import radians

import matplotlib.pyplot as plt


def make_one_scaler(min, max):
    def scale(num):
        return (num - min) / (max - min)
    return scale


def annotate_theta_accept(xlim:tuple):

    one_scale = make_one_scaler(*xlim)
    
    plt.axhline(y=100, xmin=one_scale(radians(17)), xmax=one_scale(radians(150)), label="PXD, SVD, CDC", color="red")
    plt.axhline(y=200, xmin=one_scale(radians(31)), xmax=one_scale(radians(128)), label="TOP", color="blue")
    plt.axhline(y=300, xmin=one_scale(radians(15)), xmax=one_scale(radians(34)), label="ARICH", color="pink")
    plt.axhline(y=400, xmin=one_scale(radians(12.4)), xmax=one_scale(radians(31.4)), label="ECL", color="green", linestyle="--")
    plt.axhline(y=400, xmin=one_scale(radians(32.2)), xmax=one_scale(radians(128.7)), label="ECL", color="green", linestyle="--")
    plt.axhline(y=400, xmin=one_scale(radians(130.7)), xmax=one_scale(radians(155.1)), label="ECL", color="green", linestyle="--")
    plt.axhline(y=500, xmin=one_scale(radians(40)), xmax=one_scale(radians(129)), label="KLM", color="tan", linestyle=":")
    plt.axhline(y=500, xmin=one_scale(radians(25)), xmax=one_scale(radians(40)), label="KLM", color="tan", linestyle=":")
    plt.axhline(y=500, xmin=one_scale(radians(129)), xmax=one_scale(radians(155)), label="KLM", color="tan", linestyle=":")

    plt.legend()