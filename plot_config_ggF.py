from samples_HHbbmm import *
import varial
import sys
import ROOT as R
import array
import yaml
import Htautau
# import wrappers

''' usage:
python run_plotting_with_varial.py plot_config_ggF.py input_path plot_tag & 
'''



####################
# General Settings #
####################



input_path = sys.argv[3]
#  'fixbtag_nprebtagjets_newgensum_DR_ttbar'


use_all_signal = False

high_mass = int(sys.argv[4])
PNN = int(sys.argv[5])
channel_name = str(sys.argv[6])
era = sys.argv[7]
run_fakes = int(sys.argv[8])
region = sys.argv[9]
run_dy = True



if channel_name == "et":
    channel_index = 1
elif channel_name == "mt":
    channel_index = 2
else:
    channel_index = 1

embedding_SF = {"2016preVFPmt": 1.15,"2016preVFPet": 1.15,"2016postVFPmt": 0.75,"2016postVFPet": 1.05,"2017et": 0.9,"2017mt": 0.9,"2018et": 0.85,"2018mt": 1    }
luminosities = {
    "2016preVFP": 15.1158e3,
    "2016postVFP": 10.0093e3,
    "2017": 41.5e3,
    "2018": 59.8e3,
    "2022EE":7.875e3,
    "2022postEE":  	26.337e3  }
# 2022 golden json
# C 	 	4.953 	
# D 	 	2.922 	
# E 	 	5.672 	
# F 	 	17.610 	
# G 	 	3.055 	
# postEE  26.337
if era in luminosities:
        lumi = luminosities[era]
else:
        print("Wrong year provided")
        sys.exit(-10)

print(high_mass, sys.argv[4],"===================================")


# samples_name = "sample_database/datasets_Run2.yaml" 
# samples_name = "sample_database/datasets.yaml" 
samples_name = 'sample_database_git/rebin.yaml'
samples_f = open(samples_name, "r") 
samples_list =  yaml.load(samples_f, Loader = yaml.Loader) 

stacking_order = [
'embedding', 
'fakes',
'Z->tautau', 
'Z->ll', 
'wjets', 
'ttbar',
'Single H'
'other',

]
sample_colors = {
'embedding'  :  838,
'fakes' : 617,
# 'electroweak_boson'  :  804,
# 'electroweak_boson'  :  804,
'dyjets'  :  814,
'wjets'  :  632,
# 'ggh_hbb'  :  596,
# 'ggh_htautau'  :  838,
# 'singletop'  :  920,
'ttbar'  :  400,
# 'ttbarFake'  :  596,
'Z->ll'  :  814,
'Z->tautau'  :  864,
# 'vbf_htautau'  :  814,
'diboson'  :  596,
# 'rem_hbb':  615,
'Single H': 838,
'other' : 920, 



}
varial.settings.max_num_processes = 80
varial.settings.rootfile_postfixes += [ '.png'] #'.pdf'
varial.settings.stacking_order = stacking_order
# try to find output on disk and don't run a step if present
enable_reuse_step = True

#################
# Plot Settings #
#################

name = sys.argv[2]
# 'DR-ttbar-Run2-fixbtag_nprebtagjets_newgensum'
weight_dict_mt = {
    # * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Loose_2 *iso_wgt_mu_1 *  trg_wgt_single_mu24ormu27 
    # * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Loose_2 *iso_wgt_mu_1 * trg_wgt_single_mu24ormu27 
    "2022postEE": 'Xsec   * {0} * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight *id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2  '.format(lumi),
    # "2022postEE": 'Xsec   * {0} * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight *id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  *(trg_wgt_ditau_crosstau_2 * trg_cross_mu20tau27_hps  + 1 * (trg_cross_mu20tau27_hps < 1) ) '.format(lumi),
    "2022EE": 'Xsec   * {0} * puweight * genWeight/genEventSumW * btag_weight * FF_weight   * id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1 *(trg_wgt_ditau_crosstau_2 * trg_cross_mu20tau27_hps  + 1 * (trg_cross_mu20tau27_hps < 1) )'.format(lumi),
    "2018": 'Xsec * {0} * genWeight/genEventSumW * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Tight_2 * iso_wgt_mu_1 *  btag_weight * puweight  '.format(lumi),
    "2017": 'Xsec * {0} * genWeight/genEventSumW * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Tight_2 * iso_wgt_mu_1 *  btag_weight * puweight  '.format(lumi),
    "2016": 'Xsec * {0} * genWeight/genEventSumW * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Tight_2 * iso_wgt_mu_1 *  btag_weight * puweight  '.format(lumi),
}

