import uproot
import numpy as np
import pandas as pd
import ROOT
import yaml
import os
import sys
import argparse

def is_file_ok(file_path):
    # Attempt to open the file
    file = ROOT.TFile.Open(file_path, "READ")
    
    # Check if the file is open and healthy
    if file and not file.IsZombie() and file.TestBit(ROOT.TFile.kRecovered):
        print(f"Warning: File {file_path} was not properly closed but has been recovered.")
        file.Close()
        return False
    elif not file or file.IsZombie():
        print(f"Error: Cannot open file {file_path} or file is corrupted.")
        if file:
            file.Close()
        return False
    else:
        file.Close()
        return True

def get_array(era,param,input_data):
    # Open the ROOT file and get the histogram
    file = uproot.open(input_data)
    hist_name = f"PNN_{param}"
    histogram = file[hist_name]
    # Convert the histogram to numpy arrays
    values, bin_edges = histogram.to_numpy()
    if "Run_2022" in input_data:
        s_type = "Data"
    elif "TTto" in input_data:
        s_type = "ttbar"
    elif "2HDM" in input_data:
        if "Glu" in input_data:
            s_type = f"ggH_signal_{param}"    
        elif "bbH" in input_data:
            s_type = f"bbH_signal_{param}"
        else:
            sys.exit()     
    elif "FF" in input_data:
        s_type = "fakes"
    elif "DYto2Tau" in input_data:
        s_type = "Zto2Tau"
    elif "DYto2Mu" in input_data or "DYto2E" in input_data:
        s_type = "Zto2L"      
    elif "WZ" in input_data or "WW" in input_data  or "ZZ" in input_data:
        s_type = "diboson"
    else:
        s_type = "other"
    return values, s_type, bin_edges

def rebin_histogram(signal_mva, background_mva, Z_threshold=1):
    num = 2001
    # signal_hist, _ = np.histogram(signaTackground_mva, bins=np.linspace(0, 1, num=num))
    signal_hist = signal_mva
    background_hist = background_mva
    print(signal_hist)
    Ns = np.sum(signal_hist)
    Nb = np.sum(background_hist)

    def Z(k, l, l_original):
        ns = np.sum(signal_hist[k:l+1])
        nb = np.sum(background_hist[k:l+1])
        pb = 5
        ps = 8
        # if k > 0.5 * l_original:
        #     ps *= 2
        # if nb >=1 and ns/Ns> 0.01:
        #     # return ps * ns / Ns + pb * nb / Nb
        #     return ps * ns / Ns 
        # else:
        #     return 0
        return ps * ns / Ns 

    new_bins = [0]
    l = len(signal_hist) - 1
    l_original = l 
    count = len(signal_hist) 
    k = None
    while l > 0 and count > 0:
        if not k:
            k = l # initialise the fisrt value
        else:
            k = l-1
        count -= 1
        while k >= 0 and Z(k, l,l_original) <= Z_threshold:
            k -= 1
            # print("k, l,l_original, Z(k,l,l_original)", k, l,l_original, Z(k,l,l_original))
            # print( np.sum(signal_hist[k:l+1]) )
        
        new_bins.append(k )
        l = k
    new_bins.reverse()
    new_bins[-1] =num-1
    new_bins = [(x/(num-1))for x in new_bins]
    return new_bins


def save_histogram_to_root(histogram, bin_edges, name, root_file):
    # Create a ROOT histogram
    equal_bin = []
    for i in range (0,len(bin_edges) ):
        equal_bin.append(i)
    root_histogram = ROOT.TH1F(name, name, len(bin_edges) - 1, np.array(bin_edges, dtype=np.float64))
    
    # Fill the ROOT histogram with values
    for i, value in enumerate(histogram):
        root_histogram.SetBinContent(i + 1, value)
    
    # Write the histogram to the ROOT file
    root_file.WriteObject(root_histogram, name)
def main():
    ggH = True
    folder_path = "test_rebin/100"
    era = "2022postEE"
    param = "100"
    
    array_dic = {}    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        values, s_type, bin_edges = get_array(era, param, file_path)
        
        if s_type not in array_dic:
            array_dic[s_type] = values
        else:
            array_dic[s_type] += values

    bkg_array_sum = np.zeros_like(next(iter(array_dic.values())))
    for i in array_dic:
        if "Data" not in i and "signal" not in i:
            bkg_array_sum += array_dic[i]
    
    sig_array = array_dic[f"ggH_signal_{param}" if ggH else f"bbH_signal_{param}"]
    new_bins = rebin_histogram(sig_array, bkg_array_sum)
    # new_bins = [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.54, 0.58, 0.62, 0.66, 0.7 , 0.74, 0.78, 0.82, 0.86, 0.9, 0.905, 0.91 , 0.915, 0.92 , 0.925, 0.93 , 0.935, 0.94 ,
    #    0.945, 0.95 , 0.955, 0.96 , 0.965, 0.97 , 0.975, 0.98 , 0.985,
    #    0.99 , 0.995, 1.  ]
    print(new_bins)
    
    output_root_file = ROOT.TFile("rebinned_histograms.root", "RECREATE")
    for i in array_dic:
        rebinned_values, _ = np.histogram(bin_edges[:-1], bins=new_bins, weights=array_dic[i])
        save_histogram_to_root(rebinned_values, new_bins, i, output_root_file)
   
    output_root_file.Close()

   
if __name__ == "__main__":
        

    # param = int(sys.argv[1])
    # # channel = str(sys.argv[2])
    # # era = str(sys.argv[3])
    # # tag = str(sys.argv[4])
    # parser = argparse.ArgumentParser(description='Plot btag variables from ROOT files with weights.')
    # parser.add_argument('folder_path', type=str, help='Path to the folder containing ROOT files')
    # parser.add_argument('--shift', nargs='+', type=str, help='Shift to plot (e.g., __jesUncTotalUp)')
    # args = parser.parse_args()
    main()
