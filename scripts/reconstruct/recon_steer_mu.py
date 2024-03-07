
"""Steering file for reconstructing B -> K* mu+ mu-."""


import basf2 as b2
import modularAnalysis as ma
from variables import collections as vc
from variables import utils as vu


main = b2.Path()


def append_global_tag():
    gt = ma.getAnalysisGlobaltag()
    b2.conditions.append_globaltag(gt)


def input_to_the_path():
    ma.inputMdstList(
        filelist=['/home/belle2/elee20/ml-hep-proj/data/2024-01-08_LargeMu/mc_1.root'],
        path=main,
        environmentType="default",
    )


def reconstruct_generator_level():
    ma.fillParticleListFromMC(decayString="K+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="pi-:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="mu+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="mu-:gen", cut="", path=main)

    ma.reconstructMCDecay("K*0:gen -> K+:gen pi-:gen", cut="", path=main)
    ma.reconstructMCDecay("B0:gen -> K*0:gen mu+:gen mu-:gen",cut="",path=main,)


def reconstruct_detector_level():
    ma.fillParticleList(decayString="mu+", cut="", path=main)
    ma.applyChargedPidMVA(['mu+'], path=main, trainingMode=1)
    ma.applyCuts("mu+", "pidChargedBDTScore(13, ALL) > 0.9", path=main)

    ma.fillParticleList(decayString="K+", cut="kaonID > 0.9", path=main)
    ma.fillParticleList(decayString="pi-", cut="", path=main)
    ma.reconstructDecay("K*0 -> K+ pi-", cut="", path=main)
    ma.reconstructDecay("B0 -> K*0 mu+ mu-", cut="", path=main)
    ma.matchMCTruth("B0", path=main)


def create_variable_lists():
    std_vars = (
        vc.deltae_mbc
        + vc.inv_mass
        + vc.mc_truth
        + vc.kinematics
        + vc.mc_kinematics
        + ['theta', 'thetaErr', 'mcTheta']
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
    
    B0_vars = dict(
        gen=std_vars + Kstar0_vars + finalstate_vars, 
        det=std_vars + Kstar0_vars + finalstate_vars + ["cosHelicityAngle(0,0)"]
    )

    return B0_vars


def save_output(B0_vars):
    out_file_name = "mu_re.root"

    ma.variablesToNtuple(
        decayString="B0:gen",
        variables=B0_vars['gen'],
        filename=str(out_file_name),
        treename="gen",
        path=main,
    )

    ma.variablesToNtuple(
        decayString="B0",
        variables=B0_vars['det'],
        filename=str(out_file_name),
        treename="det",
        path=main,
    )


input_to_the_path()

reconstruct_generator_level()

reconstruct_detector_level()

B0_vars = create_variable_lists()

save_output(B0_vars)

b2.process(main)

print(b2.statistics)