weight_dict_et = {
    ## * puweight is temporarily remove
#       id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 *
#   id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 * 
    "2022postEE": 'Xsec * {0}* puweight * genWeight/genEventSumW *  (id_wgt_tau_vsEle_Tight_2 * id_tau_vsEle_Tight_2 + (1-id_tau_vsEle_Tight_2) ) *  btag_weight * FF_weight * (id_wgt_tau_vsJet_Medium_2 * id_tau_vsJet_Medium_2 + (1-id_tau_vsJet_Medium_2 ) ) * id_wgt_ele_wpTight  ' .format(lumi), #* (trg_wgt_ditau_crosstau_2 * trg_cross_ele24tau30_hps + 1 * (trg_cross_ele24tau30_hps <1) ) * (trg_wgt_single_ele30 * trg_single_ele30 + 1 *(trg_single_ele30 <1)
    "2022EE": 'Xsec * {0}* puweight * genWeight/genEventSumW *  (id_wgt_tau_vsEle_Tight_2 * id_tau_vsEle_Tight_2 + (1-id_tau_vsEle_Tight_2) ) *  btag_weight * FF_weight * (id_wgt_tau_vsJet_Medium_2 * id_tau_vsJet_Medium_2 + (1-id_tau_vsJet_Medium_2 ) ) * id_wgt_ele_wpTight  ' .format(lumi), #* (trg_wgt_ditau_crosstau_2 * trg_cross_ele24tau30_hps + 1 * (trg_cross_ele24tau30_hps <1) ) * (trg_wgt_single_ele30 * trg_single_ele30 + 1 *(trg_single_ele30 <1)
    # "2022postEE": 'Xsec * {0} * genWeight/genEventSumW  '.format(lumi),
    # "2022EE": 'Xsec * {0} * genWeight/genEventSumW   '.format(lumi),

    "2018": 'Xsec * {0} * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 *   btag_weight * puweight  '.format(lumi),
    "2017": 'Xsec * {0} * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 *   btag_weight * puweight  '.format(lumi),
    "2016": 'Xsec * {0} * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 *   btag_weight * puweight  '.format(lumi),
}

weight_dict_tt = {
    ## id_wgt_tau_vsEle_VVLoose_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsMu_VLoose_1 * id_wgt_tau_vsMu_VLoose_2 * id_wgt_tau_vsJet_Medium_1 * id_wgt_tau_vsJet_Medium_2
    ## id_wgt_tau_vsEle_VVLoose_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsMu_VLoose_1 * id_wgt_tau_vsMu_VLoose_2 * id_wgt_tau_vsJet_Medium_1 * id_wgt_tau_vsJet_Medium_2
    "2022postEE": 'Xsec *  {0}* puweight * genWeight/genEventSumW *    btag_weight   *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 *  FF_weight * ( trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 + 1 * (trg_double_tau35_mediumiso_hps <1)) '.format(lumi),
    "2022EE": 'Xsec  *  {0}* puweight * genWeight/genEventSumW *    btag_weight  *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 *  FF_weight * ( trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 + 1 * (trg_double_tau35_mediumiso_hps <1))'.format(lumi),
}

if channel_name == "et":
    weight_dict = weight_dict_et 
elif channel_name == "mt":
    weight_dict = weight_dict_mt 
elif channel_name == "tt":
    weight_dict = weight_dict_tt 
else:
    sys.exit()

if PNN:
    weight = 'Train_weight'
