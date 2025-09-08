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

def check_finished(folder, filename, var,  btag_list, era):
    f_strip = filename.replace(".root", "")
    if var == "mt_tot":
        btag_list_tmp = ["nob", "btag"]  ## for mt_tot, don't split in pt_tt
    else:
        btag_list_tmp =  btag_list
    if "2HDM" in filename or "BBH" in filename:
        match = re.search(r'M-(\d+)_', filename)
        if match:
            masses_check = [int(match.group(1))]
            m = masses_check[0]
            if f"PNN_{m}" not in var and (var != "mt_tot"):
                # print(f"no need to run for PNN score {folder}/{f_strip}_era_{var + suffixs[1]}_{btag}")
                return True
    for btag in btag_list_tmp:
        if "tmp" in f_strip:
            continue
        if not os.path.exists(f"{folder}/{f_strip}_{era}_{btag}_{var}.root"):
            print("file not finished: ", f"{folder}/{f_strip}_{era}_{btag}_{var}.root")
            return False
        else:
            # print("file not finished: ", f"{folder}/{f_strip}_{era}_{btag}_{var}.root")
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
        return var_name
    else:
        return var_base

def process_file(args):
    folder_path, filename, era, variables, suffixs_ori, channel, btag_list, lumi = args
    f_strip = filename.replace(".root", "")
    output_folder = f"{folder_path}_output"
    if not filename.endswith(".root"):
        print(filename, "not endwith root")
        return
    if variables == []:
        print(f"finished all variables for file {filename}")
        return
    file_path = os.path.join(folder_path, filename)
    rdf = R.RDataFrame("ntuple", file_path)
    suffixs = []    
    for suffix in suffixs_ori:
        no_syst = True
        # if suffix not in 

        for v in rdf.GetColumnNames():
            if suffix in v:
                no_syst = False
        if not no_syst:
            suffixs.append(suffix)
    
    if ("Run2022" in filename) or ("Sep202" in filename):
            suffixs =[""]
    # print("running for systematics: ",suffixs)
    data = {}
    weights = {}
    if "" not in suffixs:
        suffixs.append("")
    for suffix in suffixs:
        extramuon_veto = get_variable_df(rdf, "extramuon_veto",suffix)
        extraelec_veto = get_variable_df(rdf, "extraelec_veto",suffix)
        eta_1 = get_variable_df(rdf, "eta_1",suffix)
        dz_1 = get_variable_df(rdf, "dz_1",suffix)
        dxy_1 = get_variable_df(rdf, "dxy_1",suffix)
        iso_1 = get_variable_df(rdf, "iso_1",suffix)
        phi_2 = get_variable_df(rdf,"phi_2",suffix)
        deltaR_ditaupair = get_variable_df(rdf, "deltaR_ditaupair",suffix)
        pt_1 = get_variable_df(rdf, "pt_1",suffix)
        eta_2 = get_variable_df(rdf, "eta_2",suffix)
        dz_2 = get_variable_df(rdf, "dz_2",suffix)
        dxy_2 = get_variable_df(rdf, "dxy_2",suffix)
        iso_2 = get_variable_df(rdf, "iso_2",suffix)
        pt_2 = get_variable_df(rdf, "pt_2",suffix)
        nbtag = get_variable_df(rdf, "nbtag",suffix)
        q_1 = get_variable_df(rdf, "q_1",suffix)
        q_2 = get_variable_df(rdf, "q_2",suffix)
        mt_1 = get_variable_df(rdf, "mt_1", suffix)
        gen_match_2 = get_variable_df(rdf, "gen_match_2",suffix)
        ZPtMassReweightWeight=get_variable_df(rdf, "ZPtMassReweightWeight", suffix)
        is_wjets =  "is_wjets"
        is_ttbar = "is_ttbar"
        btag_weight = get_variable_df(rdf, "btag_weight",suffix)
        pt_tt = get_variable_df(rdf, "pt_tt", suffix)
        pzetamissvis= get_variable_df(rdf, "pzetamissvis", suffix)
        # btag_norm = rdf.Mean(f"{btag_weight}").GetValue()
        if channel == 'em':
            id_wgt_ele_wpTight = get_variable_df(rdf, "id_wgt_ele_wpTight",suffix)
            id_wgt_mu_2 = get_variable_df(rdf, "id_wgt_mu_2",suffix)
            trg_cross_mu23ele12 = get_variable_df(rdf, "trg_cross_mu23ele12",suffix)
            trg_cross_mu8ele23 = get_variable_df(rdf, "trg_cross_mu8ele23",suffix)
            trg_single_ele30 = get_variable_df(rdf, "trg_single_ele30",suffix)
            trg_single_mu24 = get_variable_df(rdf, "trg_single_mu24",suffix)
            trg_wgt_single_mu24 = get_variable_df(rdf, "trg_wgt_single_mu24",suffix)
            trg_wgt_single_ele30 = get_variable_df(rdf, "trg_wgt_single_ele30",suffix)
            FF_weight = get_variable_df(rdf, "FF_weight",suffix)
        if channel == "mt":
            trg_cross_mu20tau27_hps = get_variable_df(rdf, "trg_cross_mu20tau27_hps",suffix)
            trg_single_tau180_2 = get_variable_df(rdf, "trg_single_tau180_2",suffix)
            trg_single_mu24 = get_variable_df(rdf, "trg_single_mu24",suffix)
            id_tau_vsMu_Tight_2 = get_variable_df(rdf, "id_tau_vsMu_Tight_2",suffix)
            id_tau_vsJet_Medium_2 = get_variable_df(rdf, "id_tau_vsJet_Medium_2",suffix)
            id_tau_vsEle_VVLoose_2 = get_variable_df(rdf, "id_tau_vsEle_VVLoose_2",suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable_df(rdf, "id_wgt_tau_vsJet_Medium_2",suffix)
            FF_weight = get_variable_df(rdf, "FF_weight",suffix)
            # iso_wgt_mu_1 = get_variable_df(rdf, "iso_wgt_mu_1",suffix)
            trg_wgt_ditau_crosstau_2 = get_variable_df(rdf, "trg_wgt_ditau_crosstau_2",suffix)
            id_wgt_tau_vsMu_Tight_2 = get_variable_df(rdf, "id_wgt_tau_vsMu_Tight_2",suffix)
            id_wgt_mu_1 = get_variable_df(rdf, "id_wgt_mu_1",suffix)
            # print(4)
        if channel == 'et': 
            trg_single_ele30 = get_variable_df(rdf, "trg_single_ele30", suffix)    
            trg_single_tau180_2 = get_variable_df(rdf, "trg_single_tau180_2", suffix)
            id_tau_vsMu_VLoose_2 = get_variable_df(rdf, "id_tau_vsMu_VLoose_2", suffix)
            id_tau_vsEle_Tight_2 = get_variable_df(rdf, "id_tau_vsEle_Tight_2", suffix)
            id_tau_vsJet_Medium_2 = get_variable_df(rdf, "id_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable_df(rdf, "id_wgt_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsEle_Tight_2 = get_variable_df(rdf, "id_wgt_tau_vsEle_Tight_2", suffix)
            FF_weight = get_variable_df(rdf, "FF_weight",suffix)
            id_wgt_ele_wpTight = get_variable_df(rdf, "id_wgt_ele_wpTight", suffix)
            trg_wgt_single_ele30 = get_variable_df(rdf, "trg_wgt_single_ele30", suffix)
            trg_wgt_ditau_crosstau_2 = get_variable_df(rdf, "trg_wgt_ditau_crosstau_2", suffix)
        if channel == 'tt':
            trg_double_tau30_plusPFjet60 = get_variable_df(rdf, "trg_double_tau30_plusPFjet60", suffix)
            trg_double_tau30_plusPFjet75 = get_variable_df(rdf, "trg_double_tau30_plusPFjet75", suffix)
            trg_double_tau35_mediumiso_hps = get_variable_df(rdf, "trg_double_tau35_mediumiso_hps", suffix)
            trg_single_deeptau180_1 = get_variable_df(rdf, "trg_single_tau180_1", suffix)
            trg_single_deeptau180_2 = get_variable_df(rdf, "trg_single_tau180_2", suffix)
            id_tau_vsJet_Medium_1 = get_variable_df(rdf, "id_tau_vsJet_Medium_1", suffix)
            id_tau_vsEle_VVLoose_1 = get_variable_df(rdf, "id_tau_vsEle_VVLoose_1", suffix)
            id_tau_vsMu_VLoose_1 = get_variable_df(rdf, "id_tau_vsMu_VLoose_1", suffix)
            id_tau_vsJet_Medium_2 = get_variable_df(rdf, "id_tau_vsJet_Medium_2", suffix)
            id_tau_vsEle_VVLoose_2 = get_variable_df(rdf, "id_tau_vsEle_VVLoose_2", suffix)
            id_tau_vsMu_VLoose_2 = get_variable_df(rdf, "id_tau_vsMu_VLoose_2", suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable_df(rdf, "id_wgt_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsJet_Medium_1 = get_variable_df(rdf, "id_wgt_tau_vsJet_Medium_1", suffix)
            FF_weight = get_variable_df(rdf, "FF_weight", suffix)
            trg_wgt_ditau_crosstau_1  = get_variable_df(rdf, "trg_wgt_ditau_crosstau_1", suffix)
            trg_wgt_ditau_crosstau_2 = get_variable_df(rdf, "trg_wgt_ditau_crosstau_2", suffix)
        print("finish getting variables. ")
        if not mt_1:
            print("fatal!! cannot retrieve variables for file ", filename)
            sys.exit(-1)
        selection_dic = {} 
        if channel == "mt":
            selection_dic['mt'] = f"((({trg_cross_mu20tau27_hps}==1)||({trg_single_mu24}==1)||({trg_single_tau180_2}==1)) && \
                ({pt_1}>25.0) && ({pt_2}>30) && ({extramuon_veto}==0)  &&  ({extraelec_veto}==0) && \
                ({iso_1}<0.15) && abs({eta_1} ) < 2.1 && \
                ({id_tau_vsMu_Tight_2}>0) && ({id_tau_vsJet_Medium_2}>0) && ({id_tau_vsEle_VVLoose_2}>0 ) && \
                (( ({gen_match_2} != 6) && ({is_wjets}>0) ) || ({is_wjets}<1)  ) &&  (({q_1} * {q_2})<0) && ({mt_1}<50)  && ({mt_1}>0)  ) && ({FF_weight} !=0)"
            selection_dic["nob_mt"] = f"{selection_dic['mt']} && ({nbtag}==0) && (( ({gen_match_2} != 6) && ({is_ttbar}>0) ) || ({is_ttbar}<1)  )" 
            selection_dic["nob1_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 0 && {pt_tt} < 50) " 
            selection_dic["nob2_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 50 && {pt_tt} < 100) " 
            selection_dic["nob3_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 100 && {pt_tt} < 200) " 
            selection_dic["nob4_mt"] = f"{selection_dic["nob_mt"]} && ({pt_tt} > 200) " 

            selection_dic["btag_mt"] = f"{selection_dic['mt']} && ({nbtag}==1)"
            # print(5)
        elif channel == "et":
            selection_dic['et'] = f"((({trg_single_ele30}==1)||({trg_single_tau180_2}==1))&& \
                ({pt_1}>30) && ({pt_2}>30)  &&  ({extramuon_veto}==0)  && ({extraelec_veto}==0) && \
                ({iso_1}<0.15) && abs({eta_1} ) < 2.1 && \
                ({id_tau_vsMu_VLoose_2}>0)  && ({id_tau_vsEle_Tight_2}>0) && ({id_tau_vsJet_Medium_2}>0 ) && \
                ((   ({gen_match_2} != 6) && ({is_wjets}>0) ) || ({is_wjets}<1)  ) && (({q_1} * {q_2})<0) && ({mt_1}<50) && ({mt_1}>0) ) && ({FF_weight} !=0)"  # 
            selection_dic["nob_et"] = f"{selection_dic['et']} && ({nbtag}==0)"
            selection_dic["nob1_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 0 && {pt_tt} < 50) " 
            selection_dic["nob2_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 50 && {pt_tt} < 100) " 
            selection_dic["nob3_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 100 && {pt_tt} < 200) " 
            selection_dic["nob4_et"] = f"{selection_dic["nob_et"]} && ({pt_tt} > 200) " 

            selection_dic["btag_et"] = f"{selection_dic['et']} && ({nbtag}==1)"
        elif channel == 'tt':
            selection_dic['tt'] = f"(({trg_double_tau35_mediumiso_hps}==1) || ({trg_single_deeptau180_1}==1) || ({trg_single_deeptau180_2}==1) || ({trg_double_tau30_plusPFjet60}==1) || ({trg_double_tau30_plusPFjet75}==1))&& \
                ({pt_1}>40) && ({pt_2}>40) && ({extramuon_veto}==0) && ({extraelec_veto}==0) && \
                ({dz_1}<0.2) && ({dz_2}<0.2) && ({eta_1}<2.1) && ({eta_1}>-2.1) && ({eta_2}<2.1) && ({eta_2}>-2.1) && \
                (({id_tau_vsJet_Medium_1}>0) && ({id_tau_vsEle_VVLoose_1}>0) && ({id_tau_vsMu_VLoose_1}>0))&& \
                (({id_tau_vsJet_Medium_2}>0) && ({id_tau_vsEle_VVLoose_2}>0) && ({id_tau_vsMu_VLoose_2}>0))&& \
                ({deltaR_ditaupair}>0.5) && (({q_1} * {q_2})<0) && ({mt_1}>0) && ({FF_weight} !=0)"
            selection_dic["btag_tt"] = f"{selection_dic['tt']} && ({nbtag}==1) "
            selection_dic["nob_tt"] = f"{selection_dic['tt']} && ({nbtag}==0)"
            selection_dic["nob1_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 0 && {pt_tt} < 50) " 
            selection_dic["nob2_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 50 && {pt_tt} < 100) " 
            selection_dic["nob3_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 100 && {pt_tt} < 200) " 
            selection_dic["nob4_tt"] = f"{selection_dic["nob_tt"]} && ({pt_tt} > 200) " 

        elif channel == 'em':
            selection_dic['em'] = f"(({extramuon_veto}==0) && ({extraelec_veto}==0) && ({mt_1} >0) && \
                        (({trg_cross_mu23ele12}==1) || ({trg_cross_mu8ele23}==1) || ({trg_single_ele30}==1) || \
                        ({trg_single_mu24}==1) ) &&   ({pzetamissvis} >= -35) && \
                        (({eta_1}>-2.4) && ({eta_1}<2.4) && ({dz_1}<0.2) && ({dxy_1}<0.045) && ({iso_1}<0.15) && \
                        ({deltaR_ditaupair}>0.3) && ({pt_1}>15)) && \
                        (({eta_2}>-2.4) && ({eta_2}<2.4) && ({dz_2}<0.2) && ({dxy_2}<0.045) && ({iso_2}<0.2) && ({pt_2}>15)) && (({q_1} * {q_2})<0) )  && ({mt_1}>0) && ({FF_weight} !=0)"

            if ("M-100_2HDM" in filename) or ("M-105_2HDM" in filename) or ("M-95_2HDM" in filename) or ("M-90_2HDM" in filename) or ("M-110_2HDM" in filename):
                selection_dic['em'] =  f"{selection_dic['em']} && (abs(Train_weight) < 10)"
            selection_dic["nob_em"] = f"{selection_dic['em']} && ({nbtag}==0)"
            selection_dic["btag_em"] = f"{selection_dic['em']} && ({nbtag}==1)"
            selection_dic["nob1_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 0 && {pt_tt} < 50) " 
            selection_dic["nob2_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 50 && {pt_tt} < 100) " 
            selection_dic["nob3_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 100 && {pt_tt} < 200) " 
            selection_dic["nob4_em"] = f"{selection_dic["nob_em"]} && ({pt_tt} > 200) " 

        else:
            print("wrong channel provided!! ")
        # print("selection_dic", selection_dic )
        
        ## define weight
        train_weight_dic = {}
        DY_em_weight_dict = {"2022EE": 0.82218013,"2022postEE":0.78275661,"2023":0.90302339 , "2023BPix":0.89675196,}
        DY_em_weight=DY_em_weight_dict[era]

        if (not "Run2022" in filename) and (not "Run2023" in filename):
            if "2HDM" in filename:
                
                if channel =='em':
                    train_weight_dic['em'] = f"Xsec * {lumi} * puweight * genWeight / genEventSumW "
                elif channel =='tt':
                    train_weight_dic['tt'] = f"Xsec * {lumi} * puweight * genWeight/genEventSumW "
                elif channel == "mt":
                    train_weight_dic['mt'] = f"Xsec *  {lumi}  * puweight * genWeight/genEventSumW "
                elif channel == "et":
                    train_weight_dic['et'] = f"Xsec * {lumi} *  puweight * genWeight/genEventSumW "
            else:
                
                if channel =='em' and "DY" in filename:
                    train_weight_dic['em'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} * puweight * genWeight / genEventSumW * {btag_weight }  * {trg_wgt_single_ele30 } *{id_wgt_ele_wpTight} * {id_wgt_mu_2} *  {trg_wgt_single_mu24 } * {DY_em_weight} "
                elif channel == "em":
                    train_weight_dic['em'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} * puweight * genWeight / genEventSumW * {btag_weight }  * {trg_wgt_single_ele30 } *{id_wgt_ele_wpTight} * {id_wgt_mu_2} *  {trg_wgt_single_mu24 } * {FF_weight}"
                elif channel =='tt':
                    train_weight_dic['tt'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} * puweight * genWeight/genEventSumW *  {btag_weight }  * {id_wgt_tau_vsJet_Medium_2} * {id_wgt_tau_vsJet_Medium_1} * {FF_weight} * {trg_wgt_ditau_crosstau_1} *{trg_wgt_ditau_crosstau_2 }"
                elif channel == "mt":
                    train_weight_dic['mt'] = f"Xsec *  {lumi}  * {ZPtMassReweightWeight} * puweight * genWeight/genEventSumW * {btag_weight }   *  {FF_weight} *{id_wgt_tau_vsJet_Medium_2}  *{trg_wgt_ditau_crosstau_2} *  {id_wgt_tau_vsMu_Tight_2} * {id_wgt_mu_1 }"
                elif channel == "et":
                    train_weight_dic['et'] = f"Xsec * {lumi} * {ZPtMassReweightWeight} *  puweight * genWeight/genEventSumW * {btag_weight } * {id_wgt_tau_vsEle_Tight_2 } *   {FF_weight} * {id_wgt_tau_vsJet_Medium_2 } * {id_wgt_ele_wpTight} * {trg_wgt_ditau_crosstau_2 } * {trg_wgt_single_ele30 }"
            train_weight = train_weight_dic[channel]

        ## define channel, region selections
        for var in variables:
            if var == "mt_tot":
                btag_list_tmp = ["nob", "btag"]  ## for mt_tot, don't split in pt_tt
            else:
                btag_list_tmp =  btag_list

            for btag in btag_list_tmp:
                selection = selection_dic[f'{btag}_{channel}']
                data[var + suffix + btag ] = rdf.Filter(selection)
                if "Run2022" in filename or "Run2023" in filename:
                    continue
                weights[var + suffix]=train_weight
                data[var + suffix +btag ] = data[var + suffix+btag ].Define("new_weight", train_weight).Filter("new_weight !=0")
        # print(data)

    colors = ['blue', 'red', 'green']
    hist_data = {}
    
    for var in variables:
        if var == "mt_tot":
            btag_list_tmp = ["nob", "btag"]  ## for mt_tot, don't split in pt_tt
        else:
            btag_list_tmp =  btag_list
        for btag in btag_list_tmp:
            out_root_file = R.TFile(f"{output_folder}/{f_strip}_{era}_{btag}_{var}.root", "RECREATE")
            out_root_file.cd()
            print(f"init plot for variable {var}")
            for i, suffix in enumerate(suffixs):

                # Create bins for each range
                if btag == "nob":
                    mt_tot_bins = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,5000.0]
                else:
                    mt_tot_bins = [0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,250.0,300.0,350.0,400.0,500.0,600.0,700.0,800.0,900.0,5000.0]
                    #  [0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,250.0,300.0,350.0,400.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,5000.0]
                bins = np.linspace(0, 1, 40000).tolist() if var != "mt_tot" else mt_tot_bins
                
                if "Run2022" in filename or "Run2023" in filename:
                    hist_data[var+suffix+btag] = data[var+suffix+btag].Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var )
                    hist_data[var+suffix+btag].Write()
                else:
                    if var+suffix in data[var+suffix+btag].GetColumnNames():
                        hist_data[var+suffix+btag] = data[var+suffix+btag].Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var+suffix,"new_weight" )
                    else:
                        ## for weight systematics only nominal var exists
                        hist_data[var+suffix+btag] = data[var+suffix+btag].Histo1D((var+suffix, var+suffix ,len(bins)-1, array.array('d', bins)),var,"new_weight" )
                    
            # for suffix in suffixs:
                    hist_data[var+suffix+btag].Write()

            out_root_file.Close()
            print(f"saved to file {output_folder}/{f_strip}_{era}_{btag}_{var}.root")
            gc.collect()
    
    out_root_file = None
    data = None
    hist_data = None
    rdf = None
    gc.collect()
#folder_path, filename, era, variables, suffixs, channel, btag, lumi = args
# process_file(("2022postEE_mt_Version10_nominal", "ZZto4L_TuneCP5_13p6TeV_powheg-pythia8_Run3Summer22EENanoAODv12_mt.root", "2022postEE", ["PNN_100", "PNN_60"], ["__jerUncDown", "__jerUncUp", "__muon_Iso_down", "__muon_Iso_up", "__FF_closureDown","__FF_closureUp"],"mt", "nob", 27e3) )
# process_file(("fitting_template_Version10/2022postEE_mt_Version10_nominal", "Muon_Sep2022_Run2022F_mt.root", "2022postEE", ["PNN_100"], ["__jerUncDown", "__jerUncUp"],"mt", "nob", 27e3) )
# process_file(("2022EE_em_Version10_nominal", "FF_Combined.root", "2022EE", ["PNN_100"], ["__mismodelingUncDown", "__mismodelingUncUp"],"em", ["nob1"], 8.077009684e3) )
# process_file(("2023_em_Version10_nominal_fix_jetveto", "FF_Combined.root", "2023", ["PNN_100"], ["__mismodelingUncDown", "__mismodelingUncUp"],"em", ["nob1"],   18.062659111e3) )
# process_file(("2022EE_mt_Version11_nominal" , "DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8Run3Summer22NanoAODv12_mt.root", "2022EE",  ["PNN_100"], ["__jerUncDown", "__jerUncUp", "__DY_pTll_reweightingdown1", "__DY_pTll_reweightingup1"], "mt", ["nob1"],   18.062659111e3))
# process_file(("2022EE_mt_Version11_nominal" , "WtoLNu-4Jets_4J_TuneCP5_13p6TeV_madgraphMLM-pythia8_Run3Summer22NanoAODv12_mt.root", "2022EE",  ["PNN_100"], ["__jerUncDown", "__jerUncUp", "__DY_pTll_reweightingdown1", "__DY_pTll_reweightingup1"], "mt", ["nob1"],   18.062659111e3))
# sys.exit(0)


    # for f in files:
    #     # if "TTto" not in f[1]:
    #     #     continue
    #     for var in list(f[3]):  # Use list(f[3]) to make a copy for safe iteration
    #         f_strip = f[1].replace(".root", "")
    #         if check_finished(f"{folder_path}_output",f[1] , var, btag_list, era):
    #             #os.path.exists(f"{folder_path}_output/{f_strip}_{era}_{btag}_{var}.root"):
    #             # print(f"finished running for {folder_path}_output", f[1], var, suffixs, btag)
    #             f[3].remove(var)  # Removing variables that have finished
    #     if  f[3]:
    #         print(f"file {f[1]} has unfinished jobs")
    #         # print(files_final)
    #         files_final.append(f)
    # num_cores_to_use = 5  # Set the number of cores you want to use
    # pool = Pool(processes=num_cores_to_use)
    # max_jobs_per_iteration = 5  # Limit the number of jobs submitted at once
    # max_jobs = 5
    # for f in files_final:
    #     print("About to run jobs for:", f[0], f[1], f[2], f[3], f[5], f[6])
    # try:
    # #     while files_final:
    #     jobs_submitted = 0  # Reset jobs submitted counter for each iteration
    #     for f in list(files_final):  # Use a copy of the list for safe iteration
    #         memory_usage = get_memory_usage()
    #         if memory_usage >20.0 and jobs_submitted <max_jobs_per_iteration:
    #             print(f" Submitting job for {f[1]}.")
    #             pool.apply_async(process_file, args=(f,))
    #             files_final.remove(f)
    #             jobs_submitted += 1
    #             time.sleep(3)  # Add a small delay between job submissions to prevent rapid submissions
    #             gc.collect()
                    
    #             # if jobs_submitted ==0:
    #             #     time.sleep(60)  # Wait for 1 minute before checking again if no jobs were submitted

    #             # # Re-check the memory usage to adjust dynamically
    #             # while ((running_jobs := sum(1 for p in pool._pool if p.is_alive())) >= max_jobs):
    #             #     print(f"Running jobs ({running_jobs}) have reached the maximum limit. Waiting...")
    #             #     time.sleep(60)  # Adjust wait time as needed

    # finally:
    #     pool.close()
    #     pool.join()
    # print("finished all jobs")
    # gc.collect()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot btag variables from ROOT files with weights.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing ROOT files')
    parser.add_argument('--shift', nargs='+', type=str, help='Shift to plot (e.g., __jesUncTotalUp)')
    parser.add_argument('--era', type=str, default='2022postEE', help='input era, 2022postEE or 2022EE')
    parser.add_argument('--channel', type=str, default='mt', help='decay channel, mt, et, tt, em')
    parser.add_argument('--btag', nargs= '+', type=str, default=['nob'], help='btag selection, nob (nob1/2/3/4),  btag')
    parser.add_argument('--PNN', type=int, default=1, help='run PNN score or mt_tot')
    parser.add_argument('--shift_file', type=str, help='Path to a text file containing shift values, one per line')
    parser.add_argument('--mass', nargs='+', help='mass to run')
    args = parser.parse_args()
    # bins = np.linspace(0, 1, 2001).tolist()  # 2001 points to get 2000 intervals
    # bins = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,2100.0,5000.0]
        # If a shift file is provided, read the shift values from the file
    if args.shift_file:
        args.shift = read_shift_file(args.shift_file)
    # variables = [args.variables, args.variables + args.shift[0], args.variables + args.shift[1]]
    # mass = [60,  70, 80,  90,  100,  110,  120,     130,  140,  160,  180, 200,250, 65,75,85,95,105,115,125,135,] # 
    # mass = [60, 100, 130] # , 500, 2000
    # mass = [100,60,130]
    # # mass = [] # 65,75,85,95,105,115,125,135,
    # PNN_vars= [f"PNN_{m}" for m in mass]
    # # PNN_vars= []
    
    # main(args.folder_path,args.era, PNN_vars, args.shift, args.channel, args.btag)
    PNN_vars= []
    mass = args.mass
    for m in mass:
        if m != "mt_tot":
            PNN_vars.append(f"PNN_{m}") 
        else:
            PNN_vars.append(m)
    # PNN_vars= [f"PNN_{m}" for m in mass]
    # PNN_vars.append("mt_tot")
    
    
    os.makedirs(f"{args.folder_path}_output", exist_ok=True)
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
        # if not  "DYto2L-2Jets_MLL-50_0J_TuneCP5_13p6" in filename and  "GluGluHto2Tau_M-100_2HDM" not  in filename and "FF_Combined" not in file:  #   
        #     continue
        # if not "DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8Run3Summer22NanoAODv12_mt.root" in filename and not "WtoLNu-4Jets_4J_TuneCP5_13p6TeV_madgraphMLM-pythia8_Run3Summer22NanoAODv12_mt.root" in filename:
        #     continue
        files.append([args.folder_path, filename, args.era, copy.deepcopy(PNN_vars), args.shift, args.channel, args.btag, lumi])


    files_final = []
    print(files_final)
    from pathlib import Path
    import multiprocessing as mp
    from itertools import islice
    # 预定义路径和常量
    output_folder = Path(f"{args.folder_path}_output")
    num_cores_to_use = 30
    max_jobs_per_iteration = 30

    # 筛选未完成任务
    for f in files:
        # if "TTto" not in f[1]:
        #     continue
        for var in list(f[3]):  # Use list(f[3]) to make a copy for safe iteration
            f_strip = f[1].replace(".root", "")
            if check_finished(f"{args.folder_path}_output",f[1] , var, args.btag, args.era):
                #os.path.exists(f"{args.folder_path}_output/{f_strip}_{args.era}_{btag}_{var}.root"):
                # print(f"finished running for {args.folder_path}_output", f[1], var, args.shift, btag)
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
            time.sleep(3)  # 控制提交频率

    print("所有任务已完成")
    # mass = [160,  180, 200,250,65,75 ]
    # PNN_vars= [f"PNN_{m}" for m in mass]
    # main(args.args.folder_path,args.args.era, PNN_vars, args.shift, args.args.channel, args.btag)
     
    # mass = [85,95,105,115,125,135, ]
    # PNN_vars= [f"PNN_{m}" for m in mass]
    # main(args.args.folder_path,args.args.era, PNN_vars, args.shift, args.args.channel, args.btag)
    # sys.exit(0)