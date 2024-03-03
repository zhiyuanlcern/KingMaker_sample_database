import ROOT as R
import sys
input_file = str(sys.argv[1])
channel_name = str(sys.argv[2])
era = str(sys.argv[3])

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
'et': '(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)&&pt_1 > 30 &&extramuon_veto == 0  && extraelec_veto == 0 && (id_tau_vsMu_VLoose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 70)',
'mt': '(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)&& pt_1> 25.0 &&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsMu_Loose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 70)',
'tt' :'(( (trg_double_tau35_mediumiso_hps == 1 || trg_double_tau40_mediumiso_tightid == 1 || trg_double_tau40_tightiso == 1 || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1)&& (id_tau_vsJet_Medium_2 > 0  && dz_2 < 0.2 &&   pt_2 > 40 && eta_2 < 2.1 && eta_2 > -2.1 && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0         && deltaR_ditaupair > 0.5 ) &&(id_tau_vsJet_Medium_1 > 0 && dz_1 < 0.2 && pt_1 > 40 && eta_1 < 2.1 && eta_1 > -2.1 && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0  )))',
}
weight_dict = {
    "tt": 'Xsec  *  {0}* puweight * genWeight/genEventSumW *    btag_weight  *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 *  FF_weight * ( trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 + 1 * (trg_double_tau35_mediumiso_hps <1))'.format(lumi),
    "mt": 'Xsec   * {0} * puweight * genWeight/genEventSumW * btag_weight * FF_weight   * id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1 *(trg_wgt_ditau_crosstau_2 * trg_cross_mu20tau27_hps  + 1 * (trg_cross_mu20tau27_hps < 1) )'.format(lumi),
    "et": 'Xsec * {0} * puweight * genWeight/genEventSumW *   btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2 * id_wgt_ele_wpTight * (trg_wgt_ditau_crosstau_2 * trg_cross_ele24tau30_hps + 1 * (trg_cross_ele24tau30_hps <1) )' .format(lumi),
}

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
    print(f"Already processed for file {input_file}.  ")
    sys.exit(0)
filtered_df = df.Filter(cut_dict[channel_name]).Define("Train_weight", weight_dict[channel_name])
col_names = [str(c) for c in ori_col_names if ("pnn" in str(c) or "Train_weight" in str(c))]

# Now, write the filtered data frame to a temporary file
filtered_df.Snapshot("ntuple", input_file, col_names)

