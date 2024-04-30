import sys
import pathlib as pl

import basf2 as b2
import generators as ge
import mdst
import reconstruction as re
import simulation as si


main = b2.Path()


path_dec = pl.Path("/home/belle2/elee20/ml-hep-proj/scripts/simulate/sl_e.dec")


path_out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-04-29_sl_e_test/')
path_out_dir.mkdir(parents=True, exist_ok=True)
path_out = path_out_dir.joinpath("mc_se_e.root")



main.add_module(
    "EventInfoSetter", evtNumList=[1_000], expList=[0]
)

ge.add_evtgen_generator(
    path=main,
    finalstate="signal",
    signaldecfile=str(path_dec),
)

si.add_simulation(path=main)

re.add_reconstruction(path=main)

mdst.add_mdst_output(path=main, filename=str(path_out))

b2.process(path=main)

print(b2.statistics)
