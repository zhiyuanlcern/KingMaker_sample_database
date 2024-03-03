import uproot
import numpy as np
import pandas as pd
import ROOT
import yaml
import os
import sys




param = int(sys.argv[1])
channel = str(sys.argv[2])
era = str(sys.argv[3])


weight_dict = {
    "tt": ["Xsec", "puweight", "genWeight", "genEventSumW", "btag_weight", "FF_weight","id_wgt_tau_vsJet_Medium_2","id_wgt_tau_vsJet_Medium_1","trg_wgt_ditau_crosstau_1","trg_wgt_ditau_crosstau_2"],
    "mt": ["Xsec", "puweight", "genWeight", "genEventSumW", "btag_weight", "FF_weight","id_wgt_tau_vsJet_Medium_2","iso_wgt_mu_1","trg_wgt_ditau_crosstau_2"],
    "et": ["Xsec", "puweight", "genWeight", "genEventSumW", "btag_weight", "FF_weight","id_wgt_tau_vsJet_Medium_2","id_wgt_ele_wpTight",], #"trg_cross_ele24tau30_hps", "trg_wgt_ditau_crosstau_2"
}
weight_list = weight_dict[channel]

sig_file = f"GluGluHto2Tau_M-{param}_2HDM-II_TuneCP5_13p6TeV_powheg-pythia8_Run3Summer22NanoAODv12_{channel}.root{param}"
bkg_file_list = [f"diboson.root{param}",f"DYto2L.root{param}"]#,f"DYto2Tau.root{param}",f"FF_Combined.root{param}",f"Hto2B.root{param}",f"Hto2Tau.root{param}",f"Wjets.root{param}",] #f"Top.root{param}",
data_file_list = [f"Data.root{param}"]

samples_name = "sample_database/datasets.yaml" 
with open(samples_name, "r") as file:
    samples_list =  yaml.safe_load(file)

def get_branch(input_file, param):
    file = uproot.open(input_file)["ntuple"]
    branch_names = file.keys()

    pnn_branches = [name for name in branch_names if f"pnn_{param}" in name]
    # print(pnn_branches)
    return pnn_branches
def get_weight_branch(input_file, weight):
    file = uproot.open(input_file)["ntuple"]
    branch_names = file.keys()

    weight_branches = [name for name in branch_names if f"{weight}" in name]
    # print(pnn_branches)
    return weight_branches

def get_data_array(era,param,input_data):
    bkg, sig, bkg_array, data_array, signal_hist, bin_edges, background_hist,bkg_weight_array,sig_weight_array= {},{}, {},{}, {},{},{},{},{}
    data = uproot.open(f"{input_data}")["ntuple"]
    data_array_list = {}
    data_array = data.arrays(f"pnn_{param}", library="pd")
    data_neg_idx = np.where(data_array<0)
    data_array = data_array.drop(data_neg_idx[0])
    data_array = np.arctanh((data_array -0.5 )*1.9999999)

    # if era == "2022EE":
    #     lumi = 7.875e3
    # else:
    #     lumi = 26.337e3
    # for i in weight_list:
    #     data_array_list[i] = data.arrays(i, library="pd").drop(data_neg_idx[0])
    data_weight = np.ones(len(data_array))
    # for i in weight_list:
    #     if i != "genEventSumW":
    #         data_weight = data_weight*data_array_list[i].iloc[:,0].values
    data_weight_array = pd.DataFrame(data_weight,columns=["Limit_Weight"])
    
    s_type = "Data"
    return data_array, data_weight_array, s_type