else:
    weight = weight_dict[era]

plot_vars = {
#    'genWeight'           :           ('genWeight',             ';genWeight;',           100,     0,      10000),
}
# mt_tot_b = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 550,  600, 650, 700, 750, 800, 850,  900, 950, 1000, 1100, 1200, 1300, 1400, 1500]
mt_tot_b = [30, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500]
# mt_tot_b  = make_logbinning(20, 2500, 36)
nob_tight_mT = [0, 50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1700.0,2100.0,5000]
m_fastmtt = [0,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220,240,260,300]
PNN_100 = [            0,            0.001232,            0.004982,            0.011598,            0.021114,            0.034304,            0.052314,            0.077834,            0.114538,            0.16762,            0.24431,            0.355564,            0.489926,            0.625302,            0.724916,            0.797848,            0.86386,            0.919758,            1.0]

# met =  make_logbinning(5, 1500, 36)
met = [0,10,20,30,40,50,60,70,80,90,120,140,200,400]
pt =  make_logbinning(20, 1500, 36)
pt = [30,40,50,60,70,80,90,100,120,140,200,350,500, 700, 1000]
mt = make_logbinning(20, 2500, 36)
# from Muon
# plot_vars.update({
#     'pnn_100' : ('pnn_100',     ';PNN 100 [GeV];NEvents', 50,0,1),     
# })
plot_vars.update({
    'dxy_1' : ('dxy_1',';dxy_{1};NEvents',50,-0.1,0.1),
    'dxy_2' : ('dxy_2',';dxy_{2};NEvents',50,-0.1,0.1),
    'dz_1' : ('dz_1',';dz_{1};NEvents',50,-0.2,0.2),
    'dz_2' : ('dz_2',';dz_{2};NEvents',50,-0.2,0.2),
    'eta_1' : ('eta_1',';eta_{1};NEvents',30,-3,3),
    'eta_2' : ('eta_2',';eta_{2};NEvents',30,-3,3),
    'eta_fastmtt' : ('eta_fastmtt',';eta_{#tau#tau};NEvents',100,-10,10),
    'iso_1' : ('iso_1',';iso_{1};NEvents',20,0,0.2),
    'iso_2' : ('iso_2',';iso_{2};NEvents',20,0,0.2),
    # 'jeta_1' : ('jeta_1',';jeta_{1};NEvents',100,-20,20),
    # 'jeta_2' : ('jeta_2',';jeta_{2};NEvents',100,-20,20),
    # 'jphi_1' : ('jphi_1',';jphi_{1};NEvents',100,-20,20),
    # 'jphi_2' : ('jphi_2',';jphi_{2};NEvents',100,-20,20),
    # 'jpt_1' : ('jpt_1',';jpt_{1};NEvents',100,-100,400),
    # 'jpt_2' : ('jpt_2',';jpt_{2};NEvents',100,-100,400),
    'mTdileptonMET' : ('mTdileptonMET',';mTdileptonMET;NEvents',100,0,200),
    'mTdileptonMET_pf' : ('mTdileptonMET_pf',';mTdileptonMET_pf;NEvents',100,0,200),
    'm_fastmtt'       :    ('m_fastmtt', '; m^{#tau#tau};NEvents', 30, 0, 300),
    'm_vis'       :    ('m_vis', '; m^{vis};NEvents', 30, 0, 300),
    'mass_1' : ('mass_1',';mass_{1};NEvents',30,-0.2,0.1),
    'mass_2' : ('mass_2',';mass_{2};NEvents',30,-0.2,0.1),    
    'met' : ('met',';met;NEvents',40,0,400), 
    'metSumEt' : ('metSumEt',';metSumEt;NEvents',200,0,1000),
    'metphi' : ('metphi',';metphi;NEvents',80,-4,4),
    'mt_tot': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents', 50, 0, 500),
    'mt_1' : ('mt_1',';mt_{1};NEvents',50,0,200),
    'mt_2' : ('mt_2',';mt_{2};NEvents',50,0,200),
    'njets' : ('njets',';njets;NEvents',10,0,10),
    # 'nprejets' : ('nprejets',';nprejets;NEvents',10,0,10),
    # 'pfmet' : ('pfmet',';pfmet;NEvents',50,0,500),
    # 'pfmetphi' : ('pfmetphi',';pfmetphi;NEvents',50,-5,5),
    'phi_1' : ('phi_1',';phi_{1};NEvents',50,-5,5),
    'phi_2' : ('phi_2',';phi_{2};NEvents',50,-5,5),
    'phi_fastmtt' : ('phi_fastmtt',';phi_{#tau#tau};NEvents',50,-5,5),
    'pt_1' : ('pt_1',';pt_{1};NEvents',50,0,500),
    'pt_2' : ('pt_2',';pt_{2};NEvents',50,0,500),
    'pt_fastmtt'   :    ('pt_fastmtt', ';p_{T}^{#tau#tau} ;NEvents', 50, 0, 500),
    'pt_tt'   :    ('pt_tt', ';pt_{tt} ;NEvents', 50, 0, 500),
    'pt_vis'   :    ('pt_vis', ';pt_{vis} ;NEvents', 50, 0, 500),

    'pzetamissvis' : ('pzetamissvis',';D_{#zeta};NEvents',35,-200,150),    
    'deltaR_ditaupair' :  ('deltaR_ditaupair', ';#deltaR [GeV];NEvents',60 , 0, 6),
    

    #   'taujet_pt_2':    ('taujet_pt_2', '#tau_{h} jetp_{T}} [GeV];', 20,0,400),
#     'mu0_pt'           :           ('mu0_pt',             ';p_{T}_Mu1 [GeV];',  25,     0,      600),
#     'm_2mu'           :            ('m_2mu',              ';Mass_H(mm) [GeV];', 25,     50,     200),
})


