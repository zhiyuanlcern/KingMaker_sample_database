import sys
import uproot
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import awkward as ak
import ROOT as R
import copy
from multiprocessing import Pool, cpu_count
import gc
import re
import time
import psutil
import array
R.TH1.SetDefaultSumw2(True)
btag_list=["nob1", "nob2", "nob3", "nob4", "nob5", "btag"] #"nob8",
btag_list_short=["nob", "btag"]

bin_dict ={}
# bin_dict["mt_tot"]={
#     "nob":[0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,5000.0],
#     "btag":[0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,250.0,300.0,350.0,400.0,500.0,600.0,700.0,5000.0] # remove two bin
# }
# common_bins = [0.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 
#               160.0, 170.0, 180.0, 190.0, 200.0, 220.0, 240.0, 260.0, 300.0]
# bin_dict["m_fastmtt"] = {
#     key: common_bins for key in ["nob1", "nob2", "nob3", "nob4", "nob5", "nob"]
# }
# bin_dict["m_fastmtt"]["btag"] = [0.0, 60.0, 80.0, 90.0, 100.0, 110.0, 120.0, 140.0, 160.0, 180.0, 200.0, 240.0, 300.]

bin_dict['pt_1'] = {}
bin_dict['pt_1']['nob']=bin_dict['pt_1']['btag'] = np.linspace(20,170,31).tolist() 
bin_dict['pt_2'] = {}
bin_dict['pt_2']['nob']=bin_dict['pt_2']['btag'] = np.linspace(20,170,31).tolist() 
bin_dict['pt_tt'] = {}
bin_dict['pt_tt']['nob']=bin_dict['pt_tt']['btag'] = np.linspace(0,200,41).tolist() 
bin_dict['mt_tot'] = {}
bin_dict['mt_tot']['nob']=bin_dict['mt_tot']['btag'] = np.linspace(0,300,31).tolist() 
bin_dict['m_vis'] = {}
bin_dict['m_vis']['nob']=bin_dict['m_vis']['btag'] = np.linspace(0,200,41).tolist() 
bin_dict['mt_1'] = {}
bin_dict['mt_1']['nob']=bin_dict['mt_1']['btag'] = np.linspace(0,200,51).tolist() 
bin_dict['mt_2'] = {}
bin_dict['mt_2']['nob']=bin_dict['mt_2']['btag'] = np.linspace(0,200,51).tolist() 
bin_dict['met'] = {}
bin_dict['met']['nob']=bin_dict['met']['btag'] = np.linspace(0,150,31).tolist() 
bin_dict['m_fastmtt'] = {}
bin_dict['m_fastmtt']['nob']=bin_dict['m_fastmtt']['btag'] =np.linspace(30,300,28).tolist()
bin_dict['deltaR_ditaupair'] = {}
bin_dict['deltaR_ditaupair']['nob']=bin_dict['deltaR_ditaupair']['btag'] =np.linspace(0,5,26).tolist()
bin_dict['nbtag'] = {}
bin_dict['nbtag']['nob']=bin_dict['nbtag']['btag'] =np.linspace(0,5,6).tolist()
bin_dict['njets'] = {}
bin_dict['njets']['nob']=bin_dict['njets']['btag'] =np.linspace(0,5,6).tolist()
bin_dict['deta_12'] = {}
bin_dict['deta_12']['nob']=bin_dict['deta_12']['btag'] =np.linspace(-3.5,3.5,31).tolist()
bin_dict['dphi_12'] = {}
bin_dict['dphi_12']['nob']=bin_dict['dphi_12']['btag'] =np.linspace(0,3.2,31).tolist()
bin_dict['metphi'] = {}
bin_dict['metphi']['nob']=bin_dict['metphi']['btag'] =np.linspace(-4,4,41).tolist()
bin_dict['pt_fastmtt'] = {}
bin_dict['pt_fastmtt']['nob']=bin_dict['pt_fastmtt']['btag'] =np.linspace(0,200,41).tolist()
bin_dict['eta_fastmtt'] = {}
bin_dict['eta_fastmtt']['nob']=bin_dict['eta_fastmtt']['btag'] =np.linspace(-2.3,2.3,31).tolist()
bin_dict['kT'] = {}
bin_dict['kT']['nob']=bin_dict['kT']['btag'] =np.linspace(0,400,41).tolist()
bin_dict['antikT'] = {}
bin_dict['antikT']['nob']=bin_dict['antikT']['btag'] =np.linspace(0,0.2,41).tolist()
bin_dict['pt1_LT_to_ptH'] = {}
bin_dict['pt1_LT_to_ptH']['nob']=bin_dict['pt1_LT_to_ptH']['btag'] =np.linspace(0,3,41).tolist()
bin_dict['pt2_LT_to_ptH'] = {}
bin_dict['pt2_LT_to_ptH']['nob']=bin_dict['pt2_LT_to_ptH']['btag'] =np.linspace(0,3,41).tolist()
bin_dict['dphi_H1'] = {}
bin_dict['dphi_H1']['nob']=bin_dict['dphi_H1']['btag'] =np.linspace(0,3.2,31).tolist()
bin_dict['dphi_H2'] = {}
bin_dict['dphi_H2']['nob']=bin_dict['dphi_H2']['btag'] =np.linspace(0,3.2,31).tolist()
bin_dict['iso_1'] = {}
bin_dict['iso_1']['nob']=bin_dict['iso_1']['btag'] =np.linspace(0,0.5,26).tolist()
def check_finished(folder, filename, var, era, signal_type):
    f_strip = filename.replace(".root", "")
    if "PNN" not in  var:
        btag_list_tmp = btag_list_short   ## for mt_tot, don't split in pt_tt
    else:
        btag_list_tmp =  btag_list
    if "2HDM" in filename or "BBH" in filename:
        match = re.search(r'M-(\d+)_', filename)
        if match:
            masses_check = [int(match.group(1))]
            m = masses_check[0]
            if f"PNN_{m}" not in var and (var != "mt_tot" and var != "m_fastmtt" ):
                # print(f"no need to run for PNN score {folder}/{f_strip}_era_{var + suffixs[1]}_{btag}")
                return True
    for btag in btag_list_tmp:
        if "tmp" in f_strip:
            continue
        if not os.path.exists(f"{folder}/{f_strip}_{era}_{btag}_{var}{signal_type}.root"):
            print("file not finished: ", f"{folder}/{f_strip}_{era}_{btag}_{var}{signal_type}.root")
            return False
        else:
            print("file finished: ", f"{folder}/{f_strip}_{era}_{btag}_{var}.root")
            continue
    return True

