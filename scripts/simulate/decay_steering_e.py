import sys
import pathlib as pl

import basf2 as b2
import generators as ge
import mdst
import reconstruction as re
import simulation as si


main = b2.Path()


path_dec = "/home/belle2/elee20/ml-hep-proj/scripts/simulate/decay_e.dec"

out_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-05-02/')
out_dir_path.mkdir(parents=True, exist_ok=True)
file_name = 'mc_e.root'
out_file_path = out_dir_path.joinpath(file_name)


main.add_module(
    "EventInfoSetter", evtNumList=[100], expList=[0]
)

ge.add_evtgen_generator(
    path=main,
    finalstate="signal",
    signaldecfile=path_dec,
)

si.add_simulation(path=main)

re.add_reconstruction(path=main)

mdst.add_mdst_output(path=main, filename=str(out_file_path))

b2.process(path=main)

print(b2.statistics)