#######################################
# Samples, Selections, and Categories #
#######################################





"""
Xsec: dictionary with key: nick name, value: dictionary of 'xsec', 'era', 'nevents', 'nfiles', 'sample_type'
"""

scope = "mt"
y_bounds = (100,10e6)
treename = 'ntuple'

if run_fakes:
    use_faketau = False
else:
    use_faketau = True
input_pattern = [input_path + '/%s*root']
def get_samples(channel, signal_overlay=True, **kwargs):
    sf_lumi = 1.
    sf_zjb = kwargs.get('sf_zjb', 1.)
    ##########################################
    samples = {}
    ## for the first run, set rerun = True
    
    for nick in samples_list:
        print(nick)
        try:
            xsec = samples_list[nick]['xsec']
        except:
            xsec = 0
        sample_type = samples_list[nick]['sample_type']
        if os.path.exists(input_path):


            if sample_type == 'fakes':
                samples["FF_Combined"] = ['1', 1,   sample_type     , ["FF_Combined"] ,  0 ]
                
            elif 'vbf' in sample_type or 'ggh_hbb' in sample_type or 'ggh' in sample_type or ("H" in nick and "SUSY" not in nick ):
                if "2HDM" not in nick:
                    samples[nick] = ['0.1', 1 ,   "Single H", [nick] ,  0 ]
                else:
                    samples[nick] = ['1000', 1 ,   "1000 * 2HDM 100"      , [nick] ,  0 ] 
            elif sample_type == 'ttbar':
                samples[nick] = ['1', 1 ,   sample_type     , [nick] ,  0 ]
                
            elif 'dyjets_ll' in sample_type:
                # samples[nick] = ['1* (gen_match_2 == {0})'.format(channel_index), 1 ,  "Z->ll"     , [nick] ,  0 ]
                samples[nick] = ['1', 1 ,  "Z->ll"     , [nick] ,  0 ]
            elif 'dyjets_tautau' in sample_type:
                    samples[nick] = ['1', 1 ,  "Z->tautau"     , [nick] ,  0 ]
                # continue

            else:
                # sumofweight = getnickweight(input_path,nick, rerun = get_weight)  
                # if sumofweight != 0:
                    if  'electroweak_boson' in sample_type or 'diboson' in sample_type or 'singletop' in sample_type  :
                        samples[nick] = ['1', 1.,   'other'     , [nick] ,  0 ]
                    elif 'wjets' in sample_type:
                        samples[nick] = ['1', 1.,   'wjets'     , [nick] ,  0 ]
                    else:
                        print("sample type: ", sample_type, "sample name: ", nick)
                        samples[nick] = ['1', 1.,   sample_type     , [nick] ,  0 ]

    samples.update({

            'Data': ["1", 1, 'Data', ['SingleMuon_Run201', 'Tau_Run201', 'EGamma_Run201', 'SingleElectron_Run201', 'DoubleMuon_Run201','MuonEG_Run2', "Muon_Sep", "EGamma_Sep", "SingleMuon_Sep", "Tau_Sep", "Data" ],0],
            
        })
    
    return samples

