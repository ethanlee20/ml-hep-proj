import sys

import basf2 as b2
import generators as ge
import mdst
import reconstruction as re
import simulation as si


main = b2.Path()


path_dec = "/home/belle2/elee20/ml-hep-proj/scripts/simulate/decay_e.dec"

path_out = '/home/belle2/elee20/ml-hep-proj/data/2024-02-21_e_test/mc_e.root'


main.add_module(
    "EventInfoSetter", evtNumList=[10_000], expList=[0]
)

ge.add_evtgen_generator(
    path=main,
    finalstate="signal",
    signaldecfile=path_dec,
)

si.add_simulation(path=main)

re.add_reconstruction(path=main)

mdst.add_mdst_output(path=main, filename=path_out)


b2.process(path=main)


print(b2.statistics)
