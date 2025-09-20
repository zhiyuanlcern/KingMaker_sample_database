import ROOT

import re
import sys

input_file_name =  str(sys.argv[1])
# Open the source ROOT file
# input_file_name = 'histograms_60_mt_2022EE.root'  # Update this to your input ROOT file path
source_file = ROOT.TFile.Open(input_file_name, "READ")

# Create two new ROOT files
nob_file = ROOT.TFile.Open(f'{input_file_name}_bkg.root', 'RECREATE')
nob_bsm_file = ROOT.TFile.Open(f'{input_file_name}_signal.root', 'RECREATE')

# Create a directory named "nob" in each of the new ROOT files
nob_dir = nob_file.mkdir("nob")
nob_bsm_dir = nob_bsm_file.mkdir("nob")

processed_histograms = set()

# Loop over all keys in the source file
source_file.cd()
for key in ROOT.gDirectory.GetListOfKeys():
    obj_name =key.GetName()
    if obj_name in processed_histograms:
        continue
    obj = source_file.Get(obj_name)
    if obj.InheritsFrom("TH1"):  # Check if the object is a histogram
    
            # If the histogram name is already processed, skip it

        # Regular expression pattern to match 'pnn_' followed by any digits
        pattern = r"pnn_\d+"
        # Replace matches with an empty string
        new_name = re.sub(pattern, "", obj_name)
        
        # new_name = obj_name.replace("pnn_60", "")
        new_name = new_name.replace("___", "")
        new_name = new_name.replace("Data_", "data_obs")
        new_name = new_name.replace("down", "Down")
        new_name = new_name.replace("up", "Up")
        new_name = new_name.replace("down", "Down")
        new_name = new_name.replace("up", "Up")
        new_name = new_name.replace("_Down", "Down")
        new_name = new_name.replace("_Up", "Up")
        
        
        if new_name.endswith("_"):
            new_name = new_name.rstrip("_")
        
        # Set the new name to the histogram
        obj.SetName(new_name)
        if new_name.endswith("weight") or new_name.endswith("_1") or new_name.endswith("_2"):
            continue
        if "BSM" in obj_name:
            # If the histogram name contains "BSM", save it in the BSM file
            nob_bsm_dir.cd()
            obj_clone = obj.Clone()
            obj_clone.Write()
        else:
            # Otherwise, save it in the regular file
            nob_dir.cd()
            obj_clone = obj.Clone()
            obj_clone.Write()
        processed_histograms.add(obj_name)

# Close the files to save changes
nob_file.Close()
nob_bsm_file.Close()
source_file.Close()
