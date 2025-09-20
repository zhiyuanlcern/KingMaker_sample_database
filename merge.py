import ROOT
import os
import sys
from array import array
import argparse
import concurrent.futures
import re
import numpy as np
ROOT.TH1.SetDefaultSumw2(True)


def hist_to_numpy(hist):
    nbins = hist.GetNbinsX()
    bin_contents = np.array([hist.GetBinContent(i) for i in range(1, nbins + 1)])
    return bin_contents


def rebin_histogram_PNN(signal_mva, background_mva, signal_hist_original, Z_threshold=1):
    # signal_hist, _ = np.histogram(signaTackground_mva, bins=np.linspace(0, 1, num=num))

    
    signal_hist = signal_mva
    background_hist = background_mva
    num = len(signal_hist) 
    print("length of the array",num)
    Ns = np.sum(signal_hist)
    Nb = np.sum(background_hist)
    print("signal_hist, Ns", signal_hist, Ns)
    print("background_hist, Nb", background_hist, Nb)
    def Z(k, l, l_original):
        ns = np.sum(signal_hist[k:l+1])
        nb = np.sum(background_hist[k:l+1])
        
        # pb = 20
        ps = 25
        # if Ns < 12.5:
        #     ps = min((round(Ns/0.2) + 1), 25) 
        #     # ps = max(ps, 25)
        #     # ps =max(ps, 10)
        if nb >=1 :
            
            return  ps * ns/Ns
        else:
            return 0

    new_bins = [num]
    l = len(signal_hist) 
    l_original = l 
    count = len(signal_hist) 
    # print(count)
    k = None
    nb = 0
    while l > 0 and count > 0:
        if not k:
            k = l # initialise the fisrt value
        else:
            k = l-1
        count -= 1
        while k >= 0 and (Z(k, l,l_original) <= Z_threshold or np.sum(background_hist[k:l+1]) < 0.5 * nb)  :
            k -= 1
            # print("k, l,l_original, Z(k,l,l_original)", k, l,l_original, Z(k,l,l_original))
            # print( np.sum(signal_hist[k:l+1]) )
        ## now the Z requirement is met, we need to satisfy signal MC stats error requirement
        signal_mc_err = 0
        for i in range(k, l+2):
            signal_mc_err += signal_hist_original.GetBinError(i) **2
        signal_mc_err = signal_mc_err ** 0.5
        print(signal_mc_err)
        ns = np.sum(signal_hist[k:l+1])
        while ns <= 0 or  signal_mc_err/ns >= 0.5:
            k-=1
            if k < 0: 
                break
            ns = np.sum(signal_hist[k:l+1])
            signal_mc_err = signal_hist_original.GetBinError(k) **2 +  signal_mc_err ** 2
            signal_mc_err = signal_mc_err ** 0.5


        nb = np.sum(background_hist[k:l+1])
        print("background yield",nb, k, l+ 1)
        print("ns =",  np.sum(signal_hist[k:l+1]) ,"nb = ",  np.sum(background_hist[k:l+1]))
        new_bins.append(k -1 )
        l = k-1
    new_bins.reverse()
    new_bins[0] = 0
    new_bins = [(x/(num-1))for x in new_bins]
    print(new_bins)
    return new_bins




def fast_walk_and_filter(directory, extension=".root", var="mt_tot", must_have=""):
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            yield from fast_walk_and_filter(entry.path, extension, var)
        elif entry.is_file():
            if entry.name.endswith(extension) and var in entry.name and must_have in entry.name:
                yield entry.path



def classify_file(filename):
    if filename.startswith("Muon") or filename.startswith("Tau") or filename.startswith("EGamma") or filename.startswith("DoubleMuon") or filename.startswith("SingleMuon"):  
        return "data_obs"
    elif "2HDM" in filename or "BBHto2Tau" in filename:
        match = re.search(r'Hto2Tau_M-(\d+)', filename)
        if match:
            masses_check = [int(match.group(1))]
            m = masses_check[0]
        if "Glu" in filename:
            return f"ggH_signal_{m}"
        elif "bbH" in filename or "BBH" in filename:
            return f"bbH_signal_{m}"
        else:
            sys.exit()
    elif filename.startswith("DYto2L"):
        return "Zto2L"
    elif filename.startswith("FF_Combined"):
        return "fakes"
    elif filename.startswith("TTtoLNu2Q") or filename.startswith("TTto2L2Nu") or filename.startswith("TTto4Q") or filename.startswith("TBbarQ_t") or filename.startswith("TbarBQ_t") or filename.startswith("TbarWplus") or filename.startswith("TWminus"):  
        return "ttbar"
    elif filename.startswith("WZto") or filename.startswith("ZZto") or filename.startswith("WWto"):
        return "diboson"
    elif filename.startswith("WtoLNu") or filename.startswith("GluGluHto2Tau_M-125_TuneCP5_13p6TeV_amcatnloFXFX") or filename.startswith("GluGluHToTauTau_M-125_TuneCP5_13p6TeV_powheg") or filename.startswith("VBFH"):
        return "other"
    else:
        print("filename",  filename)
        return "other"

