# imports
import basf2 as b2
import generators as ge
import mdst
import reconstruction as re
import simulation as si

# create path
main = b2.Path()


# define input and output file paths
path_dec_file = '/home/belle2/elee20/ml-hep-proj/mc_creation/decay_e.dec'

path_output = '/home/belle2/elee20/ml-hep-proj/mc_creation/mc_events_e.root'


# add simulation generation modules to path
main.add_module("EventInfoSetter", evtNumList=[10_000], expList=[0])

ge.add_evtgen_generator(path=main, finalstate="signal", signaldecfile=path_dec_file)

si.add_simulation(path=main)

re.add_reconstruction(path=main)

mdst.add_mdst_output(path=main, filename=path_output)


# process
b2.process(path=main)


# print statistics
print(b2.statistics)
