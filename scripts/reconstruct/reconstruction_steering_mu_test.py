
import basf2 as b2
import modularAnalysis as ma
from variables import collections as vc
from variables import utils as vu


path_input = '/home/belle2/elee20/ml-hep-proj/data/2023-12-8_tryingStopDoubleCandidates/mc_events_mu.root'
path_output = '/home/belle2/elee20/ml-hep-proj/data/2023-12-8_tryingStopDoubleCandidates/mc_events_mu_reconstructed.root'

main = b2.Path()


def input():
    ma.inputMdstList(filelist=path_input, path=main, environmentType="default")

input()


def reconst_gen():
    ma.fillParticleListFromMC(decayString='K-:gen', cut='', path=main)    
    ma.fillParticleListFromMC(decayString='pi+:gen', cut='', path=main)    
    ma.fillParticleListFromMC(decayString='mu+:gen', cut='', path=main)    
    ma.fillParticleListFromMC(decayString='mu-:gen', cut='', path=main)    

    ma.reconstructMCDecay("K*0:gen -> K-:gen pi+:gen", cut='', path=main)
    ma.reconstructMCDecay("B0:gen -> K*0:gen mu+:gen mu-:gen", cut='', path=main)

reconst_gen()


def reconst_det():
    ma.fillParticleList(decayString="mu+", cut="muonID > 0.9", path=main)
    ma.fillParticleList(decayString="K-", cut="kaonID > 0.9", path=main)
    ma.fillParticleList(decayString="pi+", cut="", path=main)
    ma.reconstructDecay("K*0 -> K- pi+", cut="", path=main)
    ma.reconstructDecay("B0 -> K*0 mu+ mu-", cut="", path=main)
    ma.matchMCTruth("B0", path=main)

reconst_det()
 

def var_lists():
    std_vars = (
        vc.deltae_mbc + vc.inv_mass + vc.mc_truth + vc.kinematics + vc.mc_kinematics
    )

    Kstar0_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string="B0 -> ^K*0 mu+ mu-",
    )
    finalstate_vars = vu.create_aliases_for_selected(
        list_of_variables=vc.pid + std_vars,
        decay_string="B0 -> [K*0 -> ^K- ^pi+] ^mu+ ^mu-",
        prefix=["K_m", "pi_p", "mu_p", "mu_m"],
    )

    B0_gen_vars = std_vars + Kstar0_vars + finalstate_vars

    B0_det_vars = B0_gen_vars + ["cosHelicityAngle(0,0)"]

    return B0_gen_vars, B0_det_vars

B0_gen_vars, B0_det_vars = var_lists()


def save():
    ma.variablesToNtuple(
        decayString='B0:gen',
        variables=B0_gen_vars,
        filename=path_output,
        treename='gen',
        path=main
    )

    ma.variablesToNtuple(
        decayString='B0',
        variables=B0_det_vars,
        filename=path_output,
        treename='det',
        path=main
    )

save()


b2.process(main)

print(b2.statistics)

