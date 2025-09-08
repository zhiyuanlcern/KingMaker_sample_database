import sys
import yaml
import os
import ROOT as R
from Htautau import *
import time
import array

# code run steering
# run = False
run = True
# produce_final_fakes = True

R.gROOT.SetBatch(True)

input_path = str(sys.argv[1]) # '2016postVFP_et'
channel = str(sys.argv[2])
era = str(sys.argv[3])
print(input_path, channel)
    
    
 DR_name = {"data":"QCD",    "wjets":"W",    "ttbar":"ttbar" } ## the naming follow the names in produce_fake
    
    systematics.insert(0,"")  ##  add the nominal in the syst list, nominal is alaways run
    for DR in DRs:
        df = df_dict[ DR_name[DR] ]
        if channel != "tt":
            GetmTtotweights_code =f'''
            auto GetmTtotweights{DR} =[] (float mt_tot, int nbtag, float mt_1 ) {{
                float W = 0;
                // nob = "( nbtag == 0 ) "
                // btag = "( nbtag >= 1 ) "
                // tight_mT = " ( mt_1 < 40.0) "
                // loose_mT = " ( mt_1 > 40.0 && mt_1 < 70.0 ) "

                if (nbtag  == 0 ){{
                    if ( mt_1 < 40.0) {{
                        W = Weights["{DR}_ARloose_mTnobmt_tot"]->GetBinContent( Weights["{DR}_ARloose_mTnobmt_tot"]->FindBin(mt_tot) ) ;
                    }}    
                    else if (mt_1 > 40.0 && mt_1 < 70.0 ) {{
                        W = Weights["{DR}_ARtight_mTnobmt_tot"]->GetBinContent( Weights["{DR}_ARtight_mTnobmt_tot"]->FindBin(mt_tot) ) ;
                    }}    
                    else {{
                        W = 0 ;}}
                }}
                else {{
                    if ( mt_1 < 40.0) {{
                        W = Weights["{DR}_ARloose_mTbtagmt_tot"]->GetBinContent( Weights["{DR}_ARloose_mTbtagmt_tot"]->FindBin(mt_tot) ) ;
                    }}    
                    else if (mt_1 > 40.0 && mt_1 < 70.0 ) {{
                        W = Weights["{DR}_ARtight_mTbtagmt_tot"]->GetBinContent( Weights["{DR}_ARtight_mTbtagmt_tot"]->FindBin(mt_tot) ) ;
                    }}    
                    else {{
                        W = 0 ;}}
                }}
                return W ;
            }};
            '''
            # print(GetmTtotweights_code)
            R.gROOT.ProcessLine(f'.L cpp_code/loadFF.C+')
            R.loadFF(era,channel)
            # R.gROOT.LoadMacro('cpp_code/loadFF.C') # load FF histograms /or any other histograms into a dictionary called Weights with key [histname] 
            R.gInterpreter.Declare(GetmTtotweights_code) 
        
        for syst in systematics:
            # for tt channel, nothing to be updated
            if apply_fraction:
                if channel !="tt": 
                    df = df.Redefine(f'FF_weight{syst}', f'GetmTtotweights{DR}(mt_tot,nbtag,mt_1 ) * FF_weight{syst}')
                    # df = df.Redefine(f'genWeight{syst}', f'FF_weight{syst}')
                    print("I am here 14 ", df.Count().GetValue())
        df.Snapshot('ntuple', f'{input_path}/Fakes_mttot_tmp{tag}{DR}.root', columns)
        print(f"finishing saving temporary fakes file to :{input_path}/Fakes_mttot_tmp{tag}{DR}.root ")    
   