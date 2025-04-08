import sys
import yaml
import os
import ROOT as R
import argparse
import array
with open("/data/bond/zhiyuanl/Plotting//sample_database/datasets.yaml" , "r") as file:
    samples_list =  yaml.safe_load(file)
import re
R.gInterpreter.Declare('#include "/data/bond/zhiyuanl/Plotting/sample_database/NN_variables.h"')

R.EnableImplicitMT()

def extract_number(s):
    # Define the regex pattern
    pattern = r'M-(\d+)'
    # Search for all occurrences of the pattern
    matches = re.findall(pattern, s)
    # Convert matches to integers (if any) and return
    return [int(match) for match in matches]
def Add_new_column(df,new_column, overwrite=False):
    '''
    add a new column, new_column should be a dictionary with key name of new column with value of column value (best to use float)
    new_column = {column_name: value}
    ''' 
    modified = False
    col_names = df.GetColumnNames()
    print("calling adding new column")
    for c in new_column:    
        if c not in col_names:    
            df = df.Define(c,str(new_column[c])) 
            print(f"Adding new Column {c}")
            modified = True
        elif overwrite and c in col_names:
            df = df.Redefine(c,str(new_column[c])) 
            print(f"Redefining Column {c}")
            modified = True
        else:
            continue
        #     print(f"Column already exists {c}")
    return df, modified
def Redefine_type(df, pattern, old_type, new_type):
    # print(df.GetColumnType(pattern))
    modified = False
    for n in df.GetColumnNames():
        name = str(n)
        if pattern in name:
            if old_type == df.GetColumnType(name):
                modified = True
                print(f'redefining column {name} for old type {old_type} to new type {new_type}')
                
                if new_type == "int":
                    df = df.Redefine(name, f'int({name})')
                elif new_type == "float":
                    df = df.Redefine(name, f'float({name})')
                elif new_type == "double":
                    df = df.Redefine(name, f'double({name})')
                elif new_type == "bool":
                    df = df.Redefine(name, f'bool({name})')
                elif new_type == "UChar_t":
                    df = df.Redefine(name, f'static_cast<UChar_t>({name})')
                else:
                    print("supported type: int, float, bool")
                
            
        
    return df, modified
def redefine_column(df,column):
   
    col_names = df.GetColumnNames()
    for c in column:
        if c not in col_names:
            print(f"ERROR , {column} not found in dataframe")
            sys.exit(-1)
        df=df.Redefine(c, column[c] )
    return df

def find_tree_names(root_file):
    tree_names = []
    rfile = R.TFile.Open(root_file)
    for key in rfile.GetListOfKeys():
        if "map" in key.GetName():
            continue
        # print(key)
        obj = key.ReadObj()
        if isinstance(obj, R.TTree):
            tree_names.append(obj.GetName())
    
    print(tree_names)
    return tree_names


def keep_only_nominal(df):
    ori_col_names = df.GetColumnNames()
    col_names = [str(c) for c in ori_col_names if "__" not in str(c)]
    return col_names

def filter_df(df, channel, FF_cut =False):
    ## do some loose preselection to speed up processing speed
    ## we need to be careful not to cut away systematics variations
    ## the selection is combined with || 
    selection_dic = {}
    selection_dic["mt"] = {
               "pt_1":"> 25.0","pt_2":"> 30","extramuon_veto":"== 0","extraelec_veto":"== 0",
               "id_tau_vsJet_Medium_2":"> 0", "mt_1" : "> 0" }
    selection_dic["et"] = {
               "pt_1":"> 30","pt_2":"> 30","extramuon_veto":"== 0","extraelec_veto":"== 0",
               "id_tau_vsMu_VLoose_2":"> 0","id_tau_vsEle_Tight_2":"> 0","id_tau_vsJet_Medium_2":"> 0", "mt_1" : "> 0" }
    selection_dic["tt"] = {
               "pt_1":"> 40","pt_2":"> 40","extramuon_veto":"== 0","extraelec_veto":"== 0",
               "id_tau_vsJet_Medium_1":"> 0","id_tau_vsJet_Medium_2":"> 0", "mt_1" : "> 0", 
               "deltaR_ditaupair":"> 0.5"}
    selection_dic["em"] = {"extramuon_veto":"== 0","extraelec_veto":"== 0","pt_1":"> 15", "pt_2":"> 15", "mt_1" : "> 0",  }
    selection_dic["mm"] = {"pt_1":"> 25", "pt_2":"> 10","mt_1" : "> 0", "jpt_1" : "> -999", "nbtag": "==0", "HLT_IsoMu24": ">0" }
    if FF_cut:
        selection_dic[channel]["FF_weight"] = "!=0"
    for i in selection_dic[channel]:
        filter_condition = []
        for var in df.GetColumnNames():
            if str(var).startswith(i) and "_tmp" not in var :
                filter_condition.append(f"{str(var)} {selection_dic[channel][i]}")
        filter_condition_final = (" || ").join(filter_condition)
        print(filter_condition_final)
        # print(df.Count().GetValue())
        df = df.Filter(f"( {filter_condition_final} )")
        # print(df.Count().GetValue())
    return df

