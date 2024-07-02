
"""
Functions for generating / deleting new physics decay files.
"""


import os
from pathlib import Path


def dec_filename(dc9_real, trial):
    result = f"dc9_{str(dc9_real)}_{trial}.dec"
    return result


def make_dec(dc9_real, trial):
    with open('template.dec', 'r') as template:
        text = template.read()
    text = text.replace("DC9REAL", str(dc9_real), 1)

    fname = dec_filename(dc9_real, trial)
    with open(fname, 'x') as dec:
        dec.write(text)
    return fname


def remove_dec(dc9_real, trial):
    os.remove(dec_filename(dc9_real, trial))
    return


def mc_filename(dc9_real, trial):
    result = Path(dec_filename(dc9_real, trial)).with_suffix(".root")
    result = str(result)
    return result