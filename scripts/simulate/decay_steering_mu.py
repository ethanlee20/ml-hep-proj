import sys

import basf2 as b2
import generators as ge
import mdst
import reconstruction as re
import simulation as si


main = b2.Path()


path_dec_file = "/home/belle2/elee20/ml-hep-proj/scripts/simulate/decay_mu.dec"

path_output = sys.argv[
    1
]  #'/home/belle2/elee20/ml-hep-proj/data/2023-12-8_tryingStopDoubleCandidates/mc_events_mu.root'


main.add_module(
    "EventInfoSetter", evtNumList=[10_000], expList=[0]
)

ge.add_evtgen_generator(
    path=main,
    finalstate="signal",
    signaldecfile=path_dec_file,
)

si.add_simulation(path=main)

re.add_reconstruction(path=main)

mdst.add_mdst_output(path=main, filename=path_output)


b2.process(path=main)


print(b2.statistics)
