import sys
import yaml
import os
import ROOT as R
import array
with open("../sample_database/datasets.yaml" , "r") as file:
    samples_list =  yaml.safe_load(file)

R.EnableImplicitMT()
def Add_new_column(df,new_column):
    '''
    add a new column, new_column should be a dictionary with key name of new column with value of column value (best to use float)
    new_column = {column_name: value}
    ''' 
    modified = False
    col_names = df.GetColumnNames()
    edited = False
    for c in new_column:    
        if c not in col_names:    
            df = df.Define(c,str(new_column[c])) 
            print(f"Adding new Column {c}")
            modified = True
        # else:
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
                else:
                    print("supported type: int, float, bool")
                
            
        
    return df, modified

def keep_only_nominal(df):
    ori_col_names = df.GetColumnNames()
    # for c in ori_col_names:
    #     print(c, type(c),str(c))
    col_names = [str(c) for c in ori_col_names if "__" not in str(c)]
    return col_names

def post_proc(f, samples_list, keep_only_nom=False):
    print("start processing    ")
    for n in samples_list:
        if n in f:
            print(f'processing {n} process for file {f} ')
            df_mc = R.RDataFrame('ntuple', f)
            col_names = df_mc.GetColumnNames()
            if 'Xsec'  not in col_names:    
                gensumw = R.RDataFrame('conditions', f).Sum('genEventSumw').GetValue()
                df_mc = df_mc.Define('Xsec', str(samples_list[n]['xsec']) +'f').Define('genEventSumW', str(gensumw) + 'f')
                print(f'finished processing {f}')
            # else:
                # print(f'already processed {f}')
                
            


            df_mc, _1 = Add_new_column(df_mc,  
            {'genWeight': '1.0f', 'Xsec' : '1.0f', 'is_fake' : 'false', 'genEventSumW': '1.0f', "gen_match_2": 'int(-1)', "puweight": "double(1.0)", "btag_weight" : "1.0f", 
            "id_wgt_mu_1" : "1.0f", "id_wgt_tau_vsEle_VVLoose_2" : "double(1.0)", "id_wgt_tau_vsJet_Medium_2" : "double(1.0)", "id_wgt_tau_vsMu_Loose_2" : "double(1.0)","iso_wgt_mu_1" : "double(1.0)",  "trg_wgt_single_mu24ormu27" : "double(1.0)",
            "ZPtMassReweightWeight" : "double(1.0)", "FF_weight": "1.0f",
            'C_QCD': 'met/pt_2 * cos(metphi - phi_2 ) ','trg_wgt_ditau_crosstau_2': '1.0f', 'id_wgt_tau_vsJet_Medium_2' :'double(1.0)', 'id_wgt_ele_wpTight': 'double(1.0)',
            'trg_wgt_ditau_crosstau_1': '1.0f', 'id_wgt_tau_vsJet_Medium_1': 'double(1.0)',
            'C_W': '(met + pt_1)/pt_2 * cos(metphi + phi_1- phi_2 )'} )
            # df_mc, modified = Add_new_column(df_mc,  'Xsec' : 
            # # 
            # df_mc, modified = Redefine_type(df_mc, "id_wgt_tau_vsJet_Medium_2","Float_t","double"  )
            # df_mc, modified = Redefine_type(df_mc, "id_wgt_tau_vsMu_Loose_2","Float_t","double"  )
            # df_mc, modified = Redefine_type(df_mc, "iso_wgt_mu_1","Float_t","double"  )
            # df_mc, modified = Redefine_type(df_mc, "trg_wgt_single_mu24ormu27","Float_t","double"  )
            
            # df_mc, modified = Redefine_type(df_mc, "ZPtMassReweightWeight","Float_t","double"  )
            # df_mc, modified = Redefine_type(df_mc, "id_wgt_tau_vsEle_VVLoose_2","Float_t","double"  )
            # df_mc,modified = Redefine_type(df_mc,"puweight", "Float_t","double"  )
            # df_mc,modified = Redefine_type(df_mc,"pt_1_FF_closureUp", "Double_t","float"  )
            df_mc,_2 = Redefine_type(df_mc,"pzetamissvis", "Double_t","float"  )
            # df_mc,modified = Redefine_type(df_mc,"pt_2", "Double_t","float"  )
            # df_mc,modified = Redefine_type(df_mc,"pt_1", "Double_t","float"  )
            
            # df_mc, modified =  Redefine_type(df_mc,"pt_1_FF_tot_StatDown", "Double_t", "float") 
            # df_mc, modified =  Redefine_type(df_mc,"pt_1_FF_tot_StatUp", "Double_t", "float") 
            # df_mc, modified =  Redefine_type(df_mc,"pt_1_FF_ttbarUp", "Double_t", "float") 
            # df_mc, modified =  Redefine_type(df_mc,"pt_1_FF_ttbarDown", "Double_t", "float") 
            # df_mc, modified =  Redefine_type(df_mc,"pt_1_FF_wjetsUp", "Double_t", "float") 
            # df_mc, modified =  Redefine_type(df_mc,"pt_1_FF_wjetsDown", "Double_t", "float") 

            modified = _1 or _2




            # if modified:
            #     df_mc,_ = Redefine_type(df_mc,"btag_weight", "Int_t","float"  )
            
            if modified:
                if keep_only_nom:
                    df_mc.Snapshot('ntuple',   f'{f}a',keep_only_nominal(df_mc)) # update the file finished
                else:
                    df_mc.Snapshot('ntuple',   f'{f}a') # update the file finished
                print(f"finished processing {f}")
                os.system(f"mv {f}a {f}")
            else:
                print(f"nothing changed for {f}")
            # break
    

post_proc(sys.argv[1],samples_list,bool(int(sys.argv[2])) ) 
    