def filter_df_pnn(df, channel):
    selection_dic = {}
    selection_dic["mt"] = "((  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)&& pt_1> 25.0 &&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsMu_Tight_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  \
    id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 50) && mt_1 > 0 && Train_weight !=0 &&(std::isnan(pzetamissvis) == 0)  && met > 0"
    selection_dic["tt"] = '(( (trg_double_tau35_mediumiso_hps == 1 || trg_double_tau40_mediumiso_tightid == 1 || trg_double_tau40_tightiso == 1 || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1)&&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsJet_Medium_1 > 0 && dz_1 < 0.2 && pt_1 > 40 && eta_1 < 2.1 && eta_1 > -2.1 && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0  )&& (id_tau_vsJet_Medium_2 > 0  && dz_2 < 0.2 &&   pt_2 > 40 && eta_2 < 2.1 && eta_2 > -2.1 && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0         && deltaR_ditaupair > 0.5 ) )&& ((q_1 * q_2) < 0) ) && met > 0'
    selection_dic["et"] =  "met > 0 && mt_1 > 0&& mt_1 < 50 && jpt_1 > -999&&  ((q_1 * q_2) < 0) && (  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) && ((trg_single_tau180_2==1 ||  trg_single_ele32==1||trg_single_ele35==1)&&(pt_1 > 33 && iso_1 < 0.15 && abs(eta_1) < 2.1)&&extramuon_veto == 0  && extraelec_veto == 0 && (id_tau_vsMu_VLoose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 && pt_2 > 30 && abs(eta_2) < 2.3) )"
    
    Dzeta_cut = "(pzetamissvis > -35  && mt_1 > 0 && jpt_1 > -999 && met > 0)"
    #Dzeta_cut = "(mt_1 > 0)"
    lepton_veto = "  (extramuon_veto == 0  && extraelec_veto == 0) " 

    em_electron_selection = "(abs(dz_1) < 0.2 && abs(dxy_1) < 0.045  && deltaR_ditaupair > 0.3 && pt_1 > 15)" #少了 iso_e
    iso_e = "(iso_1 < 0.15)"
    antiiso_e = " ( (iso_1 > 0.15) && (iso_1<0.5) )"

    em_muon_selection = "(abs(dz_2) < 0.2 && abs(dxy_2) < 0.045 && pt_2 > 15)" #少了iso mu
    iso_mu = "(iso_2 < 0.2)"
    antiiso_mu = " (  (iso_2 > 0.2) && (iso_2< 0.5)  ) "

    opposite_sign = ' ((q_1 * q_2) < 0) '
    same_sign = ' ((q_1 * q_2) > 0) '
    no_b_cut = "nbtag == 0 "
    em_triggers_selections =  "( (trg_cross_mu23ele12 == 1 || trg_cross_mu8ele23 == 1 ) || (trg_single_ele30 == 1) ||(trg_single_ele32 == 1)|| (trg_single_ele35 == 1) || (trg_single_mu24 == 1)|| (trg_single_mu27 == 1) )"    #" ( (trg_cross_mu23ele12 == 1 && pt_1 > 15 && pt_2 >24)   ||    (trg_cross_mu8ele23 == 1 && pt_1 >24 &&  pt_2 > 15)  )  " 
    # buggy_signal_cut = "( abs(Train_weight) < 10  )"
    def combinecut(*args):
        return '(' + '&&'.join(args) + ')'
    em_SR = combinecut(em_triggers_selections, em_muon_selection, iso_e, em_electron_selection, iso_mu,lepton_veto, opposite_sign,Dzeta_cut, no_b_cut   )  #  , buggy_signal_cut
    selection_dic["em"] =  em_SR
    
    df = df.Filter(selection_dic[channel])
    return df
