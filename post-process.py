import sys
import yaml
import os
import ROOT as R
import argparse
import array
with open("/data/bond/zhiyuanl/Plotting//sample_database/datasets.yaml" , "r") as file:
    samples_list =  yaml.safe_load(file)
import re


R.EnableImplicitMT()

def extract_number(s):
    # Define the regex pattern
    pattern = r'M-(\d+)'
    # Search for all occurrences of the pattern
    matches = re.findall(pattern, s)
    # Convert matches to integers (if any) and return
    return [int(match) for match in matches]
def Add_new_column(df,new_column, overwrite=False):
    '''
    add a new column, new_column should be a dictionary with key name of new column with value of column value (best to use float)
    new_column = {column_name: value}
    ''' 
    modified = False
    col_names = df.GetColumnNames()
    print("calling adding new column")
    for c in new_column:    
        if c not in col_names:    
            df = df.Define(c,str(new_column[c])) 
            print(f"Adding new Column {c}")
            modified = True
        elif overwrite and c in col_names:
            df = df.Redefine(c,str(new_column[c])) 
            print(f"Redefining Column {c}")
            modified = True
        else:
            continue
        #     print(f"Column already exists {c}")
    return df, modified
def Redefine_type(df, pattern, old_type, new_type):
    # print(df.GetColumnType(pattern))
    modified = False
    for n in df.GetColumnNames():
        name = str(n)
        if pattern in name:
            if old_type == df.GetColumnType(name):
                modified = True
                print(f'redefining column {name} for old type {old_type} to new type {new_type}')
                
                if new_type == "int":
                    df = df.Redefine(name, f'int({name})')
                elif new_type == "float":
                    df = df.Redefine(name, f'float({name})')
                elif new_type == "double":
                    df = df.Redefine(name, f'double({name})')
                elif new_type == "bool":
                    df = df.Redefine(name, f'bool({name})')
                elif new_type == "UChar_t":
                    df = df.Redefine(name, f'static_cast<UChar_t>({name})')
                else:
                    print("supported type: int, float, bool")
                
            
        
    return df, modified
def redefine_column(df,column):
   
    col_names = df.GetColumnNames()
    for c in column:
        if c not in col_names:
            print(f"ERROR , {column} not found in dataframe")
            sys.exit(-1)
        df=df.Redefine(c, column[c] )
    return df

def find_tree_names(root_file):
    tree_names = []
    rfile = R.TFile.Open(root_file)
    for key in rfile.GetListOfKeys():
        if "map" in key.GetName():
            continue
        # print(key)
        obj = key.ReadObj()
        if isinstance(obj, R.TTree):
            tree_names.append(obj.GetName())
    
    print(tree_names)
    return tree_names


def keep_only_nominal(df):
    ori_col_names = df.GetColumnNames()
    col_names = [str(c) for c in ori_col_names if "__" not in str(c)]
    return col_names