Htautau = Htautau_selections()
if channel_name == "mt":
    lepton_selection = combinecut( Htautau.mt_triggers_selections[era],Htautau.muon_selections,Htautau.lepton_veto,Htautau.mt_tau_selections[era])
elif channel_name == "et":
    lepton_selection = combinecut( Htautau.et_triggers_selections[era],Htautau.electron_selections,Htautau.lepton_veto,Htautau.et_tau_selections[era])
elif channel_name == "tt":
    lepton_selection = combinecut( Htautau.tt_triggers_selections[era],Htautau.lepton_veto, tt_leadingtau_selections, Htautau.tt_secondtau_selections)
the_samples_dict = get_samples(
    channel='Htt',
    
    signal_overlay=True,
    
    sf_zjb = 1.0,
)
if PNN:
    regions = {
    "ALL"                  : 'mt_1 < 70',
    # "nob_loose_mT" : combinecut(Htautau.nob, Htautau.loose_mT ),
    # "nob_tight_mT" : combinecut(Htautau.nob, Htautau.tight_mT ),
    # "btag_loose_mT"      : combinecut(Htautau.btag, Htautau.loose_mT),
    # "btag_tight_mT"      : combinecut(Htautau.btag, Htautau.tight_mT),
    }
else:
    regions = {
    # 'nob': '1> 0 '
    "nob" : combinecut( Htautau.nob,   lepton_selection,  Htautau.W_true_only, Htautau.opposite_sign, "mt_1 < 70"),
    # "nob_tight_mT" : combinecut(Htautau.nob, Htautau.tight_mT,lepton_selection, Htautau.W_true_only, Htautau.opposite_sign,"mt_1 < 40"),

    
    }
print( "printing cuts applied:   ",regions['nob'] , "for channels: ", channel_name )
if region == "SR":
    pass
elif region == "DR_QCD":
    regions["DR_QCD"] = combinecut(DR_QCD, lepton_selection)
elif region == "DR_W":
    regions["DR_W"] = combinecut(DR_W, lepton_selection, W_true_only)
elif region == "DR_ttbar":
    regions["DR_ttbar"] = combinecut(DR_ttbar, lepton_selection,ttbar_true_only)
else:
    print("wrong region provided!! region supported: SR, DR_QCD,DR_ttbar, DR_W ")
    sys.exit(0)
selections = [
    # Htautau.lepton_veto, # DR selections
#    '{0}>0'.format(weight),  
                                ]
if PNN:
    selections = [ ]

the_category_dict = {
    'Htautau': [regions, selections, plot_vars],
}


# yields_f_tmp = open('sample_database/datayields.yaml', 'r')
# yields = yaml.safe_load(yields_f_tmp)
# bins = yields['bins']