def read_shift_file(file_path):
    """Reads shift values from a text file."""
    with open(file_path, 'r') as file:
        shifts = [line.strip() for line in file if line.strip()]  # Strip whitespace and skip empty lines
    return shifts

def get_memory_usage():
    # Return the percentage of available memory
    memory_info = psutil.virtual_memory()
    available_memory_percentage = memory_info.available / memory_info.total * 100
    return available_memory_percentage


def get_variable_df(df, var_base, var_suffix=""):
    var_name = f"{var_base}{var_suffix}"
    if var_name in df.GetColumnNames():
        return str(var_name)
    else:
        return str(var_base)
def get_bins_from_file(era, channel, var, btag, signal_type):
                    BINNING_DIR = "/data/bond/zhiyuanl/Plotting/fitting_template_Version11/bin_edges/"
                    import ast
                    filename = f"{era}_{channel}_Version11_nominal_ggH_model_output_nosyst_{var}_{signal_type}{btag}_bin_edges.txt"
                    print("filename:",filename)
                    filepath = os.path.join(BINNING_DIR, filename)
                    
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read().strip()
                            
                            # 处理文件末尾可能多余的逗号
                            if content.endswith(','):
                                content = content[:-1]
                            
                            # 安全地解析列表
                            bins = ast.literal_eval(content)
                            
                            # 确保返回的是列表且至少有两个元素
                            if not isinstance(bins, list) or len(bins) < 2:
                                raise ValueError(f"Invalid bin edges format in {filepath}")
                                
                            return bins
                            
                    except FileNotFoundError:
                        raise FileNotFoundError(f"Binning file not found: {filepath}")
                    except (SyntaxError, ValueError) as e:
                        raise ValueError(f"Failed to parse bin edges from {filepath}: {str(e)}")
