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

def get_filtered_columns(rdf, suffixs):
    all_columns = []
    columns = []
    for i in rdf.GetColumnNames():
        all_columns.append(str(i))    
    # Ensure all elements in 'all_columns' are strings
    all_columns = [col.decode() if isinstance(col, bytes) else col for col in all_columns]
    
    for suffix in suffixs:
        if suffix == "":
            for column in all_columns:
                if "__" not in column:
                    columns.append(column)
        else:
            for column in all_columns:
                if suffix in column:
                    columns.append(column)
    return columns
def get_memory_usage():
    # Return the percentage of available memory
    memory_info = psutil.virtual_memory()
    available_memory_percentage = memory_info.available / memory_info.total * 100
    return available_memory_percentage

def get_variable(tree, var_base, var_suffix=""):
    var_name = f"{var_base}{var_suffix}"
    # print(var_name)
    if var_name in tree.keys():
        # print("yes")
        var = tree[var_name]
        dtype = var.dtype
        if not np.issubdtype(dtype, np.number) or dtype == np.uint8 or dtype == np.int16:
            var = var.astype(np.int32)
        # print(var_name)

        return var
    else:
        # print("no")
        # print(var_name)
        # print(tree.keys())
        if var_base not in  tree.keys() :
            print(f"{var_base} not exists!!!!")
            sys.exit(-1)
        var = tree[var_base]
        dtype = var.dtype
        if not np.issubdtype(dtype, np.number) or dtype == np.uint8 or dtype == np.int16:
            var = var.astype(np.int32)      
        # print(var_name)
        
        return var
# Function to save numpy arrays as ROOT histograms
def save_hist_to_root(hist_data, bins, var, output_file):
    if os.path.exists(output_file):
        root_file = R.TFile(output_file, "UPDATE")
    else:
        root_file = R.TFile(output_file, "RECREATE")
    hist_name = f"{var}"
    root_hist = R.TH1F(hist_name, hist_name, len(bins)-1, bins)
    for i, count in enumerate(hist_data):
        root_hist.SetBinContent(i+1, count)
    root_hist.Write()
    root_file.Close()
def check_finished(folder, filename, var, suffixs, btag):
    f_strip = filename.replace(".root", "")
    # print("checking file", f_strip)
    # print(suffixs)
    if suffixs == [""]:
        # running only for nominal
        if os.path.exists(f"{folder}/{f_strip}_era_{var + suffixs[0]}_{btag}.root"):
            # print("file finished: ", f"{folder}/{f_strip}_era_{var + suffixs[0]}_{btag}")
            return True
        else: 
            return False
    if "Run2022" in filename:
        if os.path.exists(f"{folder}/{f_strip}_era_{var + suffixs[0]}_{btag}.root"):
            # print("file finished: ", f"{folder}/{f_strip}_era_{var + suffixs[0]}_{btag}")
            return True
        else: 
            return False
    if "2HDM" in filename:
        match = re.search(r'Hto2Tau_M-(\d+)', filename)
        if match:
            masses_check = [int(match.group(1))]
            m = masses_check[0]
            if f"PNN_{m}" not in var and (var != "mt_tot"):
                # print(f"no need to run for PNN score {folder}/{f_strip}_era_{var + suffixs[1]}_{btag}")
                return True
    if  os.path.exists(f"{folder}/{f_strip}_era_{var + suffixs[1]}_{btag}.root"):
        # print("file finished: ", f"{folder}/{f_strip}_era_{var + suffixs[1]}_{btag}")
        return True
    else:
        return False