def get_sig_array(era,param,input_sig):
    bkg, sig, bkg_array, sig_array, signal_hist, bin_edges, background_hist,bkg_weight_array,sig_weight_array= {},{}, {},{}, {},{},{},{},{}
    pnn_branches = get_branch(input_sig,param)
    pnn_array_list = {}
    sig_weight_array_list = {}
    # Get nominal and systematic weight
    weight_array_list = {}
    trainweight_array_list = {}
    sig = uproot.open(f"{input_sig}")["ntuple"]
    for pnn_item in pnn_branches:
        sig_array_list = {}
        pnn_array_list[pnn_item] = sig.arrays(pnn_item, library="pd")
        sig_neg_idx = np.where(pnn_array_list[pnn_item]<0)
        pnn_array_list[pnn_item] = pnn_array_list[pnn_item].drop(sig_neg_idx[0])
        pnn_array_list[pnn_item] = np.arctanh((pnn_array_list[pnn_item] -0.5 )*1.9999999)
        if era == "2022EE":
            lumi = 7.875e3
        else:
            lumi = 26.337e3
        for i in weight_list:
            sig_array_list[i] = sig.arrays(i, library="pd").drop(sig_neg_idx[0])
        sig_weight = lumi/sig_array_list["genEventSumW"].iloc[:,0].values
        for i in weight_list:
            if i != "genEventSumW":
                sig_weight = sig_weight*sig_array_list[i].iloc[:,0].values
        sig_weight_array = pd.DataFrame(sig_weight,columns=["Limit_Weight"])
        sig_weight_array_list[pnn_item] = sig_weight_array
    
    sig_array = sig.arrays(f"pnn_{param}", library="pd")

    nominal_neg_idx = np.where(sig_array< 0)
    for weight in weight_list:
        if weight != "Xsec" and weight != "genWeight" and weight != "genEventSumW":
            weight_branches = get_weight_branch(input_sig,weight)
            for weight_item in weight_branches:
                sig_array_list = {}
                weight_array_list[weight_item] = sig.arrays(weight_item, library="pd")
                weight_array_list[weight_item] = weight_array_list[weight_item].drop(nominal_neg_idx[0])
                if era == "2022EE":
                    lumi = 7.875e3
                else:
                    lumi = 26.337e3
                for i in weight_list:
                    sig_array_list[i] = sig.arrays(i, library="pd").drop(nominal_neg_idx[0])
                sig_weight = lumi/sig_array_list["genEventSumW"].iloc[:,0].values
                for i in weight_list:
                    if i != "genEventSumW" and i not in weight_item:
                        sig_weight = sig_weight*sig_array_list[i].iloc[:,0].values
                sig_weight = sig_weight*weight_array_list[weight_item].iloc[:,0].values
                sig_weight_array = pd.DataFrame(sig_weight,columns=[f"Limit_Weight_{weight_item}"])
                trainweight_array_list[weight_item] = sig_weight_array

    # print(bkg_neg_idx)
    # sig_array = sig_array.drop(sig_neg_idx[0])
    # sig_array = np.arctanh((sig_array -0.5 )*1.9999999) 
    s_type = "BSM_" + str(param)
    return pnn_array_list, sig_weight_array_list, s_type, trainweight_array_list

def get_bkg_array(era,param,input_bkg):
    s_type = "None"
    nick = "None"
    for n in samples_list:
        if n in input_bkg:
            s_type = samples_list[n]['sample_type']
            nick = samples_list[n]['nick']
    # print(nick,":",s_type)
    if s_type == "None":
        raise ValueError("Error: not found the file {}".format(input_bkg))

    bkg, sig, bkg_array, sig_array, signal_hist, bin_edges, background_hist,bkg_weight_array,sig_weight_array= {},{}, {},{}, {},{},{},{},{}
    
    pnn_branches = get_branch(input_bkg,param)
    pnn_array_list = {}
    bkg_weight_array_list = {}
   
    weight_array_list = {}
    trainweight_array_list = {}
    bkg = uproot.open(f"{input_bkg}")["ntuple"]
    for pnn_item in pnn_branches:
        bkg_array_list = {}
        pnn_array_list[pnn_item] = bkg.arrays(pnn_item, library="pd")
        bkg_neg_idx = np.where(pnn_array_list[pnn_item]<0)
        pnn_array_list[pnn_item] = pnn_array_list[pnn_item].drop(bkg_neg_idx[0])
        pnn_array_list[pnn_item] = np.arctanh((pnn_array_list[pnn_item] -0.5 )*1.9999999)
        if era == "2022EE":
            lumi = 7.875e3
        else:
            lumi = 26.337e3
        for i in weight_list:
            bkg_array_list[i] = bkg.arrays(i, library="pd").drop(bkg_neg_idx[0])
        bkg_weight = lumi/bkg_array_list["genEventSumW"].iloc[:,0].values
        for i in weight_list:
            if i != "genEventSumW":
                bkg_weight = bkg_weight*bkg_array_list[i].iloc[:,0].values
        bkg_weight_array = pd.DataFrame(bkg_weight,columns=["Limit_Weight"])
        bkg_weight_array_list[pnn_item] = bkg_weight_array
    bkg_array = bkg.arrays(f"pnn_{param}", library="pd")

    nominal_neg_idx = np.where(bkg_array < 0)

    for weight in weight_list:
        if weight != "Xsec" and weight != "genWeight" and weight != "genEventSumW":
            weight_branches = get_weight_branch(input_bkg,weight)
            for weight_item in weight_branches:
                sig_array_list = {}
                weight_array_list[weight_item] = bkg.arrays(weight_item, library="pd")
                weight_array_list[weight_item] = weight_array_list[weight_item].drop(nominal_neg_idx[0])
                if era == "2022EE":
                    lumi = 7.875e3
                else:
                    lumi = 26.337e3   
                for i in weight_list:
                    sig_array_list[i] = bkg.arrays(i, library="pd").drop(nominal_neg_idx[0])
                sig_weight = lumi/sig_array_list["genEventSumW"].iloc[:,0].values
                for i in weight_list:
                    if i != "genEventSumW" and i not in weight_item:
                        sig_weight = sig_weight*sig_array_list[i].iloc[:,0].values
                sig_weight = sig_weight*weight_array_list[weight_item].iloc[:,0].values
                sig_weight_array = pd.DataFrame(sig_weight,columns=[f"Limit_Weight_{weight_item}"])
                trainweight_array_list[weight_item] = sig_weight_array                

    return pnn_array_list, bkg_weight_array_list, s_type,pnn_branches, trainweight_array_list

