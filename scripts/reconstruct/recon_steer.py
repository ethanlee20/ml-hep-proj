
"""Steering file for reconstructing B -> K* ell+ ell-."""



"""
Submit like this:

gbasf2 \
    -p e_mixed_sideband_mini \
    -s light-2401-ocicat \
    -i /belle/MC/release-06-00-08/DB00002100/MC15ri_b/prod00025630/s00/e1003/4S/r00000/1120240010/mdst/sub00/mdst_000001_prod00025630_task10020000001.root \
    /home/belle2/elee20/ml-hep-proj/scripts/reconstruct/recon_steer.py

    mixed bkg first file: -i /belle/MC/release-06-00-08/DB00002100/MC15ri_b/prod00024821/s00/e1003/4S/r00000/mixed/mdst \
    mixed bkg mini list: --input_dslist /home/belle2/elee20/ml-hep-proj/scripts/reconstruct/lpns_results_gen_mixed_mini.txt \
    signal e first: -i /belle/MC/release-06-00-08/DB00002100/MC15ri_b/prod00025630/s00/e1003/4S/r00000/1120240010/mdst/sub00/mdst_000001_prod00025630_task10020000001.root \
"""


import basf2 as b2
import modularAnalysis as ma
from variables import collections as vc
from variables import utils as vu
from variables import variables as vm
import vertex as vx


ell = 'e'
sideband = False
cut_strength = 'loose' # tight or loose


main = b2.Path()



def append_global_tag():
    gt = ma.getAnalysisGlobaltag()
    b2.conditions.append_globaltag(gt)


def input_to_the_path(ell):

    assert ell in {'mu', 'e'}

    if ell == 'mu':
        test_file = '/home/belle2/elee20/ml-hep-proj/data/2024-04-29_sl_e_test/mc_se_e.root'
    elif ell == 'e':
        test_file = '/home/belle2/elee20/ml-hep-proj/data/2024-04-29_sl_e_test/mc_se_e.root'

    ma.inputMdstList(
        filelist=[test_file],
        path=main,
        environmentType="default",
    )


def reconstruct_generator_level(ell):
    
    assert ell in {'mu', 'e'}

    ma.fillParticleListFromMC(decayString="K+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString="pi-:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString=f"{ell}+:gen", cut="", path=main)
    ma.fillParticleListFromMC(decayString=f"{ell}-:gen", cut="", path=main)

    ma.reconstructMCDecay("K*0:gen =direct=> K+:gen pi-:gen", cut="", path=main)
    ma.reconstructMCDecay(f"B0:gen =direct=> K*0:gen {ell}+:gen {ell}-:gen", cut="", path=main)