def process_file(args):
    folder_path, filename, era, variables, suffixs, channel, btag, lumi = args
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
    ## fill the neccessary variables here
    useful_vars = ["mt_tot", 'PNN_100', 'PNN_105', 'PNN_110', 'PNN_115', 'PNN_120', 'PNN_125', 'PNN_130', 'PNN_135', 'PNN_140', 'PNN_160', 'PNN_180', 'PNN_200', 'PNN_250', 'PNN_60', 'PNN_65', 'PNN_70', 'PNN_75', 'PNN_80', 'PNN_85', 'PNN_90', 'PNN_95', 'mt_1', "extramuon_veto","extraelec_veto","eta_1","dz_1","dxy_1","iso_1","phi_2","deltaR_ditaupair","pt_1","eta_2","dz_2","dxy_2","iso_2","pt_2","nbtag","q_1","q_2","puweight","Xsec","genWeight","genEventSumW","gen_match_2","is_wjets","is_ttbar","btag_weight","id_wgt_ele_wpTight","id_wgt_mu_2","trg_cross_mu23ele12","trg_cross_mu8ele23","trg_single_ele30","trg_single_ele32","trg_single_ele35","trg_single_mu24","trg_single_mu27","trg_wgt_single_mu24","trg_wgt_single_ele30","trg_cross_mu20tau27_hps","trg_single_tau180_2","trg_single_mu24","trg_single_mu27","id_tau_vsMu_Tight_2","id_tau_vsJet_Medium_2","id_tau_vsEle_VVLoose_2","id_wgt_tau_vsJet_Medium_2","FF_weight","iso_wgt_mu_1","trg_wgt_ditau_crosstau_2","id_wgt_tau_vsMu_Tight_2","id_wgt_mu_1","trg_single_ele30"    ,"trg_single_ele32","trg_single_ele35","trg_single_tau180_2","id_tau_vsMu_VLoose_2","id_tau_vsEle_Tight_2","id_tau_vsJet_Medium_2","id_wgt_tau_vsJet_Medium_2","FF_weight","id_wgt_tau_vsEle_Tight_2","id_wgt_ele_wpTight","trg_wgt_single_ele30","trg_wgt_ditau_crosstau_2","trg_double_tau30_plusPFjet60","trg_double_tau30_plusPFjet75","trg_double_tau35_mediumiso_hps","trg_single_deeptau180_1","trg_single_deeptau180_2","id_tau_vsJet_Medium_1","id_tau_vsEle_VVLoose_1","id_tau_vsMu_VLoose_1","id_tau_vsJet_Medium_2","id_tau_vsEle_VVLoose_2","id_tau_vsMu_VLoose_2","id_wgt_tau_vsJet_Medium_2","id_wgt_tau_vsJet_Medium_1","FF_weight","trg_wgt_ditau_crosstau_1","trg_wgt_ditau_crosstau_2"]
    no_syst = "True"
    for v in rdf.GetColumnNames():
        if suffixs[1] in v:
            no_syst = False
    if no_syst:
        if "Run2022" in filename:
            suffixs =[""]
            pass
        else:
            print(f"no systematics {suffixs[1] } for file {filename}")
            return 

    tree = {}
    columns = get_filtered_columns(rdf, suffixs)
    columns_final = []
    for i in columns:
        if i.split('__', 1)[0]  in useful_vars:
            columns_final.append(i)
    try:
        tree = rdf.AsNumpy(columns=columns_final)
        print(filename, variables, '==========')
        print("Successfully converted to NumPy array.")
    except Exception as e:
        print(f"Error during conversion: {e}")
    del rdf
    
    data = {var + suffix: [] for var in variables for suffix in suffixs}
    weights = {var + suffix: [] for var in variables for suffix in suffixs}
    for suffix in suffixs:
        print(1)
        extramuon_veto = get_variable(tree, "extramuon_veto",suffix)
        extraelec_veto = get_variable(tree, "extraelec_veto",suffix)
        eta_1 = get_variable(tree, "eta_1",suffix)
        dz_1 = get_variable(tree, "dz_1",suffix)
        dxy_1 = get_variable(tree, "dxy_1",suffix)
        iso_1 = get_variable(tree, "iso_1",suffix)
        phi_2 = get_variable(tree,"phi_2",suffix)
        deltaR_ditaupair = get_variable(tree, "deltaR_ditaupair",suffix)
        pt_1 = get_variable(tree, "pt_1",suffix)
        eta_2 = get_variable(tree, "eta_2",suffix)
        dz_2 = get_variable(tree, "dz_2",suffix)
        dxy_2 = get_variable(tree, "dxy_2",suffix)
        iso_2 = get_variable(tree, "iso_2",suffix)
        pt_2 = get_variable(tree, "pt_2",suffix)
        nbtag = get_variable(tree, "nbtag",suffix)
        q_1 = get_variable(tree, "q_1",suffix)
        q_2 = get_variable(tree, "q_2",suffix)
        puweight = get_variable(tree, "puweight",suffix)
        Xsec = get_variable(tree, "Xsec",suffix)
        genWeight = get_variable(tree, "genWeight",suffix)
        genEventSumW = get_variable(tree, "genEventSumW",suffix)
        gen_match_2 = get_variable(tree, "gen_match_2",suffix)
        print(2)
        is_wjets = get_variable(tree, "is_wjets",suffix)
        is_ttbar = get_variable(tree, "is_ttbar",suffix)
        btag_weight = get_variable(tree, "btag_weight",suffix)
        mt_1 = get_variable(tree, "mt_1", suffix)
        print(3)
        if channel == "em":
            id_wgt_ele_wpTight = get_variable(tree, "id_wgt_ele_wpTight",suffix)
            id_wgt_mu_2 = get_variable(tree, "id_wgt_mu_2",suffix)
            trg_cross_mu23ele12 = get_variable(tree, "trg_cross_mu23ele12",suffix)
            trg_cross_mu8ele23 = get_variable(tree, "trg_cross_mu8ele23",suffix)
            trg_single_ele30 = get_variable(tree, "trg_single_ele30",suffix)
            trg_single_ele32 = get_variable(tree, "trg_single_ele32",suffix)
            trg_single_ele35 = get_variable(tree, "trg_single_ele35",suffix)
            trg_single_mu24 = get_variable(tree, "trg_single_mu24",suffix)
            trg_single_mu27 = get_variable(tree, "trg_single_mu27",suffix)
            trg_wgt_single_mu24 = get_variable(tree, "trg_wgt_single_mu24",suffix)
            trg_wgt_single_ele30 = get_variable(tree, "trg_wgt_single_ele30",suffix)
        if channel == "mt":
            trg_cross_mu20tau27_hps = get_variable(tree, "trg_cross_mu20tau27_hps",suffix)
            trg_single_tau180_2 = get_variable(tree, "trg_single_tau180_2",suffix)
            trg_single_mu24 = get_variable(tree, "trg_single_mu24",suffix)
            trg_single_mu27 = get_variable(tree, "trg_single_mu27",suffix)
            id_tau_vsMu_Tight_2 = get_variable(tree, "id_tau_vsMu_Tight_2",suffix)
            id_tau_vsJet_Medium_2 = get_variable(tree, "id_tau_vsJet_Medium_2",suffix)
            id_tau_vsEle_VVLoose_2 = get_variable(tree, "id_tau_vsEle_VVLoose_2",suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable(tree, "id_wgt_tau_vsJet_Medium_2",suffix)
            FF_weight = get_variable(tree, "FF_weight",suffix)
            iso_wgt_mu_1 = get_variable(tree, "iso_wgt_mu_1",suffix)
            trg_wgt_ditau_crosstau_2 = get_variable(tree, "trg_wgt_ditau_crosstau_2",suffix)
            id_wgt_tau_vsMu_Tight_2 = get_variable(tree, "id_wgt_tau_vsMu_Tight_2",suffix)
            id_wgt_mu_1 = get_variable(tree, "id_wgt_mu_1",suffix)
            print(4)
        if channel == 'et': 
            trg_single_ele30 = get_variable(tree, "trg_single_ele30", suffix)    
            trg_single_ele32 = get_variable(tree, "trg_single_ele32", suffix)
            trg_single_ele35 = get_variable(tree, "trg_single_ele35", suffix)
            trg_single_tau180_2 = get_variable(tree, "trg_single_tau180_2", suffix)
            id_tau_vsMu_VLoose_2 = get_variable(tree, "id_tau_vsMu_VLoose_2", suffix)
            id_tau_vsEle_Tight_2 = get_variable(tree, "id_tau_vsEle_Tight_2", suffix)
            id_tau_vsJet_Medium_2 = get_variable(tree, "id_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable(tree, "id_wgt_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsEle_Tight_2 = get_variable(tree, "id_wgt_tau_vsEle_Tight_2", suffix)
            FF_weight = get_variable(tree, "FF_weight",suffix)
            id_wgt_ele_wpTight = get_variable(tree, "id_wgt_ele_wpTight", suffix)
            trg_wgt_single_ele30 = get_variable(tree, "trg_wgt_single_ele30", suffix)
            trg_wgt_ditau_crosstau_2 = get_variable(tree, "trg_wgt_ditau_crosstau_2", suffix)
        if channel == "tt":
            trg_double_tau30_plusPFjet60 = get_variable(tree, "trg_double_tau30_plusPFjet60", suffix)
            trg_double_tau30_plusPFjet75 = get_variable(tree, "trg_double_tau30_plusPFjet75", suffix)
            trg_double_tau35_mediumiso_hps = get_variable(tree, "trg_double_tau35_mediumiso_hps", suffix)
            trg_single_deeptau180_1 = get_variable(tree, "trg_single_deeptau180_1", suffix)
            trg_single_deeptau180_2 = get_variable(tree, "trg_single_deeptau180_2", suffix)
            id_tau_vsJet_Medium_1 = get_variable(tree, "id_tau_vsJet_Medium_1", suffix)
            id_tau_vsEle_VVLoose_1 = get_variable(tree, "id_tau_vsEle_VVLoose_1", suffix)
            id_tau_vsMu_VLoose_1 = get_variable(tree, "id_tau_vsMu_VLoose_1", suffix)
            id_tau_vsJet_Medium_2 = get_variable(tree, "id_tau_vsJet_Medium_2", suffix)
            id_tau_vsEle_VVLoose_2 = get_variable(tree, "id_tau_vsEle_VVLoose_2", suffix)
            id_tau_vsMu_VLoose_2 = get_variable(tree, "id_tau_vsMu_VLoose_2", suffix)
            id_wgt_tau_vsJet_Medium_2 = get_variable(tree, "id_wgt_tau_vsJet_Medium_2", suffix)
            id_wgt_tau_vsJet_Medium_1 = get_variable(tree, "id_wgt_tau_vsJet_Medium_1", suffix)
            FF_weight = get_variable(tree, "FF_weight", suffix)
            trg_wgt_ditau_crosstau_1  = get_variable(tree, "trg_wgt_ditau_crosstau_1", suffix)
            trg_wgt_ditau_crosstau_2 = get_variable(tree, "trg_wgt_ditau_crosstau_2", suffix)
        selection_dic = {} 
        if channel == "mt":
            selection_dic["mt"] = (((trg_cross_mu20tau27_hps==1)|(trg_single_mu24==1)|(trg_single_mu27==1)|(trg_single_tau180_2==1)) & \
                (pt_1 > 25.0) & (pt_2 > 30) & (extramuon_veto == 0)  &  (extraelec_veto == 0) & \
                (id_tau_vsMu_Tight_2 > 0) & (id_tau_vsJet_Medium_2 > 0) & (id_tau_vsEle_VVLoose_2 > 0 ) & \
                (( (gen_match_2 != 6) & (is_wjets>0) ) | (is_wjets <1)  ) &  ((q_1 * q_2) < 0) & (mt_1 < 70) )
            selection_dic["nob_mt"] = selection_dic["mt"] & (nbtag == 0) & (( (gen_match_2 != 6) & (is_ttbar>0) ) | (is_ttbar <1)  ) 
            selection_dic["btag_mt"] = selection_dic["mt"] & (nbtag == 1)
            print(5)
        elif channel == "et":
            selection_dic["et"] = (((trg_single_ele30 ==1)| (trg_single_ele32==1)|(trg_single_ele35==1)|(trg_single_tau180_2==1))& \
                (pt_1 > 30) & (pt_2 > 30)  &  (extramuon_veto == 0)  & (extraelec_veto == 0) & \
                (id_tau_vsMu_VLoose_2 > 0)  & (id_tau_vsEle_Tight_2 > 0) & (id_tau_vsJet_Medium_2 > 0 ) & \
                ((   (gen_match_2 != 6) & (is_wjets>0) ) | (is_wjets <1)  ) & ((q_1 * q_2) < 0) & (mt_1 < 70) )  # 
            selection_dic["nob_et"] = selection_dic["et"] & (nbtag == 0) & (( (gen_match_2 != 6) & (is_ttbar>0) ) | (is_ttbar <1)  ) 
            selection_dic["btag_et"] = selection_dic["et"] & (nbtag == 1)
            if era == "2022postEE":
                selection_dic["nob_et"] = selection_dic["et"] & (nbtag == 0) &~  (  ( (phi_2>1.8) & (phi_2< 2.7) & (eta_2 > 1.5)  & (eta_2<2.2) ) ) ## &~ stands for and not
                selection_dic["btag_et"] = selection_dic["et"] & (nbtag == 1) &~ (  ( (phi_2>1.8) & (phi_2< 2.7) & (eta_2 > 1.5)  &(eta_2<2.2) ) )
        elif channel == "tt":
            selection_dic["tt"] = ((trg_double_tau35_mediumiso_hps==1) | (trg_single_deeptau180_1==1) | (trg_single_deeptau180_2==1) | (trg_double_tau30_plusPFjet60==1) | (trg_double_tau30_plusPFjet75==1))& \
                (pt_1 > 40) & (pt_2 > 40) & (extramuon_veto == 0) & (extraelec_veto == 0) & \
                (dz_1 < 0.2) & (dz_2 < 0.2) & (eta_1 < 2.1) & (eta_1 > -2.1) & (eta_2 < 2.1) & (eta_2 > -2.1) & \
                ((id_tau_vsJet_Medium_1 > 0) & (id_tau_vsEle_VVLoose_1 > 0) & (id_tau_vsMu_VLoose_1 > 0))& \
                ((id_tau_vsJet_Medium_2 > 0) & (id_tau_vsEle_VVLoose_2 > 0) & (id_tau_vsMu_VLoose_2 > 0))& \
                (deltaR_ditaupair > 0.5) & ((q_1 * q_2) < 0)
            selection_dic["btag_tt"] = selection_dic["tt"] & (nbtag ==1) 
            selection_dic["nob_tt"] = selection_dic["tt"] & (nbtag ==0)
        elif channel == "em":
            selection_dic["em"] = ((extramuon_veto == 0) & (extraelec_veto == 0) & \
                        ((trg_cross_mu23ele12 == 1) | (trg_cross_mu8ele23 == 1) | (trg_single_ele30 == 1) |
                        (trg_single_ele32 == 1) | (trg_single_ele35 == 1) | (trg_single_mu24 == 1) | (trg_single_mu27 == 1)) & \
                        ((eta_1 > -2.4) & (eta_1 < 2.4) & (dz_1 < 0.2) & (dxy_1 < 0.045) & (iso_1 < 0.15) & \
                        (deltaR_ditaupair > 0.3) & (pt_1 > 15)) & \
                        ((eta_2 > -2.4) & (eta_2 < 2.4) & (dz_2 < 0.2) & (dxy_2 < 0.045) & (iso_2 < 0.2) & (pt_2 > 15)) & ((q_1 * q_2) < 0) ) 
            selection_dic["nob_em"] = selection_dic["em"] & (nbtag == 0)
            selection_dic["btag_em"] = selection_dic["em"] & (nbtag == 1)
        else:
            print("wrong channel provided!! ")
        # selection = ((nbtag == 0))
        # 应用筛选条件
        # print("selection_dic", selection_dic )
        print(6)
        selection = selection_dic[f'{btag}_{channel}']
        for var in variables:
            data[var + suffix ].append(get_variable(tree, var, suffix)[selection])
            print(7)
        print("finshied selection")
        # print(data, "data")
        # 计算 train_weight
        train_weight_dic = {}
        if not "Run2022" in filename:
            if channel =="em":
                train_weight_dic["em"] = (Xsec * lumi * genWeight / genEventSumW *((trg_wgt_single_ele30 * (trg_single_ele30 > 0) + 1 * (trg_single_ele30 < 1)) *id_wgt_ele_wpTight * id_wgt_mu_2 * btag_weight * puweight *(trg_wgt_single_mu24 * (trg_single_mu24 > 0) + 1 * (trg_single_mu24 < 1))))
            elif channel =="tt":
                train_weight_dic["tt"] = Xsec * lumi * puweight * genWeight/genEventSumW * btag_weight *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 * FF_weight * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 
            elif channel == "mt":
                train_weight_dic["mt"] = Xsec * lumi * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight *id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1 
            elif channel == "et":
                train_weight_dic["et"] = Xsec * lumi *  puweight * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2  *  btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2  * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30 
            train_weight = train_weight_dic[channel]
        # print("train_weight_dic", train_weight_dic )
        print("finshied weight")
        # 应用筛选条件并累积权重数据
        for var in variables:
            if "Run2022" in filename:
                continue
            if check_finished(output_folder, filename,  var, suffixs, btag):
                # print(f"already finished running for {output_folder}/{f_strip}_era_{var + suffixs[1]}_{btag}")
                continue
            print(var)
            weights[var + suffix].append(train_weight[selection])
            # print("finished ", var, suffix)
    
    print("Plotting and saving")
    colors = ['blue', 'red', 'green']
    hist_data = {}
    for var in variables:
        if check_finished(output_folder, filename,  var, suffixs, btag):
            print("wtf")
            f_strip = filename.replace(".root", "")
            print(f"{output_folder}/{f_strip}_era_{var + suffixs[1]}_{btag}.png")
            # print(output_folder, filename,  var, suffixs, btag)
            continue
        fig, (ax_main, ax_ratio) = plt.subplots(nrows=2, ncols=1, sharex=True, 
                                                gridspec_kw={'height_ratios': [3, 1]}, figsize=(8, 6))
        print("init plot")
        for i, suffix in enumerate(suffixs):
            bins = np.linspace(0, 1, 2001).tolist() if var != "mt_tot" else [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,2100.0,5000.0]
            if "Run2022" in filename:
                hist_data[var+suffix], bins, _ = ax_main.hist(data[var+suffix], bins=bins, histtype='step', 
                                                        label=var+ suffix, color=colors[i])
                print("finished processing data")
            else:
                hist_data[var+suffix], bins, _ = ax_main.hist(data[var+suffix], bins=bins, histtype='step', 
                                                        label=var+ suffix, color=colors[i], weights=weights[var+suffix])
        ax_main.set_title(f'{var}')
        ax_main.set_ylabel('Events')
        ax_ratio.set_ylim(0.8, 1.2)
        ax_main.legend()
        if len(suffixs) >= 3:
            ratio_up = np.divide(hist_data[var + suffixs[1]], hist_data[var], out=np.zeros_like(hist_data[var + suffixs[1]]), where=hist_data[var]!=0)
            ratio_down = np.divide(hist_data[var + suffixs[2]], hist_data[var], out=np.zeros_like(hist_data[var + suffixs[2]]), where=hist_data[var]!=0)

            ax_ratio.hist(bins[:-1], bins, weights=ratio_up, histtype='step', label=f'{var + suffixs[1]} / nominal', color='red')
            ax_ratio.hist(bins[:-1], bins, weights=ratio_down, histtype='step', label=f'{var + suffixs[2]} / nominal', color='green')
            ax_ratio.axhline(1, color='black', linestyle='--')
            ax_ratio.set_xlabel(f'{var}')
            ax_ratio.set_ylabel('Ratio')
            ax_ratio.legend()
        
        suffx_name = suffixs[1] if len(suffixs) >= 3 else suffixs[0]
        # plt.savefig(f"{output_folder}/{f_strip}_era_{var + suffx_name}_{btag}.png")
        plt.close(fig)
        for suffix in suffixs:
            save_hist_to_root(hist_data[var + suffix], bins, var + suffix,  f"{output_folder}/{f_strip}_era_{var + suffx_name}_{btag}.root")
            # save_hist_to_root(hist_data[var + suffix], bins, var + suffix,  f"{output_folder}/{f_strip}_era_{var + suffix}_{btag}.root")

        print(f"saved as {output_folder}/{f_strip}_era_{var + suffx_name}_{btag}")
    del tree
    gc.collect()
def main(folder_path, era, variables, suffixs, channel, btag):
    os.makedirs(f"{folder_path}_output", exist_ok=True)

    if era == "2022EE":
        lumi = 7.875e3
    elif era == "2022postEE":
        lumi = 26.337e3
    else:
        raise ValueError(f"Error: Year not found {era}")
    files=[]
    if "" not in suffixs:
        suffixs.insert(0, "")
    for filename in os.listdir(folder_path):
        # print(filename)
        if not  filename.endswith(".root"):
            continue
        # if not "DYto2Tau_MLL-4000to6000_TuneCP5_" in filename:
        #     continue
        files.append([folder_path, filename, era, copy.deepcopy(variables), suffixs, channel, btag, lumi])
    # print(files)

    files_final = []
    print(files_final)
    for f in files:
        # if "ZZ" not in f[1]:
            # continue
        for var in list(f[3]):  # Use list(f[3]) to make a copy for safe iteration
            if check_finished(f"{folder_path}_output", f[1], var, suffixs, btag):
                # print(f"finished running for {folder_path}_output", f[1], var, suffixs, btag)
                f[3].remove(var)  # Removing variables that have finished
        if  f[3]:
            print(f"file {f[1]} has unfinished jobs")
            # print(files_final)
            files_final.append(f)
    num_cores_to_use = 2  # Set the number of cores you want to use
    pool = Pool(processes=num_cores_to_use)
    max_jobs_per_iteration = 10  # Limit the number of jobs submitted at once
    max_jobs = 100
    print("About to run jobs for:", files_final)
    try:
        while files_final:
            jobs_submitted = 0  # Reset jobs submitted counter for each iteration
            for f in list(files_final):  # Use a copy of the list for safe iteration
                memory_usage = get_memory_usage()
                if memory_usage > 20.0 and jobs_submitted < max_jobs_per_iteration:
                    print(f"Memory usage is low ({memory_usage}%). Submitting job for {f[1]}.")
                    pool.apply_async(process_file, args=(f,))
                    files_final.remove(f)
                    jobs_submitted += 1
                    # time.sleep(1)  # Add a small delay between job submissions to prevent rapid submissions
                    # gc.collect()
                elif memory_usage <= 20.0:
                    print(f"Memory usage is high ({memory_usage}%). Waiting...")
                    break  # Exit the loop if memory usage is high

            if jobs_submitted == 0:
                time.sleep(60)  # Wait for 1 minute before checking again if no jobs were submitted

            # Re-check the memory usage to adjust dynamically
            while ((running_jobs := sum(1 for p in pool._pool if p.is_alive())) >= max_jobs):
                print(f"Running jobs ({running_jobs}) have reached the maximum limit. Waiting...")
                time.sleep(60)  # Adjust wait time as needed

    finally:
        pool.close()
        pool.join()
    print("finished all jobs")
    gc.collect()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot btag variables from ROOT files with weights.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing ROOT files')
    parser.add_argument('--shift', nargs='+', type=str, help='Shift to plot (e.g., __jesUncTotalUp)')
    parser.add_argument('--era', type=str, default='2022postEE', help='input era, 2022postEE or 2022EE')
    parser.add_argument('--channel', type=str, default='mt', help='decay channel, mt, et, tt, em')
    parser.add_argument('--btag', type=str, default='nob', help='btag selection, nob, btag')
    parser.add_argument('--PNN', type=int, default=1, help='run PNN score or mt_tot')
    args = parser.parse_args()
    bins = np.linspace(0, 1, 2001).tolist()  # 2001 points to get 2000 intervals
    # bins = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,2100.0,5000.0]

    # variables = [args.variables, args.variables + args.shift[0], args.variables + args.shift[1]]
    # mass = [60,  70, 80,  90,  100,  110,  120,     130,  140,  160,  180, 200,250] # 
    # mass = [65,75,85,95,105,115,125,135,]
    # PNN_vars= [f"PNN_{m}" for m in mass]
    PNN_vars = []
    PNN_vars.append("mt_tot")
    main(args.folder_path,args.era, PNN_vars, args.shift, args.channel, args.btag)
    