def rebin_histogram(signal_mva, background_mva, signal_weight, background_weight, Z_threshold=0.5):
    num = 5001
    # low, high  = np.min(overall), np.max(overall)
    high =max(background_mva.max().max(), signal_mva.max().max())
    low =min(background_mva.min().min(), signal_mva.min().min())
    print(low, high)
    signal_hist, _ = np.histogram(signal_mva, bins=np.linspace(low, high, num=num),weights = signal_weight)
    background_hist, _ = np.histogram(background_mva, bins=np.linspace(low, high, num=num),weights = background_weight)

    Ns = np.sum(signal_hist)
    Nb = np.sum(background_hist)
    # print(Ns, Nb)

    def Z(k, l):
        ns = np.sum(signal_hist[k:l+1])
        nb = np.sum(background_hist[k:l+1])
        if nb + ns >=1:
            return 10 * ns / Ns + 5 * nb / Nb
        else:
            return 0

    new_bins = [0]
    l = len(signal_hist) - 1
    count = len(signal_hist) 
    k = None
    while l > 0 and count > 0:
        if not k:
            k = l # initialise the fisrt value
        else:
            k = l-1
        count -= 1
        while k >= 0 and Z(k, l) <= Z_threshold:
            k -= 1
        
        new_bins.append(k )
        l = k
    new_bins.reverse()
    new_bins[-1] =num-1
    new_bins = [(x/(num-1) *(high -low)  + low )for x in new_bins]
    return new_bins

def save_root(signal_mva, signal_weight, new_bins, s_type, param,pnn_item):
    # if "BSM" in s_type:
    #     print(f"{s_type}{pnn_item}")
    root_filename = f"histograms_{param}_check_2.root"
    signal_hist, bin_edges = np.histogram(signal_mva, bins=new_bins, weights=signal_weight)

    signal_hist = np.where(signal_hist < 0, 0, signal_hist)

    n_bins = len(bin_edges) - 1
    if os.path.exists(root_filename):
        root_file = ROOT.TFile(root_filename, "UPDATE")
    else:
        root_file = ROOT.TFile(root_filename, "RECREATE")

    signal_root_hist = ROOT.TH1F(f"{s_type}{pnn_item}", f"{s_type} Distribution", n_bins, bin_edges)

    for i in range(n_bins):
    # SetBinContent takes bin index starting from 1, and the bin content value
        signal_root_hist.SetBinContent(i+1, signal_hist[i])
    signal_root_hist.GetXaxis().SetTitle("pnn_100_rebin")
    signal_root_hist.GetYaxis().SetTitle("N")

    # Write the histograms to the file
    signal_root_hist.Write()

    # Close the ROOT file
    root_file.Close()