def reconstruct_detector_level(ell, sideband=False, cut_strength='tight'):

    assert ell in {'mu', 'e'}
    assert cut_strength in {'tight', 'loose'}    
    assert sideband in {True, False}

    if ell == 'e':
        marker = '?addbrems'
    elif ell == 'mu':
        marker = ''

    dz_cut = "abs(dz) < 4"
    dr_cut = "dr < 2"
    if cut_strength == 'tight':
        muonID_min = 0.9
        electronID_min = 0.9
        kaonID_min = 0.9
        invMKst_width_scale = 1.5
    elif cut_strength == 'loose':
        muonID_min = 0.80
        electronID_min = 0.80
        kaonID_min = 0.80
        invMKst_width_scale = 2

    muon_cut = f"[muonID > {muonID_min}] and [p > 0.6] and [{dr_cut}] and [{dz_cut}]  and thetaInCDCAcceptance"
    electron_cut = f"[pidChargedBDTScore(11, ALL) > {electronID_min}] and [p > 0.2] and [{dr_cut}] and [{dz_cut}] and thetaInCDCAcceptance"
    kaon_cut = f"[kaonID > {kaonID_min}] and [{dr_cut}] and [{dz_cut}] and thetaInCDCAcceptance"
    pion_cut = f"[{dr_cut}] and [{dz_cut}] and thetaInCDCAcceptance"
    
    if (cut_strength=='loose') & (ell=='e'):
        deltaE_cut = '-0.075 <= deltaE <= 0.05'
    else:
        deltaE_cut = 'abs(deltaE) <= 0.05'

    if sideband:
        Mbc_cut = "5.2 < Mbc < 5.26"
    else: 
        Mbc_cut = "Mbc > 5.27"

    if ell == 'e':
        ma.fillParticleList(decayString="e+:raw", cut='', path=main)
        vm.addAlias("goodFWDGamma", "passesCut(clusterReg == 1 and clusterE > 0.075)")
        vm.addAlias("goodBRLGamma", "passesCut(clusterReg == 2 and clusterE > 0.05)")
        vm.addAlias("goodBWDGamma", "passesCut(clusterReg == 3 and clusterE > 0.1)")
        vm.addAlias("goodGamma", "passesCut(goodFWDGamma or goodBRLGamma or goodBWDGamma)")
        ma.fillParticleList(decayString="gamma:brems", cut="goodGamma", path=main)
        ma.correctBrems("e+:det", "e+:raw", "gamma:brems", path=main)

        ma.applyChargedPidMVA(['e+:det'], path=main, trainingMode=1)
        ma.applyCuts("e+:det", electron_cut, path=main)

    elif ell == 'mu':
        ma.fillParticleList(decayString="mu+:det", cut=muon_cut, path=main)

    ma.fillParticleList(decayString="K+:det", cut=kaon_cut, path=main)
    ma.fillParticleList(decayString="pi-:det", cut=pion_cut, path=main)

    vm.addAlias("invM_Kst", "0.892")
    vm.addAlias("fullwidth_Kst", "0.05")
    ma.reconstructDecay(
        "K*0:det =direct=> K+:det pi-:det", 
        cut=f"abs(formula(daughterInvM(0, 1) - invM_Kst)) <= formula({invMKst_width_scale} * fullwidth_Kst)", 
        path=main
    )

    ma.reconstructDecay(
        f"B0:det =direct=> K*0:det {ell}+:det {ell}-:det {marker}", 
        cut=f"[{deltaE_cut}] and [{Mbc_cut}]", 
        path=main
    )
    
    vx.treeFit('B0:det', conf_level=0.00, updateAllDaughters=True, ipConstraint=True, path=main)

    ma.matchMCTruth("B0:det", path=main)


def tree_fit_leptons(ell):
    if ell == 'e':
        marker = '?addbrems'
    elif ell == 'mu':
        marker = ''

    ma.reconstructDecay(
        f"vpho:det =direct=> {ell}+:det {ell}-:det {marker}",
        cut="",
        path=main
    )
    vx.treeFit('vpho:det', conf_level=0.00, updateAllDaughters=False, ipConstraint=False, path=main)


def rest_of_event():
    # build the ROE
    ma.fillParticleList('pi+:all', '', path=main)
    ma.tagCurlTracks('pi+:all', mcTruth=True, selectorType='mva', path=main)
    vm.addAlias('isCurl', 'extraInfo(isCurl)')
    vm.addAlias('isTruthCurl', 'extraInfo(isTruthCurl)')
    vm.addAlias('truthBundleSize', 'extraInfo(truthBundleSize)')

    ma.buildRestOfEvent('B0:det', fillWithMostLikely=True, path=main)

    loose_track = 'dr<10 and abs(dz)<20 and thetaInCDCAcceptance and E<5.5' 
    loose_gamma = "0.05 < clusterE < 5.5"
    tight_track = f'nCDCHits>=0 and thetaInCDCAcceptance and pValue>=0.0005 and \
                    [pt<0.15 and formula(dr**2/36+dz**2/16)<1] or \
                    [0.15<pt<0.25 and formula(dr**2/49+dz**2/64)<1] or \
                    [0.25<pt<0.5 and formula(dr**2/49+dz**2/16)<1] or \
                    [0.5<pt<1 and formula(dr**2/25+dz**2/36)<1] or \
                    [pt>1 and formula(dr**2+dz**2)<1]'
    tight_gamma = f'clusterE>0.05 and abs(clusterTiming)<formula(2*clusterErrorTiming) and abs(clusterTiming)<200 and \
                    beamBackgroundSuppression>0.05 and fakePhotonSuppression>0.1 and minC2TDist>25'
    roe_mask1 = ('my_mask',  loose_track, loose_gamma)
    ma.appendROEMasks('anti-B0:Dl', [roe_mask1], path=main)

    # creates V0 particle lists and uses V0 candidates to update/optimize the Rest Of Event
    ma.updateROEUsingV0Lists('B0:det', mask_names='my_mask', default_cleanup=True, selection_cuts=None,
                            apply_mass_fit=True, fitter='treefit', path=main)

    ma.updateROEMask("B0:det", "my_mask", tight_track, tight_gamma, path=main)
    vm.addAlias('CMS3_weMissM2','weMissM2(my_mask,3)')


