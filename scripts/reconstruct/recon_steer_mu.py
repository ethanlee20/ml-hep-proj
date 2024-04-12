
"""Steering file for reconstructing B -> K* mu+ mu-."""


import basf2 as b2
import modularAnalysis as ma
from variables import collections as vc
from variables import utils as vu
from variables import variables as vm
import vertex as vx
import mdst
import udst


main = b2.Path()


def append_global_tag():
    gt = ma.getAnalysisGlobaltag()
    b2.conditions.append_globaltag(gt)


def input_to_the_path():
    ma.inputMdstList(
        # filelist=['/home/belle2/elee20/ml-hep-proj/scripts/reconstruct/mu_re_save.mdst.root'],
        filelist=['/home/belle2/elee20/ml-hep-proj/data/2024-04-12_mdst_test/sub00/mdst_000001_prod00025631_task10020000001.root'],
        path=main,
        environmentType="default",
    )


def reconstruct_generator_level():
    ma.fillParticleListFromMC(decayString="K+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="pi-:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="mu+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="mu-:gen", cut="", path=main)

    ma.reconstructMCDecay("K*0:gen =direct=> K+:gen pi-:gen", cut="", path=main)
    ma.reconstructMCDecay("B0:gen =direct=> K*0:gen mu+:gen mu-:gen", cut="", path=main)


def reconstruct_detector_level():
    ma.fillParticleList(decayString="mu+:det", cut="muonID > 0.85", path=main)
    
    ma.fillParticleList(decayString="K+:det", cut="kaonID > 0.85", path=main)
    ma.fillParticleList(decayString="pi-:det", cut="", path=main)

    vm.addAlias("invM_Kst", "0.892")
    vm.addAlias("fullwidth_Kst", "0.05")
    ma.reconstructDecay("K*0:det =direct=> K+:det pi-:det", cut=f"abs(formula(daughterInvM(0, 1) - invM_Kst)) <= formula(2 * fullwidth_Kst)", path=main)
    
    ma.reconstructDecay("B0:det =direct=> K*0:det mu+:det mu-:det", cut="[abs(deltaE) <= 0.05] and [Mbc > 5.27]", path=main)
    
    vx.treeFit('B0:det', conf_level=0.00, updateAllDaughters=True, ipConstraint=True, path=main)
    vm.addAlias('tfChiSq', 'extraInfo(chiSquared)')
    vm.addAlias('tfNdf', 'extraInfo(ndf)')
    vm.addAlias('tfRedChiSq', 'formula(tfChiSq / tfNdf)')

    ma.matchMCTruth("B0:det", path=main)


def printMCParticles():
    ma.printMCParticles(onlyPrimaries=False, suppressPrint=True, path=main)


def create_variable_lists():
    std_vars = (
        vc.deltae_mbc
        + vc.inv_mass
        + vc.mc_truth
        + vc.pid
        + vc.kinematics
        + vc.mc_kinematics
        + ['theta', 'thetaErr', 'mcTheta']
        + ['tfChiSq', 'tfNdf', 'tfRedChiSq']
        + ['PDG']
    )

    Kstar0_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string="B0 -> ^K*0 mu+ mu-",
    )

    finalstate_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string="B0 -> [K*0 -> ^K+ ^pi-] ^mu+ ^mu-",
        prefix=["K_p", "pi_m", "mu_p", "mu_m"],
    )
    
    B0_vars = dict(
        gen=std_vars + Kstar0_vars + finalstate_vars, 
        det=std_vars + Kstar0_vars + finalstate_vars
    )

    return B0_vars


def save_output(B0_vars):
    out_file_name = "mu_re"
    root_ext = ".root"
    udst_ext = ".udst"
    mdst_ext = ".mdst"

    ma.variablesToNtuple(
        decayString="B0:gen",
        variables=B0_vars['gen'],
        filename=out_file_name + root_ext,
        treename="gen",
        path=main,
    )

    ma.variablesToNtuple(
        decayString="B0:det",
        variables=B0_vars['det'],
        filename=out_file_name + root_ext,
        treename="det",
        path=main,
    )

    udst.add_udst_output(
        filename=out_file_name + udst_ext + root_ext,
        particleLists=['B0:det','B0:gen'],
        path=main,
        mc=True,
    )
    
    mdst.add_mdst_output(
        path=main,
        mc=True,
        filename=out_file_name + mdst_ext + root_ext,
    )


append_global_tag()

input_to_the_path()

reconstruct_generator_level()

reconstruct_detector_level()

printMCParticles()

B0_vars = create_variable_lists()

save_output(B0_vars)

b2.process(main)

print(b2.statistics)