# Blinding the Signal Region
def additional_input_hook(wrps):

    @varial.history.track_history

    def blind_in_HmmWin(w):
        if w.legend == 'Data': # and w.in_file_path.startswith('Hmm_win'):
            # if 'PNN'  in w.name:
                print('BLINDING Data in %s' % w.in_file_path)
                for i in xrange(w.histo.GetNbinsX() + 1):
                    if i < (w.histo.GetNbinsX() - 10) :
                        continue
                    w.histo.SetBinContent(i, 0.)
                    w.histo.SetBinError(i, 0.)
        return w
    def getyields(w):
        region = ["nob_loose","nob_tight","btag_tight","btag_loose"]
        if "mt_tot" in w.name and ("ALL" not in w.in_file_path):
            for r in region:
                yields_l = []
                if r in w.in_file_path:
                    os.system('rm ' + r+'datayields.yaml')
                    w_copy = w.histo.Rebin(len(bins[r])-1,  'w_copy'+r, array.array('d', bins[r]))
                    for i in xrange(1,w_copy.GetNbinsX() + 1):
                        # print('    'combinecut(i, w_copy.GetBinContent(i), w_copy.GetXaxis().GetBinLowEdge(i), w.in_file_path))
                        yields_l.append(w_copy.GetBinContent(i))
                    a = {}
                    a[r] = yields_l
                    os.system('echo ' + r + ': ' + str(a[r]) + ' >> ' + r+'datayields.yaml')                      
                    # with open(r+'datayields.yaml' , 'w') as file:
                    #     yaml.safe_dump(yields, file) 
        return w
    def rebin(w):
        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(len(mt_tot_b)-1, 'rebinned_mt_tot', array.array('d', mt_tot_b))
        # if "mt_" in w.name or "mT" in w.name:
        #         w.histo = w.histo.Rebin(len(mt)-1, 'rebinned_mt', array.array('d', mt))
        if "met" in w.name:
            w.histo = w.histo.Rebin(len(met)-1, 'rebinned_met{0}'.format(w.name), array.array('d', met))
        # if "pt_2"  in w.name or "pt_1" in w.name:
        #     w.histo = w.histo.Rebin(len(pt)-1, 'rebinned_{0}'.format(w.name), array.array('d', pt))            
        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(2)
        # if "m_fastmtt" in w.name and "zoom" not in w.name: 
        #     w.histo = w.histo.Rebin(len(m_fastmtt)-1, 'rebinned_m_fastmtt', array.array('d', m_fastmtt))
        if "mt_tot_rebinned" in w.name:
            w.histo = w.histo.Rebin(len(nob_tight_mT)-1, 'rebinned_mt_tot', array.array('d', nob_tight_mT))
        if "PNN_500_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_500) -1, 'rebinned_mt_tot', array.array('d', PNN_500))   
            # h_PNN_500 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_500))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        if "PNN_1000_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_1000) -1, 'rebinned_mt_tot', array.array('d', PNN_1000))   
            # h_PNN_1000 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_1000))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        if "PNN_100_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_100) -1, 'rebinned_mt_tot', array.array('d', PNN_100))   
            # h_PNN_100 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_100))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        if "PNN_200_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_200) -1, 'rebinned_mt_tot', array.array('d', PNN_200))   
            # h_PNN_200 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_200))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        return w

            
    
    def scale_by_binwidth(w):
        for i in xrange(w.histo.GetNbinsX() + 1):
            w.histo.SetBinContent(i, w.histo.GetBinContent(i)/w.histo.GetBinWidth(i) )
            w.histo.SetBinError(i, w.histo.GetBinError(i)/w.histo.GetBinWidth(i))
        # w.histo.GetYaxis().SetTitle("")
        return w
    def setylimit(w):
        for i in xrange(w.histo.GetNbinsX() + 1):
            # w.histo.GetYaxis().SetRangeUser(0.1,10e5 )
            w.histo.SetMinimum(10)
        return w
            # print('+++++++++++++++++ ' , yields , '+++++++++++++++++ ')
    # wrps = (getyields(w) for w in wrps)
    if not use_all_signal:
        wrps = (rebin(w) for w in wrps)
    wrps = (blind_in_HmmWin(w) for w in wrps)
    # wrps = (setylimit(w) for w in wrps)
    # wrps = (scale_by_binwidth(w) for w in wrps)
    # for w in wrps:
    #     w.y_bounds = (1, 10e5)
    return wrps
