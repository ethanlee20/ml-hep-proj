import basf2 as b2
import modularAnalysis as ma
from variables import collections as vc
from variables import utils as vu


main = b2.Path()


def open_events_file(path_events_file):
    ma.inputMdstList(filelist=path_events_file, path=main, environmentType="default")


def reconstruct_particles():
    ma.fillParticleList(decayString="mu+", cut="muonID > 0.9", path=main)
    ma.fillParticleList(decayString="K-", cut="kaonID > 0.9", path=main)
    ma.fillParticleList(decayString="pi+", cut="", path=main)
    ma.reconstructDecay("K*0 -> K- pi+", cut="", path=main)
    ma.reconstructDecay("B0 -> K*0 mu+ mu-", cut="", path=main)


def match_mc_truth():
    ma.matchMCTruth("B0", path=main)


def find_generator_level_particles():
    ma.findMCDecay(
        list_name="B0:generator_level",
        decay="B0 -> K*0 mu+ mu-",
        appendAllDaughters=True,
        path=main,
    )


def make_variables_lists():
    standard_vars = (
        vc.deltae_mbc + vc.inv_mass + vc.mc_truth + vc.kinematics + vc.mc_kinematics
    )

    Kstar0_vars = vu.create_aliases_for_selected(
        list_of_variables=standard_vars,
        decay_string="B0 -> ^K*0 mu+ mu-",
    )
    finalstate_vars = vu.create_aliases_for_selected(
        list_of_variables=vc.pid + standard_vars,
        decay_string="B0 -> [K*0 -> ^K- ^pi+] ^mu+ ^mu-",
        prefix=["K_m", "pi_p", "mu_p", "mu_m"],
    )
    B0_generator_level_vars = standard_vars + Kstar0_vars + finalstate_vars

    B0_detector_level_vars = (
        standard_vars + Kstar0_vars + finalstate_vars + ["cosHelicityAngle(0,0)"]
    )

    return B0_generator_level_vars, B0_detector_level_vars


def save_variables_to_file(decay_string, variables, tree_name, path_output_file):
    ma.variablesToNtuple(
        decayString=decay_string,
        variables=variables,
        filename=path_output_file,
        treename=tree_name,
        path=main,
    )


path_input_mc_events_file = "/home/belle2/elee20/ml-hep-proj/mc_creation/mc_events_e.root"
open_events_file(path_input_mc_events_file)

reconstruct_particles()


match_mc_truth()

find_generator_level_particles()

generator_level_variables, detector_level_variables = make_variables_lists()

path_output_file = "/home/belle2/elee20/ml-hep-proj/reconstruction/mc_events_e_reconstructed.root"

save_variables_to_file(
    "B0:generator_level",
    generator_level_variables,
    "generator_variables",
    path_output_file,
)
save_variables_to_file(
    "B0",
    detector_level_variables,
    "detector_variables",
    path_output_file
)

b2.process(main)

print(b2.statistics)


"""
def save_generator_variables():
    standard_vars = (
            vc.deltae_mbc + vc.inv_mass + vc.mc_truth + vc.kinematics + vc.mc_kinematics
    )

    Kstar0_vars = vu.create_aliases_for_selected(
        list_of_variables=standard_vars,
        decay_string="B0 -> ^K*0 mu+ mu-",
    )
    finalstate_vars = vu.create_aliases_for_selected(
        list_of_variables=vc.pid + standard_vars,
        decay_string="B0 -> [K*0 -> ^K- ^pi+] ^mu+ ^mu-",
        prefix=["K_m", "pi_p", "mu_p", "mu_m"],
    )
    B0_gen_vars = standard_vars + Kstar0_vars + finalstate_vars + ["cosHelicityAngle(1,1)"] 
    path_ntupleoutput = "./variables_with_gen_tree.root"
    ma.variablesToNtuple(
        decayString="B0:MyB0",
        variables=B0_gen_vars,
        filename=path_ntupleoutput,
        treename="gen_variables",
        path=main,
    )
"""


"""

How I was saving variables output before:

# save variables to an output file
ma.variablesToNtuple(
    decayString= "B0",
    variables=['Mbc', 'M', 'deltaE', 'isSignal'],
    filename=path_ntupleoutput_B0,
    path=main,
)

ma.variablesToNtuple(
    decayString= "mu+",
    variables=['Mbc', 'M', 'deltaE', 'isSignal', 'muonID'],
    filename=path_ntupleoutput_muplus,
    path=main,
)

ma.variablesToNtuple(
    decayString= "K-",
    variables=['Mbc', 'M', 'deltaE', 'isSignal', 'kaonID'],
    filename=path_ntupleoutput_kminus,
    path=main,
)

ma.variablesToNtuple(
    decayString= "pi+",
    variables=['Mbc', 'M', 'deltaE', 'isSignal', 'pionID'],
    filename=path_ntupleoutput_piplus,
    path=main,
)

ma.variablesToNtuple(
    decayString= "K*0",
    variables=['Mbc', 'M', 'deltaE', 'isSignal'],
    filename=path_ntupleoutput_kstar0,
    path=main,
)
"""
