
import sys
import pathlib as pl

import basf2 as b2
import modularAnalysis as ma
from variables import collections as vc
from variables import utils as vu


main = b2.Path()


def get_user_input():
    data_dir_path = pl.Path(sys.argv[1])
    out_file_name = sys.argv[2]
    in_file_names = sys.argv[3:]

    return data_dir_path, out_file_name, in_file_names


def configure_paths(data_dir_path, out_file_name, in_file_names):

    out_file_path = data_dir_path.joinpath(out_file_name)

    in_file_paths = [data_dir_path.joinpath(file_name) for file_name in in_file_names]

    return out_file_path, in_file_paths



def input_to_the_path(in_file_paths):
    ma.inputMdstList(
        filelist=[str(file_path) for file_path in in_file_paths],
        path=main,
        environmentType="default",
    )


def reconstruct_generator_level():
    ma.fillParticleListFromMC(
        decayString="K+:gen", cut="", path=main
    )
    ma.fillParticleListFromMC(
        decayString="pi-:gen", cut="", path=main
    )
    ma.fillParticleListFromMC(
        decayString="mu+:gen", cut="", path=main
    )
    ma.fillParticleListFromMC(
        decayString="mu-:gen", cut="", path=main
    )

    ma.reconstructMCDecay(
        "K*0:gen -> K+:gen pi-:gen", cut="", path=main
    )
    ma.reconstructMCDecay(
        "B0:gen -> K*0:gen mu+:gen mu-:gen",
        cut="",
        path=main,
    )


def reconstruct_detector_level():
    ma.fillParticleList(
        decayString="mu+", cut="muonID > 0.9", path=main
    )
    ma.fillParticleList(
        decayString="K+", cut="kaonID > 0.9", path=main
    )
    ma.fillParticleList(
        decayString="pi-", cut="", path=main
    )
    ma.reconstructDecay("K*0 -> K+ pi-", cut="", path=main)
    ma.reconstructDecay(
        "B0 -> K*0 mu+ mu-", cut="", path=main
    )
    ma.matchMCTruth("B0", path=main)


def create_variable_lists():
    std_vars = (
        vc.deltae_mbc
        + vc.inv_mass
        + vc.mc_truth
        + vc.kinematics
        + vc.mc_kinematics
    )

    Kstar0_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string="B0 -> ^K*0 mu+ mu-",
    )

#    Kstar0_anti_vars = vu.create_aliases_for_selected(
#        list_of_variables=std_vars,
#        decay_string="anti-B0 -> ^anti-K*0 mu+ mu-",
#    )

    finalstate_vars = vu.create_aliases_for_selected(
        list_of_variables=vc.pid + std_vars,
        decay_string="B0 -> [K*0 -> ^K+ ^pi-] ^mu+ ^mu-",
        prefix=["K_p", "pi_m", "mu_p", "mu_m"],
    )
    
#    finalstate_anti_vars = vu.create_aliases_for_selected(
#        list_of_variables=vc.pid + std_vars,
#        decay_string="anti-B0 -> [anti-K*0 -> ^K- ^pi+] ^mu+ ^mu-",
#        prefix=["K_m", "pi_p", "mu_p", "mu_m"],
#    )
       
    B0_vars = dict(
        gen=std_vars + Kstar0_vars + finalstate_vars, 
        det=std_vars + Kstar0_vars + finalstate_vars + ["cosHelicityAngle(0,0)"]
    )

#    B0_anti_vars = dict(
#        gen=std_vars + Kstar0_anti_vars + finalstate_anti_vars,
#        det=std_vars + Kstar0_anti_vars + finalstate_anti_vars + ["cosHelicityAngle(0,0)"]
#    )
        
    return B0_vars


def save_output(B0_vars, out_file_path):
    ma.variablesToNtuple(
        decayString="B0:gen",
        variables=B0_vars['gen'],
        filename=str(out_file_path),
        treename="gen",
        path=main,
    )

    ma.variablesToNtuple(
        decayString="B0",
        variables=B0_vars['det'],
        filename=str(out_file_path),
        treename="det",
        path=main,
    )

#    ma.variablesToNtuple(
#        decayString="anti-B0:gen",
#        variables=B0_anti_vars['gen'],
#        filename=str(out_file_paths['anti-B0']),
#        treename="gen",
#        path=main,
#    )
#
#    ma.variablesToNtuple(
#        decayString="anti-B0",
#        variables=B0_anti_vars['det'],
#        filename=str(out_file_paths['anti-B0']),
#        treename="det",
#        path=main,
#    )


out_file_path, in_file_paths = configure_paths(*get_user_input())

input_to_the_path(in_file_paths)

reconstruct_generator_level()

reconstruct_detector_level()

B0_vars = create_variable_lists()

save_output(B0_vars, out_file_path)

b2.process(main)

print(b2.statistics)