def process_file(args):
    folder_path, filename, era, variables, suffixs_ori, channel,  lumi, signal_type, do_rebin, tag = args
    f_strip = filename.replace(".root", "")
    output_folder = f"{folder_path}_{tag}"
    if not filename.endswith(".root"):
        print(filename, "not endwith root")
        return
    if variables == []:
        print(f"finished all variables for file {filename}")
        return
    file_path = os.path.join(folder_path, filename)
    rdf_main = R.RDataFrame("ntuple", file_path)
    suffixs = []    
    for suffix in suffixs_ori:
        no_syst = True

        for v in rdf_main.GetColumnNames():
            if suffix in v:
                no_syst = False
        if not no_syst:
            suffixs.append(suffix)
    
    if ("Run2022" in filename) or ("Sep202" in filename):
            suffixs =[""]
    
    data = {}
    weights = {}
    if "" not in suffixs:
        suffixs.append("")
    selection_dic_suffixs = {}
    weight_dic_suffixs = {}
    for suffix in suffixs:   
        extramuon_veto = get_variable_df(rdf_main, "extramuon_veto",suffix)
        extraelec_veto = get_variable_df(rdf_main, "extraelec_veto",suffix)
        eta_1 = get_variable_df(rdf_main, "eta_1",suffix)
        dz_1 = get_variable_df(rdf_main, "dz_1",suffix)
        dxy_1 = get_variable_df(rdf_main, "dxy_1",suffix)
        iso_1 = get_variable_df(rdf_main, "iso_1",suffix)
        phi_2 = get_variable_df(rdf_main,"phi_2",suffix)
        deltaR_ditaupair = get_variable_df(rdf_main, "deltaR_ditaupair",suffix)
        pt_1 = get_variable_df(rdf_main, "pt_1",suffix)
        eta_2 = get_variable_df(rdf_main, "eta_2",suffix)
        dz_2 = get_variable_df(rdf_main, "dz_2",suffix)
        dxy_2 = get_variable_df(rdf_main, "dxy_2",suffix)
        iso_2 = get_variable_df(rdf_main, "iso_2",suffix)
        pt_2 = get_variable_df(rdf_main, "pt_2",suffix)
        nbtag = get_variable_df(rdf_main, "nbtag",suffix)
        q_1 = get_variable_df(rdf_main, "q_1",suffix)
        q_2 = get_variable_df(rdf_main, "q_2",suffix)
        mt_1 = get_variable_df(rdf_main, "mt_1", suffix)
        gen_match_2 = get_variable_df(rdf_main, "gen_match_2",suffix)
        ZPtMassReweightWeight=get_variable_df(rdf_main, "ZPtMassReweightWeight", suffix)
        is_wjets =  "is_wjets"
        is_ttbar = "is_ttbar"
        btag_weight = get_variable_df(rdf_main, "btag_weight",suffix)
        pt_tt = get_variable_df(rdf_main, "pt_tt", suffix)
        pzetamissvis= get_variable_df(rdf_main, "pzetamissvis", suffix)
        # btag_norm = rdf_main.Mean(f"{btag_weight}").GetValue()
        if channel == 'em':
            id_wgt_ele_wpTight = get_variable_df(rdf_main, "id_wgt_ele_wpTight",suffix)
            id_wgt_mu_2 = get_variable_df(rdf_main, "id_wgt_mu_2",suffix)
            trg_cross_mu23ele12 = get_variable_df(rdf_main, "trg_cross_mu23ele12",suffix)
            trg_cross_mu8ele23 = get_variable_df(rdf_main, "trg_cross_mu8ele23",suffix)
            trg_single_ele30 = get_variable_df(rdf_main, "trg_single_ele30",suffix)
            trg_single_mu24 = get_variable_df(rdf_main, "trg_single_mu24",suffix)
            trg_wgt_single_mu24 = get_variable_df(rdf_main, "trg_wgt_single_mu24",suffix)
            trg_wgt_single_ele30 = get_variable_df(rdf_main, "trg_wgt_single_ele30",suffix)
            FF_weight = get_variable_df(rdf_main, "FF_weight",suffix)
            iso_wgt_mu_2 = get_variable_df(rdf_main, "iso_wgt_mu_2", suffix)
        if channel == "mt":
            trg_cross_mu20tau27_hps = get_variable_df(rdf_main, "trg_cross_mu20tau27_hps",suffix)
            trg_single_tau180_2 = get_variable_df(rdf_main, "trg_single_tau180_2",suffix)
            trg_single_mu24 = get_variable_df(rdf_main, "trg_single_mu24",suffix)
            id_tau_vsMu_Tight_2 = get_variable_df(rdf_main, "id_tau_vsMu_Tight_2",suffix)
            id_tau_vsJet_Medium_2 = get_variable_df(rdf_main, "id_tau_vsJet_Medium_2",suffix)
            id_tau_vsEle_VVLoose_2 = get_variable_df(rdf_main, "id_tau_vsEle_VVLoose_2",suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable_df(rdf_main, "id_wgt_tau_vsJet_Medium_2",suffix)
            FF_weight = get_variable_df(rdf_main, "FF_weight",suffix)
            iso_wgt_mu_1 = get_variable_df(rdf_main, "iso_wgt_mu_1",suffix)
            trg_wgt_ditau_crosstau_2 = get_variable_df(rdf_main, "trg_wgt_ditau_crosstau_2",suffix)
            id_wgt_tau_vsMu_Tight_2 = get_variable_df(rdf_main, "id_wgt_tau_vsMu_Tight_2",suffix)
            id_wgt_mu_1 = get_variable_df(rdf_main, "id_wgt_mu_1",suffix)
            # print(4)
        if channel == 'et': 
            trg_cross_ele24tau30_hps = get_variable_df(rdf_main, "trg_cross_ele24tau30_hps", suffix)
            trg_single_ele30 = get_variable_df(rdf_main, "trg_single_ele30", suffix)    
            trg_single_tau180_2 = get_variable_df(rdf_main, "trg_single_tau180_2", suffix)
            id_tau_vsMu_VLoose_2 = get_variable_df(rdf_main, "id_tau_vsMu_VLoose_2", suffix)
            id_tau_vsEle_Tight_2 = get_variable_df(rdf_main, "id_tau_vsEle_Tight_2", suffix)
            id_tau_vsJet_Medium_2 = get_variable_df(rdf_main, "id_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable_df(rdf_main, "id_wgt_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsEle_Tight_2 = get_variable_df(rdf_main, "id_wgt_tau_vsEle_Tight_2", suffix)
            FF_weight = get_variable_df(rdf_main, "FF_weight",suffix)
            id_wgt_ele_wpTight = get_variable_df(rdf_main, "id_wgt_ele_wpTight", suffix)
            trg_wgt_single_ele30 = get_variable_df(rdf_main, "trg_wgt_single_ele30", suffix)
            trg_wgt_ditau_crosstau_2 = get_variable_df(rdf_main, "trg_wgt_ditau_crosstau_2", suffix)
        if channel == 'tt':
            trg_double_tau30_plusPFjet60 = get_variable_df(rdf_main, "trg_double_tau30_plusPFjet60", suffix)
            trg_double_tau30_plusPFjet75 = get_variable_df(rdf_main, "trg_double_tau30_plusPFjet75", suffix)
            trg_double_tau35_mediumiso_hps = get_variable_df(rdf_main, "trg_double_tau35_mediumiso_hps", suffix)
            trg_single_tau180_1 = get_variable_df(rdf_main, "trg_single_tau180_1", suffix)
            trg_single_tau180_2 = get_variable_df(rdf_main, "trg_single_tau180_2", suffix)
            id_tau_vsJet_Medium_1 = get_variable_df(rdf_main, "id_tau_vsJet_Medium_1", suffix)
            id_tau_vsEle_VVLoose_1 = get_variable_df(rdf_main, "id_tau_vsEle_VVLoose_1", suffix)
            id_tau_vsMu_VLoose_1 = get_variable_df(rdf_main, "id_tau_vsMu_VLoose_1", suffix)
            id_tau_vsJet_Medium_2 = get_variable_df(rdf_main, "id_tau_vsJet_Medium_2", suffix)
            id_tau_vsEle_VVLoose_2 = get_variable_df(rdf_main, "id_tau_vsEle_VVLoose_2", suffix)
            id_tau_vsMu_VLoose_2 = get_variable_df(rdf_main, "id_tau_vsMu_VLoose_2", suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable_df(rdf_main, "id_wgt_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsJet_Medium_1 = get_variable_df(rdf_main, "id_wgt_tau_vsJet_Medium_1", suffix)
            FF_weight = get_variable_df(rdf_main, "FF_weight", suffix)
            trg_wgt_ditau_crosstau_1  = get_variable_df(rdf_main, "trg_wgt_ditau_crosstau_1", suffix)
            trg_wgt_ditau_crosstau_2 = get_variable_df(rdf_main, "trg_wgt_ditau_crosstau_2", suffix)
        print("finish getting variables. ")
        if not mt_1:
            print("fatal!! cannot retrieve variables for file ", filename)
            sys.exit(-1)
        selection_dic = {} 
        if channel == "mt":
            # 
            selection_dic['mt'] = f"(({trg_cross_mu20tau27_hps}==1 && {pt_1} > 24 && {pt_2} > 32)||{trg_single_tau180_2}==1  ||({trg_single_mu24}==1 && {pt_1} > 25)) &&  \
                ( ({extramuon_veto}==0)  &&  ({extraelec_veto}==0) && \
                ({iso_1}<0.15) && abs({eta_1} ) < 2.1 && abs({eta_2} ) < 2.3 &&  \
                ({id_tau_vsMu_Tight_2}>0) && ({id_tau_vsJet_Medium_2}>0) && ({id_tau_vsEle_VVLoose_2}>0 ) && \
                (( ({gen_match_2} != 6) && ({is_wjets}>0) ) || ({is_wjets}<1)  ) && (( ({gen_match_2} != 6) && ({is_ttbar}>0) ) || ({is_ttbar}<1)  ) &&   (({q_1} * {q_2})<0)   && ({mt_1}>0)  && {mt_1} <50 ) && ({FF_weight} !=0)"
            selection_dic["nob_mt"] = f"{selection_dic['mt']} && ({nbtag}==0) " 
            selection_dic["nob1_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 0 && {pt_tt} < 50) "
            selection_dic["nob2_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 50 && {pt_tt} < 100)  "
            selection_dic["nob3_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 100 && {pt_tt} < 200) "
            selection_dic["nob4_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 200) "
            selection_dic["nob5_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 100) "
            selection_dic["btag_mt"] = f"{selection_dic['mt']} && ({nbtag}>=1)"
            selection_dic["nob_mt"] = f"{selection_dic["nob_mt"]} "
            # print(5)
        elif channel == "et":
            # remember to add this back!! ({iso_1}<0.15) &&  
            selection_dic['et'] = f"((  ({trg_single_ele30}==1  && {pt_1} > 31 )||({trg_single_tau180_2}==1) || ({trg_cross_ele24tau30_hps} == 1 && {pt_1} > 25 && {pt_2} > 35)    )&& \
                ({extramuon_veto}==0)  && ({extraelec_veto}==0) && \
                abs({eta_1} ) < 2.1 && abs({eta_2} ) < 2.3 && \
                ({id_tau_vsMu_VLoose_2}>0)  && ({id_tau_vsEle_Tight_2}>0) && ({id_tau_vsJet_Medium_2}>0 ) && \
                 (( ({gen_match_2} != 6) && ({is_wjets}>0) ) || ({is_wjets}<1)  ) && (( ({gen_match_2} != 6) && ({is_ttbar}>0) ) || ({is_ttbar}<1)  ) &&  ({q_1} * {q_2})<0)  && ({mt_1}>0) && {mt_1} < 50  && ({FF_weight} !=0)"  # 
            selection_dic["nob_et"] = f"{selection_dic['et']} && ({nbtag}==0) " 
            selection_dic["nob1_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 0 && {pt_tt} < 50)  " 
            selection_dic["nob2_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 50 && {pt_tt} < 100)  " 
            selection_dic["nob3_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 100 && {pt_tt} < 200)  " 
            selection_dic["nob4_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 200) " 
            selection_dic["nob5_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 100) " 
            selection_dic["btag_et"] = f"{selection_dic['et']} && ({nbtag}>=1)"
            selection_dic["nob_et"] = f"{selection_dic["nob_et"]} " 

        elif channel == 'tt':
            #
            selection_dic['tt'] = f"(({trg_double_tau35_mediumiso_hps}==1&&{pt_1}>40&&{pt_2}>40)||({trg_double_tau30_plusPFjet60}==1&&{pt_1}>35&&{pt_2}>35)||({trg_double_tau30_plusPFjet75}==1&&{pt_1}>35&&{pt_2}>35)||{trg_single_tau180_1}==1||{trg_single_tau180_2}==1)&& \
                ({extramuon_veto}==0) && ({extraelec_veto}==0) && \
                ({dz_1}<0.2) && ({dz_2}<0.2) && ({eta_1}<2.1) && ({eta_1}>-2.1) && ({eta_2}<2.1) && ({eta_2}>-2.1) && \
                (({id_tau_vsJet_Medium_1}>0) && ({id_tau_vsEle_VVLoose_1}>0) && ({id_tau_vsMu_VLoose_1}>0))&& \
                (({id_tau_vsJet_Medium_2}>0) && ({id_tau_vsEle_VVLoose_2}>0) && ({id_tau_vsMu_VLoose_2}>0))&& \
                (( ({gen_match_2} != 6) && ({is_wjets}>0) ) || ({is_wjets}<1)  ) && (( ({gen_match_2} != 6) && ({is_ttbar}>0) ) || ({is_ttbar}<1)  )&& \
                ({deltaR_ditaupair}>0.5) && (({q_1} * {q_2})<0) && ({mt_1}>0) && ({FF_weight} !=0)"
            selection_dic["btag_tt"] = f"{selection_dic['tt']} && ({nbtag}>=1) "
            selection_dic["nob_tt"] = f"{selection_dic['tt']} && ({nbtag}==0)"
            selection_dic["nob1_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 0 && {pt_tt} < 50) " 
            selection_dic["nob2_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 50 && {pt_tt} < 100) " 
            selection_dic["nob3_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 100 && {pt_tt} < 200) " 
            selection_dic["nob4_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 200) " 
            selection_dic["nob5_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 100) " 

        elif channel == 'em':
            ## remember to add this back!! ({iso_1}<0.15) &&
            selection_dic['em'] = f"(({extramuon_veto}==0) && ({extraelec_veto}==0) && ({mt_1} >0) && \
                        (({trg_cross_mu23ele12}==1) || ({trg_cross_mu8ele23}==1) || ({trg_single_ele30}==1) || \
                        ({trg_single_mu24}==1) ) &&   ({pzetamissvis} >= -35) && \
                        (({eta_1}>-2.4) && ({eta_1}<2.4) && ({dz_1}<0.2) && ({dxy_1}<0.045) &&  \
                        ({deltaR_ditaupair}>0.3) && ({pt_1}>15)) && \
                        (({eta_2}>-2.4) && ({eta_2}<2.4) && ({dz_2}<0.2) && ({dxy_2}<0.045) && ({iso_2}<0.2) && ({pt_2}>15)) && (({q_1} * {q_2})<0) )  && ({mt_1}>0) && ({FF_weight} !=0)"

            if ("M-100_2HDM" in filename) or ("M-105_2HDM" in filename) or ("M-95_2HDM" in filename) or ("M-90_2HDM" in filename) or ("M-110_2HDM" in filename):
                selection_dic['em'] =  f"{selection_dic['em']} && (abs(Train_weight) < 10)"
            selection_dic["nob_em"] = f"{selection_dic['em']} && ({nbtag}==0)"
            selection_dic["btag_em"] = f"{selection_dic['em']} && ({nbtag}>=1)"
            selection_dic["nob1_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 0 && {pt_tt} < 50) " 
            selection_dic["nob2_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 50 && {pt_tt} < 100) " 
            selection_dic["nob3_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 100 && {pt_tt} < 200) " 
            selection_dic["nob4_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 200) " 
            selection_dic["nob5_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 100) " 

        else:
            print("wrong channel provided!! ")
        # print("selection_dic", selection_dic )
        selection_dic_suffixs[suffix] = selection_dic
        ## define weight
        train_weight_dic = {}
        # DY_em_weight_dict = {"2022EE": 0.82218013,"2022postEE":0.78275661,"2023":0.90302339 , "2023BPix":0.89675196,}
        DY_em_weight_dict = {"2022EE": 0.82218013,"2022postEE":0.88,"2023":0.90302339 , "2023BPix":0.89675196,}
        DY_em_weight=DY_em_weight_dict[era]


                
        if channel =='em' and "DY" in filename:
                        train_weight_dic['em'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} * puweight * genWeight / genEventSumW * {btag_weight }  * {FF_weight} * {id_wgt_ele_wpTight} * {id_wgt_mu_2} * (( {trg_single_mu24} > 0? {trg_wgt_single_mu24} : ({trg_single_ele30} > 0? {trg_wgt_single_ele30} : 1   ) )) * {iso_wgt_mu_2} * {DY_em_weight}" 
            # train_weight_dic['em'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} * puweight * genWeight / genEventSumW * {btag_weight }  * {trg_wgt_single_ele30 } *{id_wgt_ele_wpTight} * {id_wgt_mu_2} *  {trg_wgt_single_mu24 } * {DY_em_weight} "
        elif channel == "em":
            train_weight_dic['em'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} * puweight * genWeight / genEventSumW * {btag_weight }  * {FF_weight} * {id_wgt_ele_wpTight} * {id_wgt_mu_2} * (( {trg_single_mu24} > 0? {trg_wgt_single_mu24} : ({trg_single_ele30} > 0? {trg_wgt_single_ele30} : 1   ) )) * {iso_wgt_mu_2} " 
        elif channel =='tt':
            train_weight_dic['tt'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} * puweight * genWeight/genEventSumW *  {btag_weight }   * {FF_weight} * {trg_wgt_ditau_crosstau_1} *{trg_wgt_ditau_crosstau_2 }"  # * {id_wgt_tau_vsJet_Medium_2} * {id_wgt_tau_vsJet_Medium_1}
        elif channel == "mt":
            train_weight_dic['mt'] = f"Xsec *  {lumi}  * {ZPtMassReweightWeight} * puweight * genWeight/genEventSumW * {btag_weight }   *  {FF_weight}  *{trg_wgt_ditau_crosstau_2} *  {id_wgt_tau_vsMu_Tight_2} * {id_wgt_mu_1 } * {iso_wgt_mu_1}" # *{id_wgt_tau_vsJet_Medium_2} 
        elif channel == "et":
            train_weight_dic['et'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} *  puweight * genWeight/genEventSumW * {btag_weight } * {id_wgt_tau_vsEle_Tight_2 } *   {FF_weight}  * {id_wgt_ele_wpTight} * {trg_wgt_ditau_crosstau_2 } * {trg_wgt_single_ele30 }" #* {id_wgt_tau_vsJet_Medium_2 }
        train_weight = train_weight_dic[channel]
        weight_dic_suffixs[suffix] = train_weight
        # rdf = None
        
        ## define channel, region selections
        
    for var in variables:
        if "PNN" not in var:
            btag_list_tmp = btag_list_short  ## for mt_tot, don't split in pt_tt
        # elif  var == "m_fastmtt":
        #     btag_list_tmp = ["nob1","nob2","nob3","nob4", "nob5", "btag"]  ## for mt_tot, don't split in pt_tt
        else:
            btag_list_tmp =  btag_list

        # rdf = R.RDataFrame("ntuple", file_path) 
        for btag in btag_list_tmp:
            print("checking file path")
            print(file_path)
            selection = selection_dic[f'{btag}_{channel}']
            hist_data = {}
            
            # mt_tot_bins_dic["nobloose"] = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,5000.0]
            # Create bins for each range

            if signal_type and do_rebin:
                if "PNN" in var:
                    bins = get_bins_from_file(era, channel, var, btag, signal_type) #if var != "mt_tot" else mt_tot_bins
                    print(f"the {btag} region binning is:",bins)
            if signal_type and do_rebin:
                if "PNN" in var:
                    bins=bins   
                else:
                    bins = bin_dict[var][btag]
                
                
            else:
                if "PNN" in var:
                    bins = np.linspace(0, 1, 40000).tolist()  
                else:
                    bins = bin_dict[var][btag]
            
            out_root_file = R.TFile(f"{output_folder}/{f_strip}_{era}_{btag}_{var}{signal_type}.root", "RECREATE")
            out_root_file.cd()
            hist_data_dict = {}
            for suffix in suffixs:
                
                train_weight = weight_dic_suffixs[suffix]
                data_tmp = rdf_main.Filter(selection_dic_suffixs[suffix][f'{btag}_{channel}']).Define("new_weight", train_weight).Filter("new_weight !=0")
                if "Run2022" in filename or "Run2023" in filename:
                    hist_data_dict[suffix] = data_tmp.Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var )
                else:
                    if var+suffix in data_tmp.GetColumnNames():
                        # hist_data[var+suffix+btag] = data[var+suffix+btag].Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var+suffix,"new_weight" )
                        hist_data_dict[suffix] = data_tmp.Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var+suffix,"new_weight" )
                    else:
                        # hist_data[var+suffix+btag] = data[var+suffix+btag].Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var,"new_weight" )
                        hist_data_dict[suffix] = data_tmp.Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var,"new_weight" )
                del data_tmp
            

            for suffix in suffixs:
                if "FF" in filename:
                    for ibins in range(0, hist_data_dict[suffix].GetNbinsX() +1):
                        hist_data_dict[suffix].SetBinError(ibins, 0)
                hist_data_dict[suffix].Write()
                
            out_root_file.Close()
            print(f"saved to file {output_folder}/{f_strip}_{era}_{btag}_{var}{signal_type}.root")
    
    out_root_file = None
    data = None
    hist_data = None
    rdf = None
    gc.collect()
#folder_path, filename, era, variables, suffixs, channel, btag, lumi = args
# process_file(("2022postEE_mt_Version10_nominal", "ZZto4L_TuneCP5_13p6TeV_powheg-pythia8_Run3Summer22EENanoAODv12_mt.root", "2022postEE", ["PNN_100", "PNN_60"], ["__jerUncDown", "__jerUncUp", "__muon_Iso_down", "__muon_Iso_up", "__FF_closureDown","__FF_closureUp"],"mt", "nob", 27e3) )
# process_file(("fitting_template_Version10/2022postEE_mt_Version10_nominal", "Muon_Sep2022_Run2022F_mt.root", "2022postEE", ["PNN_100"], ["__jerUncDown", "__jerUncUp"],"mt", "nob", 27e3) )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot btag variables from ROOT files with weights.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing ROOT files')
    parser.add_argument('--shift', nargs='+', type=str, help='Shift to plot (e.g., __jesUncTotalUp)', default=[])
    parser.add_argument('--era', type=str, default='2022postEE', help='input era, 2022postEE or 2022EE')
    parser.add_argument('--channel', type=str, default='mt', help='decay channel, mt, et, tt, em')
    parser.add_argument('--tag', type=str, help='subscript of output folder' )
    parser.add_argument('--PNN', type=int, default=1, help='run PNN score or mt_tot')
    parser.add_argument('--shift_file', type=str, help='Path to a text file containing shift values, one per line')
    parser.add_argument('--mass', nargs='+', help='mass to run')
    parser.add_argument('--signal_type', type=str, help='ggH or bbH type of rebin' )
    parser.add_argument('--do_rebin', type=int, default = 1, help='rerun rebin or not, 0 to run 40000 bins, 1 to read existing rebin' )
    parser.add_argument('--make_plot', type=int, default = 0, help='make ntuple->histogram for control plots' )
    args = parser.parse_args()
 
    if args.shift_file:
        args.shift = read_shift_file(args.shift_file)

    
    PNN_vars= []
    mass = args.mass
    for m in mass:
        try:
            mass = int(m)
            PNN_vars.append(f"PNN_{m}") 
        except ValueError:
            PNN_vars.append(m)

    
    
    os.makedirs(f"{args.folder_path}_{args.tag}", exist_ok=True)
    lumi_dict = {
        "2022EE":8.077009684e3,
        "2022postEE":  26.671609707e3,
        "2023":  18.062659111e3, # B + C
        "2023BPix": 9.693130053e3, # D 
    }
    lumi = lumi_dict[args.era]
    files=[]
    if "" not in args.shift:
        args.shift.insert(0, "")
    
    for filename in os.listdir(args.folder_path):
        # print(filename)
        if not  filename.endswith(".root"):
            continue
        if args.make_plot:
            if ("M-100" not in filename) and  ( ("2HDM" in filename )or  ("BBH" in filename)):  #   
                continue
        files.append([args.folder_path, filename, args.era, copy.deepcopy(PNN_vars), args.shift, args.channel,  lumi, args.signal_type, args.do_rebin, args.tag])


    files_final = []
    print(files_final)
    from pathlib import Path
    import multiprocessing as mp
    from itertools import islice
    # 预定义路径和常量
    output_folder = Path(f"{args.folder_path}_{args.tag}")
    num_cores_to_use = 60
    max_jobs_per_iteration = 60

    # 筛选未完成任务
    for f in files:
        for var in list(f[3]):  # Use list(f[3]) to make a copy for safe iteration
            f_strip = f[1].replace(".root", "")
            if check_finished(f"{args.folder_path}_{args.tag}",f[1] , var, args.era, args.signal_type):
                f[3].remove(var)  # Removing PNN_vars that have finished
        if  f[3]:
            print(f"file {f[1]} has unfinished jobs")
            # print(files_final)
            files_final.append(f)

    # 分块并行处理
    print(files_final)
    # 分块提交任务
    def chunker(seq, size):
        return (seq[i:i+size] for i in range(0, len(seq), size))
    # 修改进程池初始化逻辑
    with mp.Pool(
        processes=num_cores_to_use,
        maxtasksperchild=50  # 每子进程处理50个任务后自动重启
    ) as pool:
        for chunk in chunker(files_final, max_jobs_per_iteration):
            print(f"提交任务块: {[f[1] for f in chunk]}")
            pool.map(process_file, chunk)  # 使用 map 确保顺序执行
            if not args.make_plot:
                time.sleep(3)  # 控制提交频率

    print("所有任务已完成")
    sys.exit()
