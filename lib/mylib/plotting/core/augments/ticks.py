
import matplotlib.pyplot as plt


zero_to_two_pi = {
    nums=[0, np.pi/2, np.pi, (3/2)*np.pi, 2*np.pi],
    syms=[r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
}         

zero_to_pi = {
    nums=[0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi],
    syms= [r"$0$", r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\frac{3\pi}{4}$", r"$\pi$"]
}


def ticks_in_radians(axis, kind):
    if axis == "x":
        ticks = plt.xticks
    elif axis == "y":
        ticks = plt.yticks
        
    if kind == "0 to 2pi":
        ticks(zero_to_two_pi.nums, zero_to_two_pi.syms)
    elif kind == "0 to pi":
        ticks(zero_to_pi.nums, zero_to_pi.syms) 
    else: raise ValueError(f"Unrecognized kind: {kind}")