def post_proc(f, samples_list, keep_only_nom=False, era='2022postEE', channel='mt', cut=0, out_vars =[], pnn_format= False):
    luminosities = {
    "2022EE":8.077009684e3,
    "2022postEE":  26.671609707e3,
    "2023": 0.641474303e3 + 18.062659111e3, # B + C
    "2023BPix": 9.693130053e3, # D 
      }
    lumi = luminosities[args.era]
    weight_dict = {
        "tt": '(is_data && is_fake ==0)? float(1.0) : Xsec *  {0}* puweight * genWeight/genEventSumW *    btag_weight   *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 *  FF_weight * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 '.format(lumi), # * ggh_NNLO_weight
        "mt": '(is_data && is_fake ==0)? float(1.0) : Xsec   * {0} * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight *id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1 '.format(lumi), # * ggh_NNLO_weight
        "et": '(is_data && is_fake ==0)? float(1.0) : Xsec * {0}* puweight * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2  *  btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2  * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30 '.format(lumi), # * ggh_NNLO_weight
        "em": '(is_data && is_fake ==0)? float(1.0) : Xsec * {0} *  genWeight  / genEventSumW * id_wgt_ele_wpTight * id_wgt_mu_2 * btag_weight *  FF_weight * puweight * (trg_wgt_single_mu24 )'.format(lumi),
        "mm": '(is_data && is_fake ==0)? float(1.0) : Xsec * {0} * genWeight/genEventSumW * puweight *  id_wgt_mu_1*iso_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_2* trg_wgt_single_mu24'.format(lumi),
    }
    
    print(f"start processing   {f} ")
    

    # print(f'processing {n} process for file {f} ')
    if not ".root" in f or "roota.root" in f or "FF_input" in f or "tmp_" in f or "closure" in f or "FakeFactor" in f or "Fakes_" in f or "corrections" in f:
        print("wrong type of root file")
        sys.exit(0)
    trees = find_tree_names(f)
    tree_name = trees[0] if 'ntuple' not in trees else 'ntuple'
    print(tree_name)
    df_mc = R.RDataFrame(tree_name, f)
    ## apply or not preselection
    modified_initial = False
    if cut:
        before_cut = df_mc.Count().GetValue()
        if "FF_Combined" in f:
            df_mc = filter_df(df_mc, channel, FF_cut = True)    
        else:
            df_mc = filter_df(df_mc, channel)
        after_cut = df_mc.Count().GetValue()
        if before_cut != after_cut:
            modified_initial = True
    gensumw = 0
    col_names = df_mc.GetColumnNames()
    if 'genEventSumW'  not in col_names:    
        for n in samples_list:
            if n == f.strip(f"_{channel}.root"):
                print(f,n)
                gensumw = R.RDataFrame('conditions', f).Sum('genEventSumw').GetValue()
                if ("Run2022" in f) or( "Run2023" in f ):
                    gensumw ='1.0'
                df_mc = df_mc.Define('Xsec', f"float({samples_list[n]['xsec']})" )
                df_mc = df_mc.Define('genEventSumW', f'float({gensumw})')
                print(f"Adding new Column genEventSumW: {gensumw}")
      
        if gensumw ==0 :
            print(f"file {f} not found in sample_database yaml list")
            sys.exit()
    else:
        print(f'genEventSumW was added in file {f} already. ') 
    df_mc, _1 = Add_new_column(df_mc,  
    {'genWeight': '1.0f', 'Xsec' : '1.0f', 'is_fake' : 'false', "gen_match_1": 'int(-1)',"gen_match_2": 'int(-1)', "puweight": "double(1.0)", "btag_weight" : "float(1.0)", 
    "id_wgt_mu_1" : "1.0f", "iso_wgt_mu_1" : "float(1.0)", "id_wgt_mu_2" : "1.0f", "iso_wgt_mu_2" : "float(1.0)", 
    'id_wgt_ele_wpTight': 'float(1.0)', 'ZPtMassReweightWeight': 'double(1.0)',
    'id_wgt_tau_vsMu_Tight_2' : "float(1.0)","id_wgt_tau_vsEle_Tight_2" : 'float(1.0)', 'id_wgt_tau_vsMu_VLoose_2': 'float(1.0)', "id_wgt_tau_vsMu_Loose_2" : "float(1.0)", "id_wgt_tau_vsEle_VVLoose_2" : "float(1.0)", "id_wgt_tau_vsJet_Medium_2" : "float(1.0)",  'id_wgt_tau_vsJet_Medium_1': 'float(1.0)', 
    "trg_wgt_single_mu24ormu27" : "float(1.0)", 'trg_wgt_ditau_crosstau_2': 'float(1.0)','trg_wgt_ditau_crosstau_1': 'float(1.0)', 'trg_wgt_single_ele30' : 'float(1.0)', 'trg_wgt_single_mu24' :'float(1.0)',
    "FF_weight": "float(1.0)",
    'C_QCD': 'met/pt_2 * cos(metphi - phi_2 ) ',  'C_W': '(met + pt_1)/pt_2 * cos(metphi + phi_1- phi_2 )',
    'tau_gen_match_2' : 'bool(0)',
    'Lumi': str(lumi),  "ggh_NNLO_weight": "float(1.0)",})
    # if channel != "mm":
    #     df_mc, _1 = Add_new_column(df_mc,  {
    # "costhstar_1_LT": "calculate_costhstar(pt_1, eta_1, phi_1, mass_1,  pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
    #     "costhstar_2_LT": "calculate_costhstar(pt_2, eta_2, phi_2, mass_2,  pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
    #     "deltaR_LT": "calculate_deltaR(pt_1_LT, eta_1_LT, phi_1_LT, mass_1, pt_2_LT, eta_2_LT, phi_2_LT, mass_2)",
    #     "kT_LT": "calculate_kT(pt_1_LT, eta_1_LT, phi_1_LT, mass_1, pt_2_LT, eta_2_LT, phi_2_LT, mass_2)",  ## calculate anti-kt? # check delta R definition with CROWN?
    #     "antikT_LT": "calculate_antikT(pt_1_LT, eta_1_LT, phi_1_LT, mass_1, pt_2_LT, eta_2_LT, phi_2_LT, mass_2)",  ## calculate anti-kt? # check delta R definition with CROWN?

    #     "Z_NN_LT": "calculate_z_NN(pt_1_LT, eta_1_LT, phi_1_LT, mass_1, pt_2_LT, eta_2_LT, phi_2_LT, mass_2)",
        
    #     "pt1_to_ptH": "pt_1/pt_fastmtt",
    #     "pt2_to_ptH": "pt_2/pt_fastmtt",
    #     "pt_fastmtt_LT": "calculate_boost_pt(pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
    #     "eta_fastmtt_LT": "calculate_boost_eta(pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
    #     "phi_fastmtt_LT": "calculate_boost_phi(pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
    #     "phi_met_LT": "calculate_boost_phi(met, 0, metphi, met, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",

        
    #     'dtheta_12' : 'calculate_theta_12(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)',
    #     "m_vis_square": "calculate_m_vis_square(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2)",
        
        # 'dphi_H1_LT' : 'abs(TVector2::Phi_mpi_pi(phi_1_LT-phi_fastmtt))', ## don't transform H
        # 'dphi_H2_LT' : 'abs(TVector2::Phi_mpi_pi(phi_2_LT-phi_fastmtt))',
        # 'dphi_HMET' : 'abs(TVector2::Phi_mpi_pi(metphi-phi_fastmtt))',
        # 'dphi_MET_1' : 'abs(TVector2::Phi_mpi_pi(metphi-phi_1))',
        # 'dphi_MET_2' : 'abs(TVector2::Phi_mpi_pi(metphi-phi_2))',
        # 'dphi_HMET_LT' : 'abs(TVector2::Phi_mpi_pi(phi_met_LT-phi_fastmtt_LT))',
        # 'dphi_MET_1_LT' : 'abs(TVector2::Phi_mpi_pi(phi_met_LT-phi_1_LT))',
        # 'dphi_MET_2_LT' : 'abs(TVector2::Phi_mpi_pi(phi_met_LT-phi_2_LT))',
        # "pt1_to_mH" :  "pt_1/m_fastmtt",
        # "pt2_to_mH" :  "pt_2/m_fastmtt",
        
        # "pt_tt_to_mH" : "pt_tt/m_fastmtt",
        # "pt_fastmtt_to_mH" : "pt_fastmtt/m_fastmtt",
        # "pt_vis_to_mH" : "pt_vis/m_fastmtt",
        # "pt1_LT_to_pt2_LT" :  "pt_1_LT/pt_2_LT",
        # 'deta_12' : 'eta_1 - eta_2', 
        # 'deta_12_LT' : 'eta_1_LT - eta_2_LT',
        # 'dphi_12_LT' : 'abs(TVector2::Phi_mpi_pi(phi_1_LT-phi_2_LT))',

    # 'cos_dphi_H1' : 'cos(dphi_H1)',    ## don't allow < 0
    # 'cos_dphi_H2' : 'cos(dphi_H2)',
    # 'cos_dphi_H1_LT' : 'cos(dphi_H1_LT)',
    # 'cos_dphi_H2_LT' : 'cos(dphi_H2_LT)',
    # 'cos_dphi_HMET' : 'cos(dphi_HMET)',
    # 'cos_dphi_MET_1' : 'cos(dphi_MET_1)',
    # 'cos_dphi_MET_2' : 'cos(dphi_MET_2)',
    # 'cos_dphi_HMET_LT' : 'cos(dphi_HMET_LT)',
    # 'cos_dphi_MET_1_LT' : 'cos(dphi_MET_1_LT)',
    # 'cos_dphi_MET_2_LT' : 'cos(dphi_MET_2_LT)',
    # 'cos_dtheta_12' : 'calculate_costheta_12(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)',
    # 'dtheta_12' : 'calculate_theta_12(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)',
    # 'eta_vis' :'calculate_eta_tt(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2)',
    # 'phi_vis' :'calculate_phi_tt(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2)',
    # } )
    # df_mc, _1 = Add_new_column(df_mc,
    # {   
        

    # },
    # overwrite = True
    # )
    df_mc, _2 = Add_new_column(df_mc, 
                                {'Train_weight': weight_dict[channel],
                                # 'dphi_12' : 'phi_1 - phi_2',
                                }
                                , overwrite=False)
    df_mc,_2 = Redefine_type(df_mc,"ZPtMassReweightWeight", "Float_t","double"  )
    # df_mc = df_mc.Filter("jpt_1 > -99")
    # df_mc,_3 = Redefine_type(df_mc,"pzetamissvis_pf", "Double_t","float"  )
    # df_mc,_4 = Redefine_type(df_mc,"trg_wgt_single_ele30", "Float_t","double"  )
    # df_mc,_5 = Redefine_type(df_mc,"tau_gen_match_2", "Bool_t","UChar_t"  )
    # df_mc,_6 = Redefine_type(df_mc, "id_wgt_tau_vsJet_Medium_1",  "Float_t","double"  )
    # df_mc,_7 = Redefine_type(df_mc, "id_wgt_tau_vsJet_Medium_2",  "Float_t","double"  )
    # df_mc,_8 = Redefine_type(df_mc, "btag_weight",  "Float_t","double"  )
    # df_mc,_9 = Redefine_type(df_mc, "trg_wgt_ditau_crosstau_2",  "Float_t","double"  )
    # df_mc,_10 = Redefine_type(df_mc,"pzetamissvis", "Double_t","float"  )
    # df_mc,_11 = Redefine_type(df_mc,"iso_wgt_mu_1", "Float_t","double"  )
    # df_mc,_12 = Redefine_type(df_mc,"FF_weight", "Float_t","double"  )
    # if( channel!= "mm" ) and pnn_format:
        # df_mc, _12 = Add_new_column(df_mc, {
            # 'dphi_12' : 'abs(TVector2::Phi_mpi_pi(phi_1-phi_2))',
            # "costheta_1_LT": "calculate_costheta(pt_1, eta_1, phi_1, mass_1,  pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "costheta_2_LT": "calculate_costheta(pt_2, eta_2, phi_2, mass_2,  pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "pt_1_LT": "calculate_boost_pt(pt_1, eta_1, phi_1, mass_1, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "pt_2_LT": "calculate_boost_pt(pt_2, eta_2, phi_2, mass_2, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "eta_1_LT": "calculate_boost_eta(pt_1, eta_1, phi_1, mass_1, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "eta_2_LT": "calculate_boost_eta(pt_2, eta_2, phi_2, mass_2, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "phi_1_LT": "calculate_boost_phi(pt_1, eta_1, phi_1, mass_1, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "phi_2_LT": "calculate_boost_phi(pt_2, eta_2, phi_2, mass_2, pt_fastmtt, eta_fastmtt, phi_fastmtt, m_fastmtt)",
            # "kT": "calculate_kT(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2)",  
            # "antikT": "calculate_antikT(pt_1, eta_1, phi_1, mass_1, pt_2, eta_2, phi_2, mass_2)",
            # "m_vis_square": "calculate_m_vis_square(pt_1_LT, eta_1_LT, phi_1_LT, mass_1, pt_2_LT, eta_2_LT, phi_2_LT, mass_2)",
            # "pt1_LT_to_ptH" :  "pt_1_LT/pt_fastmtt",
            # "pt2_LT_to_ptH" :  "pt_2_LT/pt_fastmtt",
            # 'dphi_H1' : 'abs(TVector2::Phi_mpi_pi(phi_1-phi_fastmtt))',
            # 'dphi_H2' : 'abs(TVector2::Phi_mpi_pi(phi_2-phi_fastmtt))',
            # "pt1_LT_to_mH" :  "pt_1_LT/m_fastmtt",
            # "pt2_LT_to_mH" :  "pt_2_LT/m_fastmtt",
            # }, overwrite=False)
    


    # df_mc = df_mc.Redefine("njets", "((jpt_1 < 50 && abs(jeta_1) > 2.5 &&abs(jeta_1) < 3 ) || (jpt_2 < 50 && abs(jeta_2) > 2.5 &&abs(jeta_2) < 3 )) ? 0 : njets "  )
    # df_mc,_12 = Redefine_type(df_mc,"FF_weight", "Double_t","float"  )
    # modified = _1 or _2 or _3 or _4 or _5 or _6 or _7 or _8 or _9 or _10 or _11 or _12
    modified = _1 or _2 or modified_initial
    # modified=True
    if keep_only_nom:
        output_columns = keep_only_nominal(df_mc)
    else:
        output_columns = out_vars if out_vars else df_mc.GetColumnNames()

    
    output_columns = [str(c) for c in output_columns if "fCoordinates" not in str(c)]
    output_columns = [str(c) for c in output_columns if "PNN" not in str(c)]
    # PNN_vars = [ "Train_weight","event", "is_fake", "is_dyjets", "is_ttbar", "is_diboson", "is_data", "is_wjets",
    #     "dphi_12", "deta_12", "Xsec","beta_1","beta_2","bphi_1","bphi_2","bpt_1","bpt_2","deltaR_ditaupair",
    # "dxy_1","dxy_2","dz_1","dz_2","eta_1","eta_2","eta_fastmtt","mTdileptonMET","m_fastmtt","m_vis","mass_1","mass_2",
    # "mass_tt","met","metSumEt","metphi","mjj","mt_1","mt_2","mt_tot","nbtag","njets","nprebjets","phi_1","phi_2","phi_fastmtt",
    # "pt_1","pt_2","pt_dijet","pt_fastmtt","pt_tt","pt_ttjj","pt_vis","pzetamissvis","q_1","q_2"]
    pnn_remove = ["genWeight_tmp","FF_weight_tmp", "FF_weight_tmp1", "FF_weight_tmp2" , 
        "gen_pdgid_1", "gen_pdgid_2","gen_taujet_pt_2","genbosonmass", "genbosonpt", "PNN", "__", "gen_higgs_p4", "fCoordinates"]
    for i in output_columns:
        if "HTXS" in i:
            pnn_remove.append(i)
        if "ggH" in i:
            pnn_remove.append(i)
        if "higgs" in i:
            pnn_remove.append(i)    
        if "top" in i:
            pnn_remove.append(i)    
    if pnn_format:
        n = 0
        while n < 100:
            n += 1
            for var in pnn_remove:
                if var in output_columns:
                    output_columns.remove(var)
                    modified = True
    print(output_columns)
    if modified:
        if pnn_format and '2HDM' in f:
            M = extract_number(f)
            print("saving to tree ", f"Xtohh{M[0]}")
            df_mc = filter_df_pnn(df_mc, channel)
            df_mc.Snapshot(f"Xtohh{M[0]}",   f'{f}a.root',output_columns ) # update the file finished    # PNN_vars
        
        elif pnn_format:
            df_mc = filter_df_pnn(df_mc, channel)
            df_mc.Snapshot(f"ntuple",   f'{f}a.root',output_columns) # update the file finished  #PNN_vars
        else:   
            df_mc.Snapshot("ntuple",   f'{f}a.root', output_columns) # update the file finished

        print(f"finished processing {f}")
        os.system(f"mv {f}a.root {f}")
    else:
        print(f"nothing changed for {f}")
        sys.exit(0)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='input file for post-process')
    parser.add_argument('--era', type = str, default='2022postEE')
    parser.add_argument('--channel', type = str, default='mt')
    parser.add_argument('--keep_only_nom', type = int, default=0)
    parser.add_argument('--cut', type = int, default=0)
    parser.add_argument('--out_vars', nargs='+', type = str)
    parser.add_argument('--pnn_format', type= int, default =0)
    args = parser.parse_args()
    



    
    post_proc(args.input_file, samples_list, args.keep_only_nom, args.era, args.channel, args.cut, args.out_vars, args.pnn_format )