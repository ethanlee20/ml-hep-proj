
from math import radians

import matplotlib.pyplot as plt


def make_one_scaler(min, max):
    def scale(num):
        return (num - min) / (max - min)
    return scale


def make_big_scaler(min, max):
    def scale(num):
        return ((max - min) * num) + min
    return scale


def annotate_theta_accept(xlim:tuple, ylim:tuple):

    one_scale = make_one_scaler(*xlim)
    big_scale = make_big_scaler(*ylim)

    plt.axhline(y=big_scale(0.1), xmin=one_scale(radians(17)), xmax=one_scale(radians(150)), label="PXD, SVD, CDC", color="red")
    plt.axhline(y=big_scale(0.2), xmin=one_scale(radians(31)), xmax=one_scale(radians(128)), label="TOP", color="aquamarine")
    plt.axhline(y=big_scale(0.3), xmin=one_scale(radians(15)), xmax=one_scale(radians(34)), label="ARICH", color="pink")
    plt.axhline(y=big_scale(0.4), xmin=one_scale(radians(12.4)), xmax=one_scale(radians(31.4)), label="ECL", color="green", linestyle="--")
    plt.axhline(y=big_scale(0.4), xmin=one_scale(radians(32.2)), xmax=one_scale(radians(128.7)), color="green", linestyle="--")
    plt.axhline(y=big_scale(0.4), xmin=one_scale(radians(130.7)), xmax=one_scale(radians(155.1)), color="green", linestyle="--")
    plt.axhline(y=big_scale(0.5), xmin=one_scale(radians(40)), xmax=one_scale(radians(129)), label="KLM", color="orange", linestyle=":")
    plt.axhline(y=big_scale(0.5), xmin=one_scale(radians(25)), xmax=one_scale(radians(40)), color="orange", linestyle=":")
    plt.axhline(y=big_scale(0.5), xmin=one_scale(radians(129)), xmax=one_scale(radians(155)), color="orange", linestyle=":")

    plt.legend()