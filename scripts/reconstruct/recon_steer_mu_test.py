import sys
import pathlib as pl

import basf2 as b2
import modularAnalysis as ma
from variables import collections as vc
from variables import utils as vu


main = b2.Path()


def configure_paths():
    data_dir_path = pl.Path(sys.argv[1])

    in_file_name = sys.argv[2]
    in_file_path = data_dir_path.joinpath(in_file_name)

    out_file_name = sys.argv[3]
    out_file_path = data_dir_path.joinpath(out_file_name)

    return in_file_path, out_file_path


def input_to_the_path(in_file_path):
    ma.inputMdstList(
        filelist=str(in_file_path),
        path=main,
        environmentType="default",
    )


def reconstruct_generator_level():
    ma.fillParticleListFromMC(decayString="K+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="pi-:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="mu+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="mu-:gen", cut="", path=main)

    ma.reconstructMCDecay("K*0:gen -> K+:gen pi-:gen", cut="", path=main)
    ma.reconstructMCDecay(
        "B0:gen -> K*0:gen mu+:gen mu-:gen",
        cut="",
        path=main,
    )


def create_variable_list():
    std_vars = (
        vc.deltae_mbc + vc.inv_mass + vc.mc_truth + vc.kinematics + vc.mc_kinematics
    )

    Kstar0_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string="B0 -> ^K*0 mu+ mu-",
    )
    finalstate_vars = vu.create_aliases_for_selected(
        list_of_variables=vc.pid + std_vars,
        decay_string="B0 -> [K*0 -> ^K+ ^pi-] ^mu+ ^mu-",
        prefix=["K_p", "pi_m", "mu_p", "mu_m"],
    )

    B0_gen_vars = std_vars + Kstar0_vars + finalstate_vars

    return B0_gen_vars


def save_output(B0_gen_vars, out_file_path):
    ma.variablesToNtuple(
        decayString="B0:gen",
        variables=B0_gen_vars,
        filename=str(out_file_path),
        treename="gen",
        path=main,
    )


in_file_path, out_file_path = configure_paths()

input_to_the_path(in_file_path)

reconstruct_generator_level()

B0_gen_vars = create_variable_list()

save_output(B0_gen_vars, out_file_path)

b2.process(main)

print(b2.statistics)
