#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Steering file for new physics MC generation.
"""


import sys

import basf2 as b2
import simulation as si
import reconstruction as re
import mdst as mdst
import glob as glob

from helpers import make_dec, remove_dec, mc_filename


dc9_real = float(sys.argv[1])
trial = int(sys.argv[2])
n_events = int(sys.argv[3])

path_dec = make_dec(dc9_real, trial)

# background (collision) files
bg = glob.glob('/group/belle2/dataprod/BGOverlay/early_phase3/release-06-00-05/overlay/BGx1/set0/*.root')
# background if running locally
bg_local = glob.glob('/group/belle2/dataprod/BGOverlay/early_phase3/release-06-00-05/overlay/BGx1/set0/*.root')

# set database conditions (in addition to default)
b2.conditions.prepend_globaltag("mc_production_MC15ri_a")

# create path
main = b2.Path()

# default to early phase 3 (exp=1003), run 0
main.add_module("EventInfoSetter", expList=1003, runList=0, evtNumList=n_events)

# generate events from decfile
main.add_module('EvtGenInput', userDECFile=b2.find_file(path_dec))

# detector simulation
si.add_simulation(path=main, bkgfiles=bg)

# reconstruction
re.add_reconstruction(path=main)

# Finally add mdst output (file name overwritten on the grid)
mdst.add_mdst_output(path=main, filename=f"../datafiles/{mc_filename(dc9_real, trial)}")

# process events and print call statistics
b2.process(path=main)
print(b2.statistics)

remove_dec(dc9_real, trial)