def extract_variables(filename, era):
    # Remove the .root extension
    filename = filename.replace('.root', '')
    # Split by '_era_'
    parts = filename.split(f'_{era}_')
    # print(parts)
    # Extract f_strip
    f_strip = parts[0]
    # Split the remaining part by the last '_'
    print(parts)
    print("=============")
    remaining_parts = parts[1]
    if "nob" not in remaining_parts and "btag" not in remaining_parts:
        remaining_parts = parts[2]
    ## remaing_parts: nob_mt_tot
    print("remaining_parts =============== ", remaining_parts)
    if remaining_parts.startswith("nob"):
        var_suffix = remaining_parts.split("_")[1] + "_" + remaining_parts.split("_")[2]
    if remaining_parts.startswith("btag"):
        var_suffix = remaining_parts[5:]
    # Extract var + suffixs[1]
    # print(remaining_parts)
    # Extract btag
    btag = remaining_parts.split("_")[0]
    if "__" in filename:
        # Further split var_suffix to extract var and syst
        var, syst = var_suffix.split('__', 1)   
    else:
        var = var_suffix
        syst = ''
    # print(f_strip, var, syst, btag)
    return f_strip, var, syst, btag
def rebin_histogram(hist, new_bins):
    # Create a new histogram with the specified binning
    new_hist_name = hist.GetName() 
    new_hist = ROOT.TH1F(new_hist_name, hist.GetTitle(), len(new_bins) - 1, array('d', new_bins))
    
    # Fill the new histogram with the contents of the original histogram
    for bin in range(1, hist.GetNbinsX() + 1):
        content = hist.GetBinContent(bin)
        error = hist.GetBinError(bin)
        x = hist.GetBinCenter(bin)
        new_bin = new_hist.FindBin(x)
        new_hist.SetBinContent(new_bin, new_hist.GetBinContent(new_bin) + content)
        new_hist.SetBinError(new_bin, (new_hist.GetBinError(new_bin)**2 + error**2)**0.5)
    
    return new_hist
def get_latest_histograms(file):
    latest_hists = {}
    for key in file.GetListOfKeys():
        hist_name = key.GetName()
        cycle_number = key.GetCycle()  # Get the cycle number
        base_name = hist_name.split(';')[0]
        if base_name not in latest_hists or cycle_number > latest_hists[base_name][1]:
            latest_hists[base_name] = (hist_name, cycle_number)
    
    return latest_hists


def process_file(input_file, histograms_by_type, processed_processes, era, nom_only):
    # print(input_file)
    file = os.path.basename(input_file)
    physics_process, variable, syst, region = extract_variables(file, era)
    if not physics_process:
        return
    
    # if "Run2022" not in physics_process and ("DY" not in physics_process):
    #     return
    s_type = classify_file(physics_process)

    if s_type not in histograms_by_type:
        histograms_by_type[s_type] = {}
    if region not in histograms_by_type[s_type]:
        histograms_by_type[s_type][region] = {}
    if variable not in histograms_by_type[s_type][region]:
        histograms_by_type[s_type][region][variable] = {}
    try:
        fin = ROOT.TFile(input_file, "READ")
    except:
        print(f"ERROR: cannot open file", input_file)
        return

    # Mark the physics process as processed
    # Get the latest histograms
    latest_histograms = get_latest_histograms(fin)
    # print(latest_histograms)
    # Print the names and histograms
    for base_name, (hist_name, cycle_number) in latest_histograms.items():
        if nom_only:
            if "__" in hist_name:
                continue
        try:
            hist = fin.Get(f"{hist_name};{cycle_number}")  # Use the cycle number to get the specific version
        except:
            print(new_hist_name, "cannot be retrieved", s_type, region, variable)
            print(input_file)
            print(fin)
            print(hist)
            continue
        
        if s_type == "fakes":
            for ibins in range(0, hist.GetNbinsX()+1):
                hist.SetBinError(ibins, 0)
        new_hist_name = f"{s_type}_{hist_name}"
        # print("new_hist_name",new_hist_name)
        # print("histograms_by_type", histograms_by_type)
        # print(input_file)
        # Check if histogram is already in the dictionary
        if new_hist_name not in histograms_by_type[s_type][region][variable]:
            try:
                histograms_by_type[s_type][region][variable][new_hist_name] = hist.Clone()
                histograms_by_type[s_type][region][variable][new_hist_name].SetDirectory(0)  # Detach from input file
            except:
                print(new_hist_name, "cannot be retrieved", s_type, region, variable)
                print("problematic file:", input_file)
                print(fin)
                print(hist)
        else:
            if "__" in new_hist_name:
                ## systematics    
                if not hist:
                    print("problematic file:", input_file)
                    print(fin)
                    print(hist)
                    continue
                histograms_by_type[s_type][region][variable][new_hist_name].Add(hist)
                histograms_by_type[s_type][region][variable][new_hist_name].SetDirectory(0)
            else:
                ## nominal histograms
                if not (physics_process, variable, region) in processed_processes:
                    if not hist:
                        print("problematic file:", input_file)
                        print(fin)
                        print(hist)
                        continue
                    ## for nominal hist, only sum the different processes
                    histograms_by_type[s_type][region][variable][new_hist_name].Add(hist)
                    histograms_by_type[s_type][region][variable][new_hist_name].SetDirectory(0)
    
    if (physics_process, variable, region) not in processed_processes:
        ## mark processed for 1 physics process 
        processed_processes.add((physics_process, variable, region))
        

    fin.Close()

