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
    remaining_parts = parts[1]
    ## remaing_parts: nob_mt_tot
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

def get_bins_from_file(era, channel, var, btag, signal_type):
    import ast
    BINNING_DIR = "/data/bond/zhiyuanl/Plotting/fitting_template_Version11/bin_edges/"
    filename = f"{era}_{channel}_Version11_nominal_output_{var}_{signal_type}{btag}_bin_edges.txt"
    # print("filename:",filename)
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

def process_file(input_file, histograms_by_type, processed_processes, era, nom_only, signal_type):
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
        

        # if hist.GetNbinsX() >= 1000: ## this needs to rebin
        #     new_bins = get_bins_from_file(era, channel, variable, region, signal_type)
        #     hist = rebin_histogram(hist, new_bins)

        if s_type == "fakes":
            for ibins in range(0, hist.GetNbinsX()+1):
                hist.SetBinError(ibins, 0)
        new_hist_name = f"{s_type}_{hist_name}"
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

    if "_mt_Version" in input_dir:
        channel='mt'
    elif "_et_Version" in input_dir:
        channel='et'
    elif "_tt_Version" in input_dir:
        channel='tt'
    elif "_em_Version" in input_dir:
        channel='em'
    else:
        print("wrong input name provided")
        sys.exit(-1)
    input_files = list(fast_walk_and_filter(input_dir, ".root", var))  # Convert generator to list
    print(f"lenght of input files: {len(input_files)}")
    # Adjust the number of workers based on your system's capability
    num_workers = min(4, len(input_files))  # Example: use 32 workers or the number of files, whichever is smaller
    for f in input_files:
        process_file(f, histograms_by_type, processed_processes, era, nom_only, signal)

    fout = ROOT.TFile(output_dir, "RECREATE")
    print("creating output file")

    # Create the directories "nob" and "btag"
    if var == "mt_tot":
        fout.mkdir("nob")
    else:
        fout.mkdir("nob1")
        fout.mkdir("nob2")
        fout.mkdir("nob3")
        fout.mkdir("nob4")
    fout.mkdir("btag")

 
    # Loop over the histograms and save them in the corresponding directories
    if "PNN" in var:
        mass = var[4:] 
        for index in range(1,5):
            print(histograms_by_type[f"{signal}_signal_{mass}"])
            # print( histograms_by_type[f"{signal}_signal_{mass}"][f"nob{index}"][var])
            h_sig_nob = histograms_by_type[f"{signal}_signal_{mass}"][f"nob{index}"][var][f"{signal}_signal_{mass}_{var}"] 
            try:
                h_bkg = histograms_by_type[f"Zto2L"][f"nob{index}"][var][f"Zto2L_{var}"].Clone()
                h_bkg.Add(histograms_by_type[f"fakes"][f"nob{index}"][var][f"fakes_{var}"])
            except:
                h_bkg = histograms_by_type[f"Zto2L"][f"nob{index}"][var][f"Zto2L_{var}"].Clone()
  
        h_sig_btag = histograms_by_type[f"{signal}_signal_{mass}"]["btag"][var][f"{signal}_signal_{mass}_{var}"] 
        try:
            h_bkg_btag = histograms_by_type[f"Zto2L"]["btag"][var][f"Zto2L_{var}"].Clone()
            h_bkg_btag.Add(histograms_by_type[f"fakes"]["btag"][var][f"fakes_{var}"]).Clone()
        except:
            h_bkg_btag = histograms_by_type[f"Zto2L"]["btag"][var][f"Zto2L_{var}"]
       

    for s_type, regions in histograms_by_type.items():
        print( "s_type, regions", s_type, regions)
        for region, variables in regions.items():
            # Change to the correct directory based on the region
            if "nob" in region:
                fout.cd()
                fout.cd(region)
            elif region == "btag":
                fout.cd()
                fout.cd("btag")
            else:
                continue  # Skip if the region is not recognized
            
            for variable, hists in variables.items():
                if variable != "mt_tot":
                    new_bins = get_bins_from_file(era, channel, variable, region, signal)
                
                for hist_name, hist in hists.items():
                    final_hist_name = hist_name.replace(f"_{variable}", "")
                    
                    if "__" in final_hist_name:
                        if "nob" in region:
                            if "FF_tot_Stat" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_tot_Stat", "FF_tot_Stat1")
                            if "FF_ttbar" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_ttbar", "FF_ttbar1")
                            if "FF_wjets" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_wjets", "FF_wjets1")
                            if "FF_closure" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_closure", "FF_closure1")
                        if region == "btag":
                            if "FF_tot_Stat" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_tot_Stat", "FF_tot_Stat2")
                            if "FF_ttbar" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_ttbar", "FF_ttbar2")
                            if "FF_wjets" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_wjets", "FF_wjets2")
                            if "FF_closure" in final_hist_name:
                                final_hist_name = final_hist_name.replace("FF_closure", "FF_closure2")
                    
                    if "__" in final_hist_name:
                        if final_hist_name.endswith("up"):
                            final_hist_name = final_hist_name[:-2] + "Up"
                        if final_hist_name.endswith("down"):
                            final_hist_name = final_hist_name[:-4] + "Down"
                    hist.SetName(final_hist_name)
                    if "PNN" in hist_name:
                        if hist.GetNbinsX() >= 1000: ## this needs to rebin
                            rebinned_hist = rebin_histogram(hist, new_bins)
                        else:
                            rebinned_hist = hist
                        rebinned_hist.SetName(final_hist_name)
                        rebinned_hist.Write()
                    else:
                        hist.SetName(final_hist_name)
                        hist.Write()                    



        # Close the ROOT file

    fout.cd()
    if nom_only:
        fout.Close()
        print("finish filling output file, nominal only")
        return 0
    indices = list(range(1,5)) if "PNN" in var else [""]
    for index in indices:
        if "_em_" in input_dir:
            continue
        ## there is some small issue with the closure uncertainty, post-process it here
        h_closure = fout.Get(f"nob{index}/fakes")
        h_closure1Up = fout.Get(f"nob{index}/fakes__FF_closure1Up")
        h_closure1Down = fout.Get(f"nob{index}/fakes__FF_closure1Down")
        # Calculate integrals first before scaling
        integralUp = h_closure1Up.Integral()
        integralDown = h_closure1Down.Integral()
        totalIntegral = h_closure.Integral()

        # Scale histograms and reassign them
        h_closure1Up.Scale(2 * totalIntegral / (integralUp + integralDown))
        h_closure1Down.Scale(2 * totalIntegral / (integralUp + integralDown))
        fout.cd(f"nob{index}")
        h_closure1Up.Write()
        h_closure1Down.Write()
        fout.cd()
    
    ad_hoc_systs = {"fakes":"FF_closure2",}# "ttbar":"btagUncLF"}
    for hist in ad_hoc_systs:
        if "_em_" in input_dir:
            continue
        fout.cd()
        h_closure = fout.Get(f"btag/{hist}")
        h_closure2Up = fout.Get(f"btag/{hist}__{ad_hoc_systs[hist]}Up")
        h_closure2Down = fout.Get(f"btag/{hist}__{ad_hoc_systs[hist]}Down")
        # Calculate integrals first before scaling
        integralUp = h_closure2Up.Integral()
        integralDown = h_closure2Down.Integral()
        totalIntegral = h_closure.Integral()



        # Scale histograms and reassign them
        h_closure2Up.Scale(2 * totalIntegral / (integralUp + integralDown))
        h_closure2Down.Scale(2 * totalIntegral / (integralUp + integralDown))
        fout.cd("btag")
        h_closure2Up.Write()
        h_closure2Down.Write()


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
    