def post_proc(f, samples_list, keep_only_nom=False, era='2022postEE', channel='mt', cut='nob', out_vars =[], pnn_format= False):
    luminosities = {
    "2022EE":7.875e3,
    "2022postEE":  	26.337e3  }
    lumi = luminosities[args.era]
    cut_dict = {
    'et': {
    'nob': '(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)&&pt_1 > 30 &&extramuon_veto == 0  && extraelec_veto == 0 && (id_tau_vsMu_VLoose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 70) && ( ! (phi_2>1.8 && phi_2< 2.7 && eta_2 > 1.5  && eta_2<2.2)  )',
    'nob_tight': '(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)&&pt_1 > 30 &&extramuon_veto == 0  && extraelec_veto == 0 && (id_tau_vsMu_VLoose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 70) && ( ! (phi_2>1.8 && phi_2< 2.7 && eta_2 > 1.5  && eta_2<2.2)  )',
    
    },
    'mt':{
    'nob':'(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)&& pt_1> 25.0 &&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsMu_Loose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 70)',
    'nob_tight':'(( nbtag == 0 ) &&(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) &&((trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)&& pt_1> 25.0 &&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsMu_Loose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) )&& ((q_1 * q_2) < 0) &&mt_1 < 40)',
    },
    'tt': {
    'nob': '(( (trg_double_tau35_mediumiso_hps == 1 || trg_double_tau40_mediumiso_tightid == 1 || trg_double_tau40_tightiso == 1 || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1)&& (id_tau_vsJet_Medium_2 > 0  && dz_2 < 0.2 &&   pt_2 > 40 && eta_2 < 2.1 && eta_2 > -2.1 && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0         && deltaR_ditaupair > 0.5 ) &&(id_tau_vsJet_Medium_1 > 0 && dz_1 < 0.2 && pt_1 > 40 && eta_1 < 2.1 && eta_1 > -2.1 && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0  )))',
    'btag': '(( nbtag >= 1 ) &&( (trg_double_tau35_mediumiso_hps == 1 || trg_double_tau40_mediumiso_tightid == 1 || trg_double_tau40_tightiso == 1 || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1)&&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsJet_Medium_1 > 0 && dz_1 < 0.2 && pt_1 > 40 && eta_1 < 2.1 && eta_1 > -2.1 && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0  )&& (id_tau_vsJet_Medium_2 > 0  && dz_2 < 0.2 &&   pt_2 > 40 && eta_2 < 2.1 && eta_2 > -2.1 && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0         && deltaR_ditaupair > 0.5 ) )&& ((q_1 * q_2) < 0) )',
    }
    }
    weight_dict = {
        "tt": 'is_data? double(1.0) : Xsec *  {0}* puweight * genWeight/genEventSumW *    btag_weight   *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 *  FF_weight * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 * ggh_NNLO_weight'.format(lumi),
        "mt": 'is_data? double(1.0) : Xsec   * {0} * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight *id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1 * ggh_NNLO_weight'.format(lumi),
        "et": 'is_data? double(1.0) : Xsec * {0}* puweight * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2  *  btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2  * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30 * ggh_NNLO_weight'.format(lumi),
    }
    
    print("start processing    ")
    for n in samples_list:
        if n in f:
            print(f'processing {n} process for file {f} ')
            trees = find_tree_names(f)
            tree_name = trees[0] if 'ntuple' not in trees else 'ntuple'
            print(tree_name)
            df_mc = R.RDataFrame(tree_name, f)
            col_names = df_mc.GetColumnNames()
            if 'genEventSumW'  not in col_names:    
                gensumw = R.RDataFrame('conditions', f).Sum('genEventSumw').GetValue()
                df_mc = df_mc.Define('Xsec', str(samples_list[n]['xsec']) +'f')
                # df_mc = df_mc.Define('Xsec', '2.0f')
                df_mc = df_mc.Define('genEventSumW', f'{gensumw}f')
                print(f"Adding new Column genEventSumW: {gensumw}")
            else:
                print(f'genEventSumW was added in file {f} already. ')
            if "Run_2022" in f:
                    df_mc = df_mc.Redefine("genEventSumW", '1.0f') ## for data define genEventSumW as 1   
            df_mc, _1 = Add_new_column(df_mc,  
            {'genWeight': '1.0f', 'Xsec' : '1.0f', 'is_fake' : 'false', "gen_match_2": 'int(-1)', "puweight": "double(1.0)", "btag_weight" : "double(1.0)", 
            "id_wgt_mu_1" : "1.0f", "iso_wgt_mu_1" : "double(1.0)", 'id_wgt_ele_wpTight': 'double(1.0)',
            'id_wgt_tau_vsMu_Tight_2' : "double(1.0)","id_wgt_tau_vsEle_Tight_2" : 'double(1.0)', 'id_wgt_tau_vsMu_VLoose_2': 'double(1.0)', "id_wgt_tau_vsMu_Loose_2" : "double(1.0)", "id_wgt_tau_vsEle_VVLoose_2" : "double(1.0)", "id_wgt_tau_vsJet_Medium_2" : "double(1.0)",  'id_wgt_tau_vsJet_Medium_1': 'double(1.0)', 
            "trg_wgt_single_mu24ormu27" : "double(1.0)", 'trg_wgt_ditau_crosstau_2': 'double(1.0)','trg_wgt_ditau_crosstau_1': 'double(1.0)', 'trg_wgt_single_ele30' : 'double(1.0)', 'trg_wgt_single_mu24' :'double(1.0)',
            "ZPtMassReweightWeight" : "double(1.0)", "FF_weight": "1.0f",
            'C_QCD': 'met/pt_2 * cos(metphi - phi_2 ) ',  'C_W': '(met + pt_1)/pt_2 * cos(metphi + phi_1- phi_2 )',
            'deta_12' : 'eta_1 - eta_2', 'dphi_12' : 'phi_1 - phi_2', 'tau_gen_match_2' : 'bool(0)',
            'Lumi': str(lumi),  "ggh_NNLO_weight": "double(1.0)",
            # 'trg_wgt_ditau_crosstau_12' : '( trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 + 1 * (trg_double_tau35_mediumiso_hps <1))'
            } )
            df_mc, _2 = Add_new_column(df_mc, 
                                       {'Train_weight': weight_dict[channel],}, overwrite=True)
            df_mc,_3 = Redefine_type(df_mc,"pzetamissvis", "Double_t","float"  )
            df_mc,_4 = Redefine_type(df_mc,"trg_wgt_single_ele30", "Float_t","double"  )
            df_mc,_5 = Redefine_type(df_mc,"tau_gen_match_2", "Bool_t","UChar_t"  )
            df_mc,_6 = Redefine_type(df_mc, "id_wgt_tau_vsJet_Medium_1",  "Float_t","double"  )
            df_mc,_7 = Redefine_type(df_mc, "id_wgt_tau_vsJet_Medium_2",  "Float_t","double"  )
            df_mc,_8 = Redefine_type(df_mc, "btag_weight",  "Float_t","double"  )
            modified = _1 or _2 or _3 or _4 or _5 or _6 or _7 or _8
    
            if keep_only_nom:
                output_columns = keep_only_nominal(df_mc)
            else:
                output_columns = out_vars if out_vars else df_mc.GetColumnNames()

            if cut: 
                before_count = df_mc.Count().GetValue()
                df_mc = df_mc.Filter(cut_dict[channel][cut])
                after_count =  df_mc.Count().GetValue()
                print("before_count , after_count",before_count , after_count)
                modified = True if before_count != after_count else modified
            if modified:
                # df_mc.Snapshot(tree_name,   f'{f}a', PNN_vars) # update the file finished
                if pnn_format and '2HDM' in f:
                    M = extract_number(f)
                    print("saving to tree ", f"Xtohh{M[0]}")
                    df_mc.Snapshot(f"Xtohh{M[0]}",   f'{f}a.root', output_columns) # update the file finished 
                else:   
                    df_mc.Snapshot(tree_name,   f'{f}a.root', output_columns) # update the file finished

                print(f"finished processing {f}")
                os.system(f"mv {f}a.root {f}")
            else:
                print(f"nothing changed for {f}")
                sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='input file for post-process')
    parser.add_argument('--era', type = str, default='2022postEE')
    parser.add_argument('--channel', type = str, default='mt')
    parser.add_argument('--keep_only_nom', type = int, default=0)
    parser.add_argument('--cut', type = str, default='nob')
    parser.add_argument('--out_vars', nargs='+', type = str)
    parser.add_argument('--pnn_format', type= int, default =0)
    args = parser.parse_args()
    



    PNN_vars = [ "dphi_12", "deta_12", "Train_weight","Xsec","beta_1","beta_2","bphi_1","bphi_2","bpt_1","bpt_2","deltaR_ditaupair","dxy_1","dxy_2","dz_1","dz_2","eta_1","eta_2","eta_fastmtt","event","mTdileptonMET","m_fastmtt","m_vis","mass_1","mass_2","mass_tt","met","metSumEt","metphi","mjj","mt_1","mt_2","mt_tot","nbtag","njets","nprebjets","phi_1","phi_2","phi_fastmtt","pt_1","pt_2","pt_dijet","pt_fastmtt","pt_tt","pt_ttjj","pt_vis","pzetamissvis","q_1","q_2"]
    post_proc(args.input_file, samples_list, args.keep_only_nom, args.era, args.channel, args.cut, args.out_vars, args.pnn_format )
    # print(args.out_vars)