def printMCParticles():
    ma.printMCParticles(onlyPrimaries=False, suppressPrint=True, path=main)


def create_variable_lists(ell):

    assert ell in {'mu', 'e'}

    vm.addAlias('tfChiSq', 'extraInfo(chiSquared)')
    vm.addAlias('tfNdf', 'extraInfo(ndf)')
    vm.addAlias('tfRedChiSq', 'formula(tfChiSq / tfNdf)')
    vm.addAlias('mcMother_mcPDG', 'mcMother(mcPDG)')
    vm.addAlias('mcSister_0_mcPDG', 'mcMother(mcDaughter(0, mcPDG))')
    vm.addAlias('mcSister_1_mcPDG', 'mcMother(mcDaughter(1, mcPDG))')
    vm.addAlias('mcSister_2_mcPDG', 'mcMother(mcDaughter(2, mcPDG))')
    vm.addAlias('mcSister_3_mcPDG', 'mcMother(mcDaughter(3, mcPDG))')
    vm.addAlias('mcSister_4_mcPDG', 'mcMother(mcDaughter(4, mcPDG))')
    vm.addAlias('mcSister_5_mcPDG', 'mcMother(mcDaughter(5, mcPDG))')
    vm.addAlias('mcSister_6_mcPDG', 'mcMother(mcDaughter(6, mcPDG))')
    vm.addAlias('e_id_BDT', 'pidChargedBDTScore(11, ALL)')

    std_vars = (
        vc.deltae_mbc
        + vc.inv_mass
        + vc.mc_truth
        + ['mcMother_mcPDG']
        + ['PDG']
        + ['mcSister_0_mcPDG', 'mcSister_1_mcPDG', 'mcSister_2_mcPDG', 'mcSister_3_mcPDG', 'mcSister_4_mcPDG', 'mcSister_5_mcPDG', 'mcSister_6_mcPDG']
        + vc.pid
        + vc.kinematics
        + vc.mc_kinematics
        + ['dr', 'dz']
        + ['theta', 'thetaErr', 'mcTheta']
        + ['tfChiSq', 'tfNdf', 'tfRedChiSq']
        + ['isSignalAcceptBremsPhotons']
        + ['CMS3_weMissM2']
    )

    Kstar0_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string=f"B0 -> ^K*0 {ell}+ {ell}-",
    )

    K_pi_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string=f"B0 -> [K*0 -> ^K+ ^pi-] {ell}+ {ell}-",
        prefix=["K_p", "pi_m"],
    )

    lepton_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars + ['e_id_BDT'],
        decay_string=f"B0 -> [K*0 -> K+ pi-] ^{ell}+ ^{ell}-",
        prefix=[f"{ell}_p", f"{ell}_m"],
    )

    fake_vpho_vars = vu.create_aliases_for_selected(
        list_of_variables=std_vars,
        decay_string=f"^vpho -> {ell}+ {ell}-",
        prefix=["vpho"]
    )
    
    B0_vars = std_vars + Kstar0_vars + K_pi_vars + lepton_vars + fake_vpho_vars
        
    return B0_vars


def save_output(ell, B0_vars):
    assert ell in {'mu', 'e'}
    out_file_name = f"{ell}_re"
    root_ext = ".root"
    # udst_ext = ".udst"
    # mdst_ext = ".mdst"

    ma.variablesToNtuple(
        decayString="B0:gen",
        variables=B0_vars,
        filename=out_file_name + root_ext,
        treename="gen",
        path=main,
    )

    ma.variablesToNtuple(
        decayString="B0:det",
        variables=B0_vars,
        filename=out_file_name + root_ext,
        treename="det",
        path=main,
    )

    # udst.add_udst_output(
    #     filename=out_file_name + udst_ext + root_ext,
    #     particleLists=['B0:det','B0:gen'],
    #     path=main,
    #     mc=True,
    # )
    
    # mdst.add_mdst_output(
    #     path=main,
    #     mc=True,
    #     filename=out_file_name + mdst_ext + root_ext,
    # )


append_global_tag()

input_to_the_path(ell)

reconstruct_generator_level(ell)

reconstruct_detector_level(ell, sideband=sideband, cut_strength=cut_strength)

rest_of_event()

tree_fit_leptons(ell)

printMCParticles()

B0_vars = create_variable_lists(ell)

save_output(ell, B0_vars)

b2.process(main)

print(b2.statistics)