def merge_systematics_by_type(input_dir, output_dir, var, era, signal, nom_only):
    # Dictionary to store histograms by type, variable, and region
    print("start processing")
    histograms_by_type = {}
    processed_processes = set()
    
    input_files = list(fast_walk_and_filter(input_dir, ".root", var))  # Convert generator to list
    print(f"lenght of input files: {len(input_files)}")
    # Adjust the number of workers based on your system's capability
    num_workers = min(4, len(input_files))  # Example: use 32 workers or the number of files, whichever is smaller
    for f in input_files:
        process_file(f, histograms_by_type, processed_processes,  era, nom_only)

    fout = ROOT.TFile(output_dir, "RECREATE")
    print("creating output file")
    print(var)

    region_list=["nob1", "nob2", "nob3", "nob4", "nob5", "btag"] if var != "mt_tot" else ["nob",  "btag"]
    # Create the directories "nob" and "btag"
    for r in region_list:
        fout.mkdir(r)
    
    new_bin_edges= {}
    # Loop over the histograms and save them in the corresponding directories
    # in this step, rebinning algorithm is used
    if "PNN" in var:
        mass = var[4:] 
        for r in region_list:
            print(histograms_by_type[f"{signal}_signal_{mass}"])
            # print( histograms_by_type[f"{signal}_signal_{mass}"][f"nob{index}"][var])
            h_sig = histograms_by_type[f"{signal}_signal_{mass}"][f"{r}"][var][f"{signal}_signal_{mass}_{var}"] 
            
            h_bkg = histograms_by_type[f"Zto2L"][f"{r}"][var][f"Zto2L_{var}"].Clone()
            h_bkg.Add(histograms_by_type[f"ttbar"][f"{r}"][var][f"ttbar_{var}"])
            h_bkg.Add(histograms_by_type[f"diboson"][f"{r}"][var][f"diboson_{var}"])
            h_bkg.Add(histograms_by_type[f"other"][f"{r}"][var][f"other_{var}"])
            try:
                h_bkg.Add(histograms_by_type[f"fakes"][f"{r}"][var][f"fakes_{var}"])
            except:
                pass
            signal_mva = hist_to_numpy(h_sig)
            background_mva = hist_to_numpy(h_bkg)
            # Use the rebin function to get the new bin edges
            new_bins = rebin_histogram_PNN(signal_mva, background_mva,h_sig)
            print(new_bins)
            new_bin_edges[r] = np.array(new_bins)
        
        
    for s_type, regions in histograms_by_type.items():
        print( "s_type, regions", s_type, regions)
        for region, variables in regions.items():
            # Change to the correct directory based on the region
            fout.cd()
            fout.cd(region)
            
            
            for variable, hists in variables.items():
                for hist_name, hist in hists.items():
                    final_hist_name = hist_name.replace(f"_{variable}", "")
                    if "__" in final_hist_name:
                        if final_hist_name.endswith("up"):
                            final_hist_name = final_hist_name[:-2] + "Up"
                        if final_hist_name.endswith("down"):
                            final_hist_name = final_hist_name[:-4] + "Down"
                    hist.SetName(final_hist_name)
                    if "PNN" in hist_name:
                        new_bins=new_bin_edges[region]
                        
                        rebinned_hist = rebin_histogram(hist, new_bins)
                        rebinned_hist.SetName(final_hist_name)
                        rebinned_hist.Write()
                    else:
                        hist.SetName(final_hist_name)
                        hist.Write()                    

    fout.cd()
    if nom_only:
        fout.Close()
        print("finish filling output file, nominal only")
        return 0



    fout.Close()



    print("finish filling output file")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot btag variables from ROOT files with weights.')
    parser.add_argument('--input_dir', type=str, help='Shift to plot (e.g., __jesUncTotalUp)')
    parser.add_argument('--var', type=str, default='mt_tot', help='variable to save')
    parser.add_argument('--era', type=str, default='2022postEE', help='era')
    parser.add_argument('--signal', type=str, default='ggH', help='signal type to run for ')
    parser.add_argument('--nom_only', type=int, default=0, help='remove systematics or not ')
    args = parser.parse_args()

    
    # Directory containing input ROOT files
    input_dir = args.input_dir
    # Output ROOT file
    # mv ${era}_${channel}_Version10_nominal_fix_jetveto_output_${v}_ggH.root  ${era}_${channel}_Version10_nominal_output_${v}_ggH_signal_.root 
    output_file = f"{args.input_dir}_{args.var}_{args.signal}_signal_.root".replace("_fix_jetveto", "")
    # Merge systematics by type
    print(f"working on file: {output_file} ")
    merge_systematics_by_type(input_dir, output_file, args.var, args.era, args.signal, args.nom_only)
    
