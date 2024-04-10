import ROOT as R
import sys
import re
input_file = str(sys.argv[1])
channel_name = str(sys.argv[2])
era = str(sys.argv[3])


def extract_number(s):
    # Define the regex pattern
    pattern = r'M-(\d+)'
    # Search for all occurrences of the pattern
    matches = re.findall(pattern, s)
    # Convert matches to integers (if any) and return
    return [int(match) for match in matches]
def is_file_ok(file_path):
    # Attempt to open the file
    file = R.TFile.Open(file_path, "READ")
    
    # Check if the file is open and healthy
    if file and not file.IsZombie() and file.TestBit(R.TFile.kRecovered):
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

luminosities = {
    "2022EE":7.875e3,
    "2022postEE":  	26.337e3  }
lumi = luminosities[era]
cut_dict = {
'et': '(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)&&pt_1 > 30 &&extramuon_veto == 0  && extraelec_veto == 0 && (id_tau_vsMu_VLoose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 40)',
'mt': '(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)&& pt_1> 25.0 &&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsMu_Loose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 40)',
'tt' :'(( (trg_double_tau35_mediumiso_hps == 1 || trg_double_tau40_mediumiso_tightid == 1 || trg_double_tau40_tightiso == 1 || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1)&& (id_tau_vsJet_Medium_2 > 0  && dz_2 < 0.2 &&   pt_2 > 40 && eta_2 < 2.1 && eta_2 > -2.1 && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0         && deltaR_ditaupair > 0.5 ) &&(id_tau_vsJet_Medium_1 > 0 && dz_1 < 0.2 && pt_1 > 40 && eta_1 < 2.1 && eta_1 > -2.1 && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0  )))',
}
weight_dict = {
    "tt": 'Xsec  *  {0}* puweight * genWeight/genEventSumW *    btag_weight  * FF_weight * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 *  ( trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 + 1 * (trg_double_tau35_mediumiso_hps <1))'.format(lumi),
    "mt": 'Xsec   * {0} * puweight * genWeight/genEventSumW * btag_weight * FF_weight   * id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1 *(trg_wgt_ditau_crosstau_2 * trg_cross_mu20tau27_hps  + 1 * (trg_cross_mu20tau27_hps < 1) )'.format(lumi),
    "et": 'Xsec * {0} * puweight * genWeight/genEventSumW *   btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2 * id_wgt_ele_wpTight * (trg_wgt_ditau_crosstau_2 * trg_cross_ele24tau30_hps + 1 * (trg_cross_ele24tau30_hps <1) )' .format(lumi),
}
def post_process():
    # Create an RDataFrame from the tree
    if is_file_ok(input_file):
        df = R.RDataFrame( "ntuple",input_file)

    # Apply your filter condition here
    # For example, filter out entries with a value less than 5 in the column 'value'
    try:
        ori_col_names = df.GetColumnNames()
    except:
        print(f"warning!  file {input_file} cannot be opened! ")
        sys.exit(0)
    if "Train_weight" in ori_col_names:
        if "mt_1" not in ori_col_names:
            print(f"warning!  file {input_file} doesn't have mt_1! ")
            sys.exit(0)
        print(f"Already processed for file {input_file}.  , cutting for tight_mt")
        # filtered_df = df.Filter("mt_1 < 40") if channel_name != "tt" else df
        filtered_df = df
        filtered_df1 = filtered_df.Filter("pt_tt < 50")
        filtered_df2 =filtered_df.Filter("pt_tt > 50 && pt_tt < 100")
        filtered_df3 =filtered_df.Filter("pt_tt > 100 && pt_tt < 200")
        filtered_df4 =filtered_df.Filter("pt_tt > 200")
    else:
        if "mt_1" not in ori_col_names:
            print(f"warning!  file {input_file} doesn't have mt_1! ")
            sys.exit(0)
        filtered_df = df.Filter(cut_dict[channel_name])
        filtered_df1 = filtered_df.Filter("pt_tt < 50")
        filtered_df2 =filtered_df.Filter("pt_tt > 50 && pt_tt < 100")
        filtered_df3 =filtered_df.Filter("pt_tt > 100 && pt_tt < 200")
        filtered_df4 =filtered_df.Filter("pt_tt > 200")
    #     sys.exit(0)
    if ("Data" in input_file) or ("data" in input_file) or ("Run2022" in input_file) or ('Sep2022' in input_file) :
        
        if "Train_weight" in ori_col_names:
            filtered_df = filtered_df.Redefine("Train_weight", "1.0f")    
        else:   
            filtered_df = filtered_df.Define("Train_weight", "1.0f")    
            # filtered_df = df.Filter(cut_dict[channel_name]).Define("Train_weight", "1.0f")    
    else:
        if "Train_weight" in ori_col_names:
            filtered_df = filtered_df.Redefine("Train_weight", weight_dict[channel_name])
        else:
            # filtered_df = df.Filter(cut_dict[channel_name]).Define("Train_weight", weight_dict[channel_name])
            filtered_df = filtered_df.Define("Train_weight", weight_dict[channel_name])
    # new_column = filtered_df.GetColumnNames()
    # col_names = [str(c) for c in new_column if ("pnn" in str(c) or "Train_weight" in str(c) or "weight" in str(c) or "wgt" in str(c) or "Weight" in str(c) or "Xsec" in str(c) or "genEvent" in str(c)) ]

    # Now, write the filtered data frame to a temporary file
    # filtered_df.Snapshot("ntuple", input_file, col_names)
    
    if '2HDM' not in input_file:
        filtered_df.Snapshot("ntuple", input_file)
    else:
        M = extract_number(input_file)
        print("saving to tree ", f"Xtohh{M[0]}")
        filtered_df.Snapshot(f"Xtohh{M[0]}", input_file)
    # filtered_df1.Snapshot("ntuple", input_file + "_bin1")
    # filtered_df2.Snapshot("ntuple", input_file + "_bin2")
    # filtered_df3.Snapshot("ntuple", input_file + "_bin3")
    # filtered_df4.Snapshot("ntuple", input_file + "_bin4")

def simple_cut():
    # Create an RDataFrame from the tree
    if is_file_ok(input_file):
        df = R.RDataFrame( "ntuple",input_file)

    # Apply your filter condition here
    # For example, filter out entries with a value less than 5 in the column 'value'
    try:
        ori_col_names = df.GetColumnNames()
    except:
        print(f"warning!  file {input_file} cannot be opened! ")
        sys.exit(0)
    if "mt_1" not in ori_col_names:
        print(f"warning!  file {input_file} doesn't have mt_1! ")
        sys.exit(0)
    filtered_df = df.Filter("mt_1 < 40")
    
    filtered_df.Snapshot("ntuple", input_file)

post_process()
# simple_cut()