def main():
    type_list = []

    bkg_array_sum  = {}
    bkg_array_sum["sum"] = pd.DataFrame()
    bkg_weight_array_sum = {}
    bkg_weight_array_sum["sum"] = pd.DataFrame()
    bkg_trainweight_array_list = {}

    data_array_sum = pd.DataFrame()
    data_weight_array_sum = pd.DataFrame()
    for data_file in data_file_list:
        data_array, data_weight_array, data_s_type = get_data_array(era,param,data_file)
        data_array_sum = pd.concat([data_array_sum,data_array],axis=0)
        data_weight_array_sum = pd.concat([data_weight_array_sum,data_weight_array],axis=0)
    
    sig_array, sig_weight_array,sig_s_type,sig_trainweight_array_list = get_sig_array(era,param,sig_file)
    for bkg_file in bkg_file_list:
        bkg_array, bkg_weight_array, s_type, pnn_branches, trainweight_array_list = get_bkg_array(era,param,bkg_file)
        # print(s_type,trainweight_array_list)
        if s_type not in type_list:
            type_list.append(s_type)
        bkg_array_sum["sum"] = pd.concat([bkg_array_sum["sum"], bkg_array[f"pnn_{param}"]],axis=0)
        # print(bkg_weight_array_sum["sum"])
        # print(bkg_weight_array)
        bkg_weight_array_sum["sum"] = pd.concat([bkg_weight_array_sum["sum"],bkg_weight_array[f"pnn_{param}"]],axis=0)
        for pnn_item in pnn_branches:
            if (s_type + pnn_item) not in bkg_array_sum:
                bkg_array_sum[s_type + pnn_item] = pd.DataFrame()
                bkg_array_sum[s_type + pnn_item] = pd.concat([bkg_array_sum[s_type + pnn_item],bkg_array[pnn_item]],axis=0)
            else:
                bkg_array_sum[s_type + pnn_item] = pd.concat([bkg_array_sum[s_type + pnn_item],bkg_array[pnn_item]],axis=0)
        for pnn_item in pnn_branches:
            if (s_type + pnn_item) not in bkg_weight_array_sum:
                bkg_weight_array_sum[s_type + pnn_item] = pd.DataFrame()
                bkg_weight_array_sum[s_type + pnn_item] = pd.concat([bkg_weight_array_sum[s_type + pnn_item],bkg_weight_array[pnn_item]],axis=0)
            else:
                bkg_weight_array_sum[s_type + pnn_item] = pd.concat([bkg_weight_array_sum[s_type + pnn_item],bkg_weight_array[pnn_item]],axis=0)
        for train_weight in trainweight_array_list:
            if s_type+train_weight not in bkg_trainweight_array_list:
                bkg_trainweight_array_list[s_type+train_weight] = pd.DataFrame()
                bkg_trainweight_array_list[s_type+train_weight] = pd.concat([bkg_trainweight_array_list[s_type+train_weight],trainweight_array_list[train_weight]],axis=0)
            else:
                bkg_trainweight_array_list[s_type+train_weight] = pd.concat([bkg_trainweight_array_list[s_type+train_weight],trainweight_array_list[train_weight]],axis=0)

    new_bins = rebin_histogram(sig_array[f"pnn_{param}"],bkg_array_sum["sum"],sig_weight_array[f"pnn_{param}"],bkg_weight_array_sum["sum"],0.5)
    for s_type in bkg_array_sum:
        bkg_array_sum[s_type] = bkg_array_sum[s_type].reset_index(drop=True)
    for s_type in bkg_weight_array_sum:
        bkg_weight_array_sum[s_type] = bkg_weight_array_sum[s_type].reset_index(drop=True)

    # print(new_bins)
    # print(bkg_array_sum)
    # print(bkg_weight_array_sum)

    # Save signal file
    save_root(data_array_sum, data_weight_array_sum,new_bins,data_s_type,param,pnn_item="")

    for item in sig_array:
        # print(item)
        save_root(sig_array[item], sig_weight_array[item],new_bins,sig_s_type,param,pnn_item=str(item))
    for item in sig_trainweight_array_list:
        save_root(sig_array[f'pnn_{param}'], sig_trainweight_array_list[item],new_bins,sig_s_type,param,pnn_item=str(item))
    for s_type in type_list:
        for pnn_item in pnn_branches:
            save_root(bkg_array_sum[s_type + pnn_item],bkg_weight_array_sum[s_type + pnn_item],new_bins,s_type,param,pnn_item)
        for train_weight in trainweight_array_list:
            save_root(bkg_array_sum[s_type + f'pnn_{param}'],bkg_trainweight_array_list[s_type+train_weight],new_bins,s_type,param,train_weight)

if __name__ == "__main__":
    main()
