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

Htautau = Htautau_selections()
DR_QCD= Htautau.DR_QCD_tt if channel == "tt" else Htautau.DR_QCD_lt
DR_W= Htautau.DR_W
DR_ttbar=  Htautau.DR_ttbar
if channel == "tt":
    ID = combinecut(Htautau.ID_tt,  Htautau.DR_deeptau_selections[channel])
    Anti_ID = combinecut(Htautau.Anti_ID_tt,Htautau.DR_deeptau_selections[channel])
else:
    ID = combinecut(Htautau.ID_lt,  Htautau.DR_deeptau_selections[channel])
    Anti_ID = combinecut(Htautau.Anti_ID_lt,Htautau.DR_deeptau_selections[channel])

if era == "2016preVFP":
    lumi = 15.1158e3
elif era == "2016postVFP":
    lumi = 10.0093e3
elif era == "2017":
    lumi = 41.5e3
elif era == "2018":
    lumi = 59.8e3
elif era == "2022EE":
    lumi = 7.875e3
elif era == "2022postEE":
    lumi = 26.337e3
else: 
    print("wrong year provided")
    sys.exit(-10) 


MC_weight_list = ["genWeight", "btag_weight", "id_wgt_tau_vsJet_Medium_2", "trg_wgt_ditau_crosstau_2", "genEventSumW" , "Xsec"]
if channel == "et":
    lepton_selection = combinecut(Htautau.et_triggers_selections[era],Htautau.electron_selections,Htautau.lepton_veto,)
    complete_lepton_selection = lepton_selection
    var = "pt_2"
    MC_weight =  f'(is_data == 0? genWeight *  btag_weight * puweight * (-1.0) * Xsec * {lumi} *  id_wgt_tau_vsJet_Medium_2 *id_wgt_tau_vsEle_Tight_2* id_wgt_ele_wpTight * (trg_wgt_ditau_crosstau_2 * trg_cross_ele24tau30_hps + 1 * (trg_cross_ele24tau30_hps <1))  / genEventSumW  :  double(1.0))'
    MC_weight_list.extend(["id_wgt_ele_wpTight" , "id_wgt_tau_vsEle_Tight_2", 'trg_wgt_single_ele30'])
elif channel == "mt":
    lepton_selection = combinecut(Htautau.mt_triggers_selections[era],Htautau.muon_selections,Htautau.lepton_veto,)
    complete_lepton_selection  = lepton_selection
    var = "pt_2"
    MC_weight =  f'(is_data == 0? genWeight *  btag_weight * puweight * (-1.0) * Xsec * {lumi} * id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  * (trg_wgt_ditau_crosstau_2 * trg_cross_mu20tau27_hps  + 1 * (trg_cross_mu20tau27_hps < 1) )/ genEventSumW  :  double(1.0) )'
    MC_weight_list.extend(["iso_wgt_mu_1"])
elif channel == "tt":
    lepton_selection = combinecut(Htautau.tt_triggers_selections[era],Htautau.tt_secondtau_selections,Htautau.lepton_veto)
    # lepton_selection = combinecut(Htautau.tt_secondtau_selections,Htautau.lepton_veto)
    # lepton_selection = combinecut(Htautau.lepton_veto)
    complete_lepton_selection = combinecut(Htautau.tt_secondtau_selections,Htautau.lepton_veto, Htautau.tt_triggers_selections[era])
    var = "pt_1"
    MC_weight =  f'(is_data == 0? genWeight *  btag_weight * puweight * (-1.0) * Xsec * {lumi} * id_wgt_tau_vsJet_Medium_2  * id_wgt_tau_vsJet_Medium_1 * ( trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 + 1 * (trg_double_tau35_mediumiso_hps <1)) / genEventSumW  : double(1.0))'
    MC_weight_list.extend(["id_wgt_tau_vsJet_Medium_1", "trg_wgt_ditau_crosstau_1", "trg_wgt_ditau_crosstau_2"])
else:
    exit("wrong channel provided")

print(input_path, channel)


# input_path = 'fixbtag_nprebtagjets_newgensum'
# input_path = 'BSM_signals_highmass'
# input_path = 'tt_cross_checks_run2/'
# input_path = 'BSM_signals_fix_genweight/'
# input_path = 'mutau-new-CROWN/'
# input_path = 'mutau-fastmtt/'
# input_path = 'mutau-fastmtt'
with open("sample_database/datasets_plotting.yaml" , "r") as file:
    samples_list =  yaml.safe_load(file)


cut_dic = {
    'DR_QCD' : DR_QCD,
    'DR_W' : DR_W,
    'DR_ttbar' : DR_ttbar
}
if channel == "tt":
    cut_dic = {
    'DR_QCD' : DR_QCD,
}    
ID_dic = {
    'ID' : ID,
    'Anti' : Anti_ID,
}
nprebjets_dic = {
    '0preb': 'nprebjets == 0',
     '1ormorepreb'    : 'nprebjets > 0',
}
ratio_dic = {
    '0'    : f'(taujet_{var}/{var}) > 0 && (taujet_{var}/{var}) < 1.25 ',
    '1p25': f'(taujet_{var}/{var}) > 1.25 && (taujet_{var}/{var}) < 1.5 ',
    '1p5'    : f'(taujet_{var}/{var}) > 1.5',
}

def get(hname, directory, fin ):
    "get histogram from dir `directory` with name `hname` in file `fin`"
    if not hname or not fin: return
    fin.cd()
    dir_now = None
    if not directory:
        return fin.Get(hname)
    for d in directory.split('/'):
        if not dir_now:
            dir_now = fin.Get(d)
            dir_now.cd()
        else:
            dir_now = dir_now.Get(d)
    return dir_now.Get(hname)
def write(h, directory, name,fout):
    "Write `h` to dir `directory` with name `name` in file `fout`"
    if not h or not fout: return

    # if out.startswith('/'):
    #     out = out[1:]
    
    fout.cd()
    # R.gDirectory
    for d in directory.split('/'):
        if not d: continue
        if not R.gDirectory.Get(d) or not R.gDirectory.cd(d):
            R.gDirectory.mkdir(d)
            R.gDirectory.cd(d)
      
    h.Write(name)
    return 
def remove_neg(h):
    ## remove negative and large values 
    is_2D = False
    if h.GetNbinsY()>1:
        is_2D = True
    if is_2D:
        for x in range(0, h.GetNbinsX() +1 ):
            for y in range(0, h.GetNbinsY()+1):
                if (h.GetBinContent(x, y)) <0 or (h.GetBinContent(x, y)) >1:
                    h.SetBinContent(x, y, 0)
    else:
        for x in range(0, h.GetNbinsX() +1 ):
            if (h.GetBinContent(x) <  0.) :
                    h.SetBinContent(x, 0.0)
                    # print(h.GetTitle(),x, h.GetBinContent(x))
                    # h.SetBinError(x,1.0)
    return h 
def getall_list(input_path, samples_list, embedding =False, FF = False, signal=False, exclude_wjets=False, exlcude_dyjets_ll = True):
    '''
    get all samples names in input_path, default to exclude embedding, FF and signal files and include Wjets samples
    '''
    inputfile = []
    for fname in os.listdir(input_path):
        if '.root' not in fname or 'FakeFactor' in fname or 'output' in fname or 'input' in fname or 'Fakes' in fname or "closure" in fname or "Closure" in fname or "pnn" in fname or "tmpsamples" in fname:
            continue
        if not embedding:  ## default to skip embedding
            if  'Embedding' in fname :
                continue
        if not FF:  ## default to skip FF 
            if  'FF' in fname :
                continue
        if not signal:
            if ("SUSY" in fname) or ("Xtohh" in fname) or ("2HDM-II" in fname):
                continue
        if exclude_wjets:
            if ("WtoLNu" in fname ) or ("W1Jets" in fname ) or ("W2Jets" in fname ) or  ("W3Jets" in fname ) or ("W4Jets" in fname ) or ("WJets" in fname ):
                continue
        if exlcude_dyjets_ll:
            if "DYto2L" in fname:
                continue
        inputfile.append(input_path + '/' + fname)
    return inputfile
def getdata_list(input_path, samples_list):
    inputfile = []
    for fname in os.listdir(input_path):
        if 'FF' in fname or 'Fakes' in fname or "closure" in fname or "Closure" in fname:
            continue
        for n in samples_list: 
            if samples_list[n]['sample_type'] == 'data':
                if n in fname:
                    inputfile.append(input_path + '/' + fname)
                    break
    return inputfile
def Add_new_column(input_path, samples_list, new_column, embedding = False, FF = False):
    '''
    add a new column, new_column should be a dictionary with key name of new column with value of column value (best to use float), default to skip embedding and FF
    new_column = {column_name: value}
    '''
    f_list = getall_list(input_path, samples_list, embedding, FF)
    for f in f_list:
        # f: for example, fixbtag_nprebtagjets/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_RunIISummer20UL18NanoAODv9-106X.root
        for n in samples_list:
            if n in f:
                print(f)
                df_mc = R.RDataFrame('ntuple', f)
                col_names = df_mc.GetColumnNames()
                edited = False
                for c in new_column:    
                    if c not in col_names:    
                        edited = True
                        df_mc = df_mc.Define(c,str(new_column[c]))
                if edited:
                    df_mc.Snapshot('ntuple',  f)
                else:
                    print( f'column {new_column} already exists, skip' )   
def get_df(input_path, samples_list, save_ttbar_data=False, save_fraction=False):
    df_d = {}
    print(combinecut(DR_QCD, ID, lepton_selection))
    # binning = [30,40,50,60,70,80,90,100,120,140,200,350,500]
    samples = getall_list(input_path, samples_list)
    samples_noW = getall_list(input_path, samples_list, exclude_wjets=True) ## exlcude wjets background from W DR, Wjets will be only coming from fakes
    # print(samples)
    df0 = R.RDataFrame('ntuple', samples) ## skip signal from the background!!
    df_noW = R.RDataFrame('ntuple', samples_noW) ## skip signal from the background!!
    print(f"Finish getting df, entries : {df0.Count().GetValue() }")
    
    df_d['DR_QCDID'] = df0.Filter(combinecut(DR_QCD, ID, lepton_selection)).Define('genWeight_tmp',f'{MC_weight}')
    df_d['DR_QCDAnti'] = df0.Filter(combinecut(DR_QCD, Anti_ID, lepton_selection)).Define('genWeight_tmp',f'{MC_weight}')
    print(f"Finish getting QCD df, entries of QCD ID: {df_d['DR_QCDID'].Count().GetValue() }")
    print(f"Finish getting QCD df, entries of QCD Anti ID: {df_d['DR_QCDAnti'].Count().GetValue() }")

    if channel == "tt":
        ## for tt channel, only need to proceed QCD DR
        return df_d

    df_ttbar0 = R.RDataFrame('ntuple', input_path+'/TT*root') ## for ttbar, fakes are small, using only MC to calculate 
    print(f"Finish getting ttbar df, entries : {df_ttbar0.Count().GetValue() }")
    if save_ttbar_data:
        ## keep data with ttbar MC together
        df_d['DR_ttbarID']   = df0.Filter(combinecut('(  ( gen_match_2 != 6 && is_ttbar>0 ) || (is_ttbar <1)  )', DR_ttbar, ID , lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
        df_d['DR_ttbarAnti'] = df0.Filter(combinecut('(  ( gen_match_2 != 6 && is_ttbar>0 ) || (is_ttbar <1)  )', DR_ttbar,Anti_ID, lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
    else:
        ## using only MC to calculate 
        df_d['DR_ttbarID']   = df_ttbar0.Filter(combinecut('gen_match_2 ==  6','is_ttbar >= 1', DR_ttbar, ID,  lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
        df_d['DR_ttbarAnti'] = df_ttbar0.Filter(combinecut('gen_match_2 ==  6','is_ttbar >= 1', DR_ttbar, Anti_ID,  lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
        print(f"Finish getting ttbar df,  {df_ttbar0.Count().GetValue() }")
        print(f"Finish getting ttbar df, entries of ttbar ID: {df_d['DR_ttbarID'].Count().GetValue() }")
        print(f"Finish getting ttbar df, entries of ttbar AntiID: {df_d['DR_ttbarAnti'].Count().GetValue() }")
    df_d['DR_WID']   = df_noW.Filter(combinecut('is_wjets < 1', DR_W, ID, lepton_selection )).Define('genWeight_tmp',f'{MC_weight}')
    df_d['DR_WAnti'] = df_noW.Filter(combinecut('is_wjets < 1', DR_W, Anti_ID, lepton_selection )).Define('genWeight_tmp',f'{MC_weight}')
    print(f"Finish getting df, entries : {df_noW.Count().GetValue() }")
    print(f"Finish getting W df, entries of W Anti ID: {df_d['DR_WAnti'].Count().GetValue() }")
    print(f"Finish getting W df, entries of W ID: {df_d['DR_WID'].Count().GetValue() }")

    
    return df_d
def get_FF_f(df_d, FF_input,run =False, syst = False):
    h_d = {}
    #r = [30,40,50,60,70,80,90,100,120,140,200,350]
    binning = [30,40,50,60,70,80,90,100,120,140,200,350,500]
    c = R.TCanvas()
    for DR in cut_dic:
        for tau_id in ID_dic:
            for npreb in nprebjets_dic:
                for ratio in ratio_dic:
                    if run:
                        h_d[DR+tau_id+npreb+ratio] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, 'genWeight_tmp')
                        if syst: 
                            ## logic for ttbar / wjets stat up/down
                            #if is_ttbar: # up: redefine genWeight_tmp = genWeight_tmp * 1.4 # down: redefine genWeight_tmp =  genWeight_tmp * 0.6
                            #if is_wjets: # up: redefine genWeight_tmp = genWeight_tmp * 1.2 # down: redefine genWeight_tmp = genWeight_tmp * 0.8
                            h_d[DR+tau_id+npreb+ratio+"__FF_ttbarUp"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_ttbarUp", "is_ttbar? 1.4 * genWeight_tmp : genWeight_tmp ").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_ttbarUp")
                            h_d[DR+tau_id+npreb+ratio+"__FF_ttbarDown"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_ttbarDown", "is_ttbar? 0.6 * genWeight_tmp : genWeight_tmp").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_ttbarDown")
                            h_d[DR+tau_id+npreb+ratio+"__FF_wjetsDown"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_wjetsDown", "is_wjets? 1.2 * genWeight_tmp : genWeight_tmp").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_wjetsDown")
                            h_d[DR+tau_id+npreb+ratio+"__FF_wjetsUp"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_wjetsUp", "is_wjets? 0.8 * genWeight_tmp : genWeight_tmp").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_wjetsUp")
                        # write(h, directory, name,fout): "Write `h` to dir `directory` with name `name` in file `fout`"
                        write(h_d[DR+tau_id+npreb+ratio], "", DR+tau_id+npreb+ratio,FF_input)
                        if syst:
                            write(h_d[DR+tau_id+npreb+ratio+"__FF_ttbarUp"], "", DR+tau_id+npreb+ratio+"__FF_ttbarUp", FF_input)
                            write(h_d[DR+tau_id+npreb+ratio+"__FF_ttbarDown"], "", DR+tau_id+npreb+ratio+"__FF_ttbarDown", FF_input)
                            write(h_d[DR+tau_id+npreb+ratio+"__FF_wjetsDown"], "", DR+tau_id+npreb+ratio+"__FF_wjetsDown", FF_input)
                            write(h_d[DR+tau_id+npreb+ratio+"__FF_wjetsUp"], "", DR+tau_id+npreb+ratio+"__FF_wjetsUp", FF_input)
                        
                    h_d[DR+tau_id+npreb+ratio] =  get(DR+tau_id+npreb+ratio, "",FF_input )
                    if syst:
                        h_d[DR+tau_id+npreb+ratio+"__FF_ttbarUp"] = get(DR+tau_id+npreb+ratio+"__FF_ttbarUp", "", FF_input)
                        h_d[DR+tau_id+npreb+ratio+"__FF_ttbarDown"] = get(DR+tau_id+npreb+ratio+"__FF_ttbarDown", "", FF_input)
                        h_d[DR+tau_id+npreb+ratio+"__FF_wjetsDown"] = get(DR+tau_id+npreb+ratio+"__FF_wjetsDown", "", FF_input)
                        h_d[DR+tau_id+npreb+ratio+"__FF_wjetsUp"] = get(DR+tau_id+npreb+ratio+"__FF_wjetsUp", "", FF_input)
                    # h_d[DR+tau_id+npreb+ratio].Draw()
                    # c.Print(input_path + '/' + DR+tau_id+npreb+ratio + '.png' ) 
    return h_d
def write_FF_f(h_d, FF_output, syst = False):
    for DR in cut_dic:
        for npreb in nprebjets_dic:
            for ratio in ratio_dic:
                if syst: 
                    syst_list = ["","__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsDown","__FF_wjetsUp"  ]
                else:
                    syst_list = [""]
                for sys in syst_list:
                    num = h_d[DR+'ID'+npreb+ratio+sys]
                    den = h_d[DR+'Anti'+npreb+ratio+sys]
                    # print(num, den)
                    FF = num.Clone()
                    FF.Divide(den)
                    FF_processed = remove_neg(FF)
                    # remove the negative bins in FF
                    FF_processed.SetMaximum(1.0)
                    FF_processed.SetMinimum(0)
                    write(FF_processed, f'FakeFactor/{DR}' ,'FF' + DR + var + npreb + ratio + sys, FF_output)  
def Fit_FF(DR, npreb, ratio,  var = 'pt_2', Produce_tot_stat_Syst = False, syst= ""):
    print(f"running for {'FF'+DR+var + npreb + ratio + syst}")
    if DR ==  "DR_ttbar" and npreb == "0preb":
        return 0
    # R.DisableImplicitMT() ## R.EnableImplicitMT() # I dont know why but it causes the TVirtualFitter.GetFitter() fail
    ## function to fit Fake factor. Save the fitted result to a TGraph in root file
    fnew = R.TFile.Open(input_path + '/FakeFactor.root', 'r')
    ff_h = get('FF'+DR+var + npreb + ratio + syst, f'FakeFactor/{DR}', fnew )
    for i in range(0, ff_h.GetNbinsX()+1):
        if ff_h.GetBinContent(i) > 1:
            ff_h.SetBinContent(i, 0)
    ff_original = ff_h.Clone()
    # print('FF'+DR+var + npreb + ratio + syst, 'FakeFactor/'+DR+'', fnew )
    bin_120 = ff_h.FindBin(130)
    bin_140 = ff_h.FindBin(180)
    bin_200 = ff_h.FindBin(300)
    bin_350 = ff_h.FindBin(400)
    
    # f1 = R.TF1('FF'+DR+var + npreb + ratio," [0]+[1]*x + [2]*x*x + [3]*x*x*x  ",30,140)
    # formular_string = " ({0}+{1}*x + {2}*x*x  + {3}*x*x*x  > 0?{0}+{1}*x + {2}*x*x  + {3}*x*x*x: 0 )".format(h_Fit.Parameter(0), h_Fit.Parameter(1),  h_Fit.Parameter(2),h_Fit.Parameter(3))
    # ff_h is a defined histogram
    hint = ff_h.Clone()
    
    f1 = R.TF1('FF'+DR+var + npreb + ratio + syst, " [2] + TMath::Landau(x, [0], [1], false)", -10, 10)
    h_Fit = ff_h.Fit(f1,"ESRQ","",30.0,140.0)

    ## this step calculates the error of one sigma
    R.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint)

    # Now the "hint" histogram has the fitted function values as the
    # bin contents and the confidence intervals as bin errors, we can directly use that 
    hint.SetStats(False)
    hint.SetFillColor(870)
    thr = 0.5
  
    # formular_string = " ({2}+TMath::Landau(x,{0},{1}, false) )".format(h_Fit.Parameter(0), h_Fit.Parameter(1),  h_Fit.Parameter(2))
    
    bin_120_value ,bin_120_error = ff_h.GetBinContent(bin_120), ff_h.GetBinError(bin_120)
    bin_140_value ,bin_140_error = ff_h.GetBinContent(bin_140), ff_h.GetBinError(bin_140)
    bin_200_value ,bin_200_error = ff_h.GetBinContent(bin_200), ff_h.GetBinError(bin_200)
    bin_350_value ,bin_350_error = ff_h.GetBinContent(bin_350), ff_h.GetBinError(bin_350)
    for i in range(0, ff_h.GetNbinsX()+1):
        if ff_h.GetBinContent(i) > 1:
            ff_h.SetBinContent(i, 0)
    def SetValueError(h, bin, value, error, toEnd =False):
        h.SetBinContent(bin, value)
        h.SetBinError(bin, error)
        if toEnd: 
            for i in range(bin+1, h.GetNbinsX()+1):
                h.SetBinContent(i, value)
                h.SetBinError(i, error)
        return h
    if bin_140_value and bin_140_error :
        if bin_140_error / bin_140_value < thr:
            if bin_200_value:
                if bin_200_error / bin_200_value < thr :
                    if bin_350_value:
                        if bin_350_error / bin_350_value < thr:
                            # f2 = R.TF1("f2","x < 140 ? {0} : x < 200?  {1} :   x < 350? {2} : {3}".format(
                            #     formular_string, bin_140_value,bin_200_value, bin_350_value
                        # ),30, 2000)
                            hint = SetValueError(hint,bin_140, bin_140_value,bin_140_error)
                            hint = SetValueError(hint,bin_200, bin_200_value,bin_200_error)
                            if bin_350_value > 0.5:
                                hint = SetValueError(hint,bin_200, bin_200_value,bin_200_error, True)
                            else:
                                hint = SetValueError(hint,bin_350, bin_350_value,bin_350_error,True)
                            print("I am here 1")
                        else:
                            # f2 = R.TF1("f2","x < 140 ? {0} : x< 200? {1} :{2}".format(
                            #     formular_string, bin_140_value, bin_200_value                     
                        # ),30, 2000)
                            hint = SetValueError(hint,bin_140, bin_140_value,bin_140_error)
                            hint = SetValueError(hint,bin_200, bin_200_value,bin_200_error,True)
                            print("I am here 2")
                    else:
                            # f2 = R.TF1("f2","x < 140 ? {0} : x< 200? {1} :{2}".format(
                            #     formular_string, bin_140_value, bin_200_value    ),30, 2000)
                            
                            hint = SetValueError(hint,bin_140, bin_140_value,bin_140_error)
                            hint = SetValueError(hint,bin_200, bin_200_value,bin_200_error,True)
                            print("I am here 3")
                            
                else:
                    # f2 = R.TF1("f2","{0}  ".format(
                    #     formular_string, bin_140_value
                    # ),30, 2000)   
                    # # hint = SetValueError(hint,bin_140, bin_140_value,bin_140_error,True)
                    hint = SetValueError(hint,bin_140, bin_140_value,bin_140_error,True)
                    print("I am here 4")
                    
            else:
                # f2 = R.TF1("f2","x < 140 ? {0}  :{1}".format(
                #         formular_string, bin_140_value
                #     ),30, 2000)  
                hint = SetValueError(hint,bin_140, bin_140_value,bin_140_error,True)
                print("I am here 5")
        else:
            if bin_200_value:
                if bin_200_error / bin_200_value < thr:
                    if bin_350_value:
                        if bin_350_error / bin_350_value < thr:
                            # f2 = R.TF1("f2","x < 200 ?  {0} :x< 350?  {1} : {2}".format(
                            #     formular_string,bin_200_value,bin_350_value
                            # ),30, 2000)
                            hint = SetValueError(hint,bin_200, bin_200_value,bin_200_error)
                            hint = SetValueError(hint,bin_350, bin_350_value,bin_350_error,True)
                            print("I am here 6")
                        else:
                            # f2 = R.TF1("f2","x < 200 ?  {0} :  {1}".format(
                            #     formular_string,bin_200_value
                            # ),30, 2000)
                            hint = SetValueError(hint,bin_200, bin_200_value,bin_200_error,True)
                            print("I am here 7")
                    else:
                        # f2 = R.TF1("f2","x< 350? {0} :{1}".format( 
                        #     formular_string, bin_350_value
                        # ),30, 2000)  
                        hint = SetValueError(hint,bin_350, bin_350_value,bin_350_error,True)
                        print("I am here 8")
                else:
                    # f2 = R.TF1("f2","{0} ".format( 
                    #         formular_string,bin_140_value
                    #     ),30, 2000)  
                    print("I am here 9")
            else: 
                # f2 = R.TF1("f2","x< 140? {0} :{1}".format( 
                #             formular_string,bin_140_value
                #         ),30, 2000)  
                if bin_140_value -bin_140_error   >0  and bin_140_error/ (bin_140_value + 0.001) < thr:
                    
                    hint = SetValueError(hint,bin_140, bin_140_value,bin_140_error,True)
                print("I am here 10")
    else:
        # f2 = R.TF1("f2"," {0}".format(
        #             formular_string
        #         ),30, 2000)        
        print("I am here 11")  
        if bin_120_value - bin_120_error >0:
            hint = SetValueError(hint,bin_120, bin_120_value,bin_120_error,True)
    
    ## We increase the error linearly for high pT bins
    ## the value of 1600 is picked , several different values are tried and 1600 gives good agreement with the actual bin errors
    for i in range(bin_120-1, hint.GetNbinsX()+2): 
        if hint.GetBinContent(i) > 0:
            if hint.GetBinError(i) < hint.GetBinCenter(i)/1600 * hint.GetBinContent(i): 
                    hint.SetBinError(i, hint.GetBinCenter(i)/1600 * hint.GetBinContent(i))
        else:
            hint.SetBinError(i, hint.GetBinCenter(i)/1600 * abs(hint.GetBinContent(i)))
    
    ## drawing and saving 
    dummy_hist = R.TH1F("dummy", ";pT;Fake Factor", 1, 40, 425)
    dummy_hist.SetStats(False)  # Turn off stats box
    actual_max = 0
    for bin in range(0, ff_h.GetNbinsX() + 1):
        bin_content = ff_h.GetBinContent(bin)
        if bin_content > actual_max:
            actual_max = bin_content
    dummy_hist.GetYaxis().SetRangeUser(0.,0.6 if actual_max > 0.25 else 0.3)
    
    c = R.TCanvas("p1", "p1", 1000,600)
    dummy_hist.Draw()
    hint.Draw("e3 same")
    ff_original.SetStats(False)
    ff_original.Draw('same')
    ## now save the fit result to TGraph        
    n_bins = hint.GetNbinsX()
    graph = R.TGraph(n_bins+1)
    if Produce_tot_stat_Syst:
        graph_up = R.TGraph(n_bins+1)
        graph_down = R.TGraph(n_bins+1)
        

    for bin in range(0, n_bins + 1):
        # For variable bin widths, use GetBinCenter to get the correct bin center
        bin_center = hint.GetBinCenter(bin)
        bin_content = hint.GetBinContent(bin)
        
        bin_err = hint.GetBinError(bin)
        
        graph.SetPoint(bin, bin_center, bin_content)
        if Produce_tot_stat_Syst:            
            bin_content_down = bin_content - bin_err if bin_content - bin_err >0  else 0
            bin_content_up = bin_content + bin_err if bin_content - bin_err < 1  else 1
            graph_down.SetPoint(bin, bin_center, bin_content_down )
            graph_up.SetPoint(bin, bin_center, bin_content_up )
    
    graph.GetXaxis().SetRangeUser(hint.GetXaxis().GetXmin(),hint.GetXaxis().GetXmax() )
    graph.SetPoint(n_bins+1, 1000, bin_content)
    graph.SetLineColor(910)
    graph.Draw("same")

    if Produce_tot_stat_Syst:
        graph_up.GetXaxis().SetRangeUser(hint.GetXaxis().GetXmin(),hint.GetXaxis().GetXmax() )
        graph_down.GetXaxis().SetRangeUser(hint.GetXaxis().GetXmin(),hint.GetXaxis().GetXmax() )
        graph_up.SetPoint(n_bins+1, 1000, bin_content_up)
        graph_down.SetPoint(n_bins+1, 1000, bin_content_down)

        graph_down.SetLineColor(860)
        graph_down.Draw("same")

        graph_up.SetLineColor(810)
        graph_up.Draw("same")

    # Create a TGraph from the histogram
    # Save the graph to a ROOT file
    output_file = R.TFile(f"{input_path}/FakeFactor_fitted.root", "UPDATE") if os.path.exists(f"{input_path}/FakeFactor_fitted.root") else  R.TFile(f"{input_path}/FakeFactor_fitted.root", "RECREATE")
    graph.Write(f"FF{DR}{var}{npreb}{ratio}{syst}")
    if Produce_tot_stat_Syst:
        graph_up.Write(f"FF{DR}{var}{npreb}{ratio}_FF_tot_StatUp")
        graph_down.Write(f"FF{DR}{var}{npreb}{ratio}_FF_tot_StatDown")
    output_file.Close()
    c.Print( input_path +'/FF'+DR+var + npreb + ratio + syst+'.png')
    fnew.Close()
def produce_fake(input_path, samples_list, systematics = [], save_DR = True ,index = 10):
    '''
    input_path, sample_list, final_string:dictionary of key DR names and values FF string
    produce fakes template in Anti ID regions and for each DRs
    in fact the selections for each DR is not applied here. Only the FF for each DR is applied
    '''
    samples = getall_list(input_path, samples_list)
    if not os.path.exists(f'{input_path}/tmpsamples_withW.root'):
        command = "hadd -f2 " + f'{input_path}/tmpsamples_withW.root' + " " + " ".join(samples)
        # Execute the command using os.system
        result = os.system(command)
        if result != 0:
            sys.exit(-1)
    if not os.path.exists(f'{input_path}/tmpsamples_withnoW.root'):
        samples_noW = getall_list(input_path, samples_list, exclude_wjets=True)
        command = "hadd -f2 " + f'{input_path}/tmpsamples_withnoW.root' + " " + " ".join(samples_noW)
        result = os.system(command)
        if result != 0:
            sys.exit(-1)
    print("using weight:  ",  f'({MC_weight})/{lumi}')
    # R.gDebug=3
    ## the lumi is divided only once here. Otherwise the normalisation is wrong
    df_withW = R.RDataFrame('ntuple', f'{input_path}/tmpsamples_withW.root').Filter(combinecut(Anti_ID,Htautau.lepton_veto, complete_lepton_selection)).Define('genWeight_tmp',  
        f'({MC_weight})/{lumi}') #.Redefine("genWeight_tmp", f" is_data == 0? genWeight_tmp/{lumi} :genWeight_tmp  ")
    df_noW = R.RDataFrame('ntuple', f'{input_path}/tmpsamples_withnoW.root').Filter(combinecut(Anti_ID,Htautau.lepton_veto, complete_lepton_selection)).Define('genWeight_tmp',  
        f'({MC_weight})/{lumi}') #.Redefine("genWeight_tmp", f" is_data == 0? genWeight_tmp/{lumi} :genWeight_tmp  ")
    df_data = R.RDataFrame('ntuple', getdata_list(input_path, samples_list)).Filter(combinecut(Anti_ID,Htautau.lepton_veto, complete_lepton_selection)).Define('genWeight_tmp',  
        f'({MC_weight})/{lumi}') #.Redefine("genWeight_tmp", f" is_data == 0? genWeight_tmp/{lumi} :genWeight_tmp  ")


    columns = list(df_data.GetColumnNames() )
    print("printing data list:   ", getdata_list(input_path, samples_list))
    print("printing data columns:      " , columns)
    output_column = columns
    ## many columns are not present in data, using only data columns to save
    systematics.insert(0,"") ##  add the nominal in the syst list, nominal is alaways run
    ## systematics example: _FF_tot_StatUp
    cpp_code_initial =f""" TFile* f_FakeFactor{index} = new TFile("{input_path}/FakeFactor_fitted.root");"""
    R.gInterpreter.Declare(cpp_code_initial)
    
    df_dict = {}
    DR_list = ['QCD'] if channel =="tt" else [ 'W','QCD','ttbar']
    for DR in DR_list:
        for syst in systematics:
            for npreb in nprebjets_dic:
                if DR == "ttbar":
                    if npreb == "0preb":
                        print("skipping ttbar FF for 0preb")
                        continue
                for ratio in ratio_dic:
                    # Construct the graph name
                    graph_name = f"FFDR_{DR}{var}{npreb}{ratio}{syst}"
                    
                    # Generate the C++ code for the interpolation function
                    cpp_code = f"""
                    
                    TGraph* graph_{npreb}_{ratio}_{DR}{syst}{index} = (TGraph*)f_FakeFactor{index}->Get("{graph_name}");
                    double interpolate_{npreb}_{ratio}_{DR}{syst}{index}(double x) {{
                        return graph_{npreb}_{ratio}_{DR}{syst}{index}->Eval(x);
                    }}
                    """
                    # print(cpp_code)
                    # Declare the function
                    R.gInterpreter.Declare(cpp_code)

            combined_weight_str = ""

            for npreb in nprebjets_dic:
                if DR == "ttbar":
                    if npreb == "0preb":
                        print("skipping ttbar FF string combination for 0preb")
                        continue
                for ratio in ratio_dic:
                    # Combine cuts and weights into a single string
                    if combined_weight_str != "":
                        combined_weight_str += " + "
                    combined_weight_str += f"({combinecut(nprebjets_dic[npreb], ratio_dic[ratio])}) * interpolate_{npreb}_{ratio}_{DR}{syst}{index}({var})"
            # print(f"combined_weight_str, {combined_weight_str}")
            if channel=="tt":
                df0= df_data ## in practice the MC subtaction leave a small gap in the SR. The MC subtraction is very small and shouldn't cause any difference
            else:
                df0 = df_noW if DR == "W" else df_withW
            if syst == "":
                if "FF_weight" not in df0.GetColumnNames():
                    df_dict[DR] = df0.Define("FF_weight", f"genWeight_tmp * ({combined_weight_str})" )
                else:
                    df_dict[DR] = df0.Redefine("FF_weight", f"genWeight_tmp * ({combined_weight_str})" )
                
                df_dict[DR] = df_dict[DR].Redefine(
                    'genWeight', "1.0f").Redefine('is_fake', 'true' ).Redefine("puweight", "double(1.0)")
                for w in MC_weight_list:
                    df_dict[DR] = df_dict[DR].Redefine(w, "1.0f")
                    df_dict[DR] = df_dict[DR].Redefine('id_wgt_tau_vsJet_Medium_2',  'double(1)')
                df_dict[DR] = df_dict[DR].Redefine('id_tau_vsJet_Medium_1' if channel == "tt" else 'id_tau_vsJet_Medium_2',  'int(1)')
                if channel == "tt":
                    df_dict[DR] = df_dict[DR].Redefine('id_wgt_tau_vsJet_Medium_1',  'double(1)')
                    #.Filter("genWeight != 0")
            else:
                ## set pt to -1 if weight is 0, pt if not equal to 0 for syst
                if f'FF_weight{syst}' not in df_dict[DR].GetColumnNames():
                    df_dict[DR] = df_dict[DR].Define(f'FF_weight{syst}', f"genWeight_tmp * ({combined_weight_str})" )
                else:
                    df_dict[DR] = df_dict[DR].Redefine(f'FF_weight{syst}', f"genWeight_tmp * ({combined_weight_str})" )
            #     df_dict[DR] = df_dict[DR].Define(f'{var}{syst}', f' FF_weight{syst} == 0.0? -1.0 : {var}')
                
            # ## set pt to -1 if weight is 0, pt if not equal to 0 for nominal
            # df_dict[DR] = df_dict[DR].Redefine(f'{var}', f' FF_weight == 0? -1.0 : {var}')
            
    for syst in systematics: 
        if f"FF_weight{syst}" not in output_column:
            output_column.append(f"FF_weight{syst}")
        # if f"{var}{syst}" not in output_column:
        #     output_column.append(f"{var}{syst}")
    
    for o in output_column:
        if o not in df_dict[DR].GetColumnNames():
            print(o, "not found!!!!!!!!!")
    for o in columns:
        if o not in df_dict[DR].GetColumnNames():
            print(o, "not found in data!!!!!!!!!")

        # print(output_column)
        # print(df_dict["QCD"].GetColumnNames())
        # df_dict["QCD"].Snapshot('ntuple', f'test.root', ['genWeight__FF_tot_StatUp'])
    
    DR_speical_cut = {'QCD': "1>0"} if channel =="tt" else {'W': Htautau.W_true_only, 'QCD' : "1>0",'ttbar': Htautau.ttbar_true_only}
    if save_DR:
        for DR in df_dict:
        # for DR in ["ttbar"]:            
            print("processing ",DR)
            # print("saving DR with columns:  ", output_column)
            print('checking output coloumn', output_column)
            for c in output_column:
                if str(c) not in df_dict[DR].GetColumnNames():
                    print(f'================   ERROR: {c} not in output column')
            # df_dict[DR].Filter(DR_speical_cut[DR]).Snapshot("ntuple", f"{input_path}/FF_{DR}.root", output_column)
            df_dict[DR].Filter(DR_speical_cut[DR]).Snapshot("ntuple", f"{input_path}/FF_{DR}.root")
            
            print(f"saving dataframe {DR} to FF_{DR}.root"  )
    return df_dict, output_column
def combine_Fakes(input_path, df_dict, columns,  apply_fraction = False, systematics = [], tag = ""):
    '''
    fraction: root file storing the fraction in mt_tot
    '''
    # for DR in ['DR_ttbar', 'DR_W', 'DR_QCD']: 
    # histogram name: wjets_ARtight_mTnobmt_tot
    # for DR in ["data", "wjets", "ttbar"]:    
    DRs = ["data"] if channel == "tt" else ["data", "wjets", "ttbar"]
    # DRs = ["data"] if channel == "tt" else ["wjets"]
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
            R.gROOT.LoadMacro('cpp_code/loadFF.C') # load FF histograms /or any other histograms into a dictionary called Weights with key [histname] 
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
    
    if channel != "tt": 
        in_file  = f"{input_path}/Fakes_mttot_tmp{tag}data.root {input_path}/Fakes_mttot_tmp{tag}wjets.root {input_path}/Fakes_mttot_tmp{tag}ttbar.root "
        # in_file  = f"{input_path}/Fakes_mttot_tmp{tag}wjets.root  "
    else:
        in_file  = f"{input_path}/Fakes_mttot_tmp{tag}data.root "
    os.system(f'hadd -f {input_path}/FF_Combined{tag}.root {in_file}')
def clousre_correction( run_double_correction = True, index = 1):
    ## produce closure correction for each channel.
    ## tt: correction bin in eta_1
    ## mt,et: correction bin in C_QCD, C_W
    
    c = R.TCanvas()
    h_n ={}
    h_d ={}
    df_num = {}
    df_den = {}
    corr = {}
    h_setting = {}
    if channel == "et":
        selection = combinecut( Htautau.et_triggers_selections[era],Htautau.electron_selections,Htautau.lepton_veto,Htautau.et_tau_selections[era])
    elif channel == "mt":
        selection = combinecut( Htautau.mt_triggers_selections[era],Htautau.muon_selections,Htautau.lepton_veto,Htautau.mt_tau_selections[era])
    elif channel == "em":
        selection = combinecut( Htautau.em_triggers_selections[era],Htautau.em_electron_selection,Htautau.em_muon_selection,Htautau.lepton_veto)
    elif channel == "tt":
        selection = combinecut( Htautau.tt_triggers_selections[era],Htautau.tt_secondtau_selections,Htautau.tt_leadingtau_selections,Htautau.lepton_veto)
    for DR in (["QCD"] if channel == "tt" else ["QCD", "W"]):
        ## for ttbar, I haven't figured out a way to correct    
        bins = 20
        if lumi < 10e3:
            bins= 20
        if channel =="tt":
            var =  "eta_1"
            h_setting[DR] = ( f"Correction;{var};Closure Correction", bins, -2.3, 2.3)
        else:
            var = f"C_{DR}"    
            var_2 = "pt_1"
            binning = [20,30,35,40,45,50,55,60,65,70,75,80,90,100,150] if DR =="W" else [20,30,35,40,45,50,55,60,70,80,120]
            # binning = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1,1.2,1.3,1.4,1.5,1.6] if DR =="W" else [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1,1.2,1.3,1.4,1.5,1.6]
            h_setting[DR] = ( f"Correction;{var};Closure Correction",bins,-2.5,2.) if DR == "QCD" else ( f"Correction;{var};Closure Correction",bins,-6,6)    
            h_setting[f"{DR}_pt_1"] = ( f"Correction;{var_2};Closure Correction",len(binning)-1, array.array('d', binning))
        exclude_w = True if DR=="W" else False
        samples = getall_list(input_path, samples_list, exclude_wjets=exclude_w)
        
        df_num[DR] = R.RDataFrame('ntuple', samples) 
        df_den[DR] = R.RDataFrame('ntuple', f"{input_path}/FF_{DR}.root") 
        if DR == "QCD":    
            df_num["QCD"] = df_num[DR].Filter(combinecut(DR_QCD, ID, selection)).Define('genWeight_tmp1',f'{MC_weight}')
            df_den["QCD"] = df_den[DR].Filter(combinecut(DR_QCD, ID, selection)).Define('genWeight_tmp1',f'FF_weight * {lumi} ')
            print(f"Finish getting QCD df, entries of QCD ID: {df_num['QCD'].Count().GetValue() }")
        if DR == "W":
            df_num["W"]= df_num[DR].Filter(combinecut('is_wjets < 1', DR_W, ID, selection )).Define('genWeight_tmp1',f'{MC_weight}')
            df_den["W"] = df_den[DR].Filter(combinecut('is_wjets < 1', DR_W, ID, selection )).Define('genWeight_tmp1',f'FF_weight * {lumi} ')
            print(f"Finish getting W df, entries of W ID: {df_num['W'].Count().GetValue() }")
    if run:
        closure_input  = R.TFile.Open('/'.join([input_path,'closure_input.root']), 'RECREATE' ) 
        for DR in df_num:
            print(f"generating histograms of {DR}")
            h_n[DR] = df_num[DR].Histo1D((f"input_num_{DR}",*h_setting[DR]),var, 'genWeight_tmp1')
            h_d[DR] = df_den[DR].Histo1D((f"input_den_{DR}",*h_setting[DR]),var, 'genWeight_tmp1')
            # write(h, directory, name,fout): "Write `h` to dir `directory` with name `name` in file `fout`"
            write(h_n[DR], "", f'closure_{DR}_num',closure_input)
            write(h_d[DR], "", f'closure_{DR}_den',closure_input)
            if channel != "tt" and run_double_correction:
                h_n[f"{DR}_pt_1"] = df_num[DR].Histo1D((f"input_num_{DR}_pt_1",*h_setting[f"{DR}_pt_1"]),var_2, 'genWeight_tmp1')
                h_d[f"{DR}_pt_1"] = df_den[DR].Histo1D((f"input_den_{DR}_pt_1",*h_setting[f"{DR}_pt_1"]),var_2, 'genWeight_tmp1')
                write(h_n[f"{DR}_pt_1"], "", f'closure_{DR}_pt_1_num',closure_input)
                write(h_d[f"{DR}_pt_1"], "", f'closure_{DR}_pt_1_den',closure_input)

    else:
        closure_input  = R.TFile.Open('/'.join([input_path,'closure_input.root']),'READ' ) 
        for DR in df_num:
            h_n[DR] =  get(f'closure_{DR}_num', "",closure_input )
            h_d[DR] =  get(f'closure_{DR}_den', "",closure_input )
            if channel != "tt" and run_double_correction:
                h_n[f"{DR}_pt_1"] =  get(f'closure_{DR}_pt_1_num', "",closure_input )
                h_d[f"{DR}_pt_1"] =  get(f'closure_{DR}_pt_1_den', "",closure_input )
    # Finished generate numerator and denominator
    
    # if run:
    closure_output  = R.TFile.Open('/'.join([input_path,'closure_corrections.root']),'RECREATE' ) 
    for DR in (["QCD"] if channel == "tt" else ["QCD", "W"]):
        if run:
            num = h_n[DR].GetValue()
            den = h_d[DR].GetValue()
            if channel != "tt" and run_double_correction:
                num_pt_1 = h_n[f"{DR}_pt_1"].GetValue()
                den_pt_1 = h_d[f"{DR}_pt_1"].GetValue()
        else:
            num = h_n[DR]
            den = h_d[DR]
            if channel != "tt" and run_double_correction:
                num_pt_1 = h_n[f"{DR}_pt_1"]
                den_pt_1 = h_d[f"{DR}_pt_1"]
        print(num, den, num.Integral(), den.Integral())
        
        closure = num.Clone()
        closure.Divide(den)
        corr[DR] = closure
        write(closure, '' ,f'closure_{DR}', closure_output)  
        if channel != "tt" and run_double_correction:
            closure_pt_1 = num_pt_1.Clone()
            closure_pt_1.Scale( den_pt_1.Integral()/closure_pt_1.Integral() )
            closure_pt_1.Divide(den_pt_1)
            closure_pt_1 = remove_neg(closure_pt_1)
            corr[f"{DR}_pt_1"] = closure_pt_1
            write(closure_pt_1, '' ,f'closure_{DR}_pt_1', closure_output)  


    # fit closure. Save the fitted result to a TGraph in root file
    output_file = R.TFile(f"{input_path}/closure_corrections_fitted.root", "UPDATE") if os.path.exists(f"{input_path}/closure_corrections_fitted.root") else  R.TFile(f"{input_path}/closure_corrections_fitted.root", "RECREATE")
    c = R.TCanvas("p1", "p1", 1000,600)
    c.cd()
    for DR in corr:
        ff_h = corr[DR]
        ff_original = ff_h.Clone()
        
        hint = ff_h.Clone()
        # f1 = R.TF1('closure_{DR}', " ([0] + [1] *x + [2] *x*x + [3] *x*x*x  + [4] *x*x*x*x) + [5] *x*x*x*x*x)", -2.1, 2.1)
        # h_Fit = ff_h.Fit(f1,"ESRQ","",-2.1,2.1)
        f_Fit = ff_h.Fit("pol6" ,"ESRQ", "",ff_h.GetXaxis().GetXmin(), ff_h.GetXaxis().GetXmax()) ## pol6 gives best result

        ## this step calculates the error of one sigma
        R.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint)

        # Now the "hint" histogram has the fitted function values as the
        # bin contents and the confidence intervals as bin errors, we can directly use that 
        ff_h.SetStats(False)
        hint.SetFillColor(870)
        
        ## drawing and saving 
        dummy_hist = R.TH1F( f"dummy_{DR}",*h_setting[DR])
        # dummy_hist = R.TH1F( "dummy",f"Correction;{var};Closure Correction", 20, -2.1, 2.1)
        dummy_hist.SetStats(False)  # Turn off stats box
        actual_max = 0
        for bin in range(0, ff_h.GetNbinsX() + 1):
            bin_content = ff_h.GetBinContent(bin)
            if bin_content > actual_max:
                actual_max = bin_content
        dummy_hist.GetYaxis().SetRangeUser(0., actual_max *1.5)
        dummy_hist.Draw()
        hint.Draw("e3 same")
        print(f"hint.Integral() {hint.Integral()}")
        # ff_original.SetStats(False)
        print(f"ff_original.Integral() {ff_original.Integral()}")
        ff_original.Draw('same')
        ## now save the fit result to TGraph        
        n_bins = hint.GetNbinsX()
        graph = R.TGraph(n_bins+1)
        
        for bin in range(0, n_bins + 1):
            # For variable bin widths, use GetBinCenter to get the correct bin center
            bin_center = hint.GetBinCenter(bin)
            bin_content = hint.GetBinContent(bin)    
            # bin_err = hint.GetBinError(bin)
            graph.SetPoint(bin, bin_center, bin_content)
            
        graph.GetXaxis().SetRangeUser(hint.GetXaxis().GetXmin(),hint.GetXaxis().GetXmax() )
        graph.SetLineColor(910)
        graph.Draw("same")

        # Create a TGraph from the histogram
        # Save the graph to a ROOT file
        
        graph.Write(f"closure_{DR}")
        c.Print( f'{input_path}/closure_correction_{DR}.png')
    output_file.Close()
    closure_output.Close()
    closure_input.Close()

    ## df_den is df containing the Fakes file
    cpp_code_initial =f""" TFile* f_closure{index} = new TFile("{input_path}/closure_corrections_fitted.root");"""
    R.gInterpreter.Declare(cpp_code_initial)
    df_dict = {}
    if run_double_correction:
        tag = "double_corrected"
    else:
        tag = "closure_corrected"
    for DR in (['QCD'] if channel =="tt" else ['W', 'QCD']):
            df_dict[DR] =R.RDataFrame('ntuple', f"{input_path}/FF_{DR}.root") 
            # Construct the graph name
            graph_name = f"closure_{DR}"
            # Generate the C++ code for the interpolation function
            cpp_code = f"""
            
            TGraph* graph_closure_{DR}{index} = (TGraph*)f_closure{index}->Get("{graph_name}");
            double interpolate_closure_{DR}{index}(double x) {{
                return graph_closure_{DR}{index}->Eval(x);
            }}

            """
            # Declare the function
            R.gInterpreter.Declare(cpp_code)
            weight_str = f"interpolate_closure_{DR}{index}({var})"
            if channel != "tt" and run_double_correction:
                ## additional corrections applied for pt_1
                graph_name = f"closure_{DR}_pt_1"
                cpp_code = f"""    
                TGraph* graph_closure_{DR}{index}_pt_1 = (TGraph*)f_closure{index}->Get("{graph_name}");
                double interpolate_closure_{DR}{index}_pt_1(double x) {{
                    return graph_closure_{DR}{index}_pt_1->Eval(x);
                }}

                """
                R.gInterpreter.Declare(cpp_code)
                weight_str = f"(interpolate_closure_{DR}{index}({var}) * interpolate_closure_{DR}{index}_pt_1(pt_1))"
            if "FF_weight" not in df_dict[DR].GetColumnNames():
                print("ERROR:   FF_weight not found")
                sys.exit(-1)
            else:
                df_dict[DR] = df_dict[DR].Define("FF_weight_tmp", "FF_weight").Define(
                    "FF_weight__FF_closureDown", f"FF_weight").Define(
                    "FF_weight__FF_closureUp",   f"FF_weight * ({weight_str}) * ({weight_str})"  ) ## multiply two times for up, no for down
                df_dict[DR] = df_dict[DR].Redefine("FF_weight", f"FF_weight_tmp * ({weight_str})" )
                for s in ["__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown"]:
                    df_dict[DR] = df_dict[DR].Redefine(f"FF_weight{s}", f"FF_weight{s} * ({weight_str})" )
            
            # print(weight_str)
            df_dict[DR] = df_dict[DR].Define("Closure_corrected", "int(1)")
            # .Define(
            #     f'pt_1_FF_closureDown', f' FF_weight__FF_closureDown == 0? -1.0f : pt_1').Define(
            #     f'pt_1_FF_closureUp', f' FF_weight__FF_closureUp == 0? -1.0f : pt_1').Redefine(
            #     f'pt_1', f' FF_weight == 0? -1.0f : pt_1')
            
            df_dict[DR].Snapshot("ntuple", f"{input_path}/FF_{DR}_{tag}.root")
    if channel != "tt" :
        df_dict["ttbar"]= R.RDataFrame('ntuple', f"{input_path}/FF_ttbar.root").Define(
            "Closure_corrected", "int(1)").Define(
            "FF_weight__FF_closureDown", f"FF_weight").Define(
            "FF_weight__FF_closureUp", f"FF_weight").Define(
            "FF_weight_tmp", f"FF_weight")
            # .Define(
            # 'pt_1_FF_closureDown', "pt_1").Define(
            # 'pt_1_FF_closureUp', "pt_1").


    

    columns = list(df_dict["QCD"].GetColumnNames())
    combine_Fakes(input_path,df_dict,columns, True, ["__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown", "__FF_closureDown", "__FF_closureUp" ], tag = tag)


if __name__ == '__main__':        
    
    if run:
        df_d = get_df(input_path, samples_list) # acquire dataframe 
    else:
        df_d = 0
        
    FF_input  = R.TFile.Open('/'.join([input_path,'FF_input.root']), 'RECREATE' if run else 'READ' ) 
    h_n = get_FF_f(df_d, FF_input,run, syst=True) # acquire histogram, save them in FakeFactor.root. if run, this functions will get the histograms from the dataframe; else get it from existing FF_input.root
    FF_output = R.TFile.Open('/'.join([input_path,'FakeFactor.root']), 'RECREATE' ) 
    write_FF_f(h_n, FF_output, syst=True) # save the calculated FF from the last step in FakeFactor.root 
    FF_input.Close()
    FF_output.Close()
    R.DisableImplicitMT() ## R.EnableImplicitMT() # I dont know why but it causes the TVirtualFitter.GetFitter() fail
    i = 10
    for DR in cut_dic:
        for npreb in nprebjets_dic:
                for ratio in ratio_dic:
                    Fit_FF(DR,npreb, ratio,  var,Produce_tot_stat_Syst = True, syst="") ## Produce FF_tot_stat systematics
                    for sys in ["__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsDown","__FF_wjetsUp"  ]:
                        Fit_FF(DR,npreb, ratio,  var,Produce_tot_stat_Syst = False, syst= sys) ## Produce FF_ttbar, FF_Wjets systematics
    # if produce_final_fakes :
        # produce the fakes
    for DR in cut_dic:  
        # df_dict, columns = produce_fake(input_path, samples_list, [])
        df_dict, columns = produce_fake(input_path, samples_list, [
            "__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown"
            ], save_DR = True, index =i)
        i+=1 
        #    always save_DR , the output is needed by the closure corrections
        combine_Fakes(input_path,df_dict,columns, True,["__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown"] )

    # if run:
    # R.DisableImplicitMT() ##  R.EnableImplicitMT() # I dont know why but it causes the TVirtualFitter.GetFitter() fail
    clousre_correction(run_double_correction=False , index=1)
    os.system(f"mkdir -p {input_path}_corrected/")
    os.chdir(f"{input_path}_corrected/")
    os.system(f'ln -s ../{input_path}/* .')
    os.system(f'mv FF* bkp')
    os.chdir(f"..")
    print(os.getcwd())
    print("moving files to single corrected folder")
    os.system(f'mv {input_path}/FF_*closure*root {input_path}_corrected/')  
    os.system(f'mv {input_path}_corrected/FF_Combinedclosure_corrected.root {input_path}_corrected/FF_Combined.root')  
    os.system(f'mv {input_path}_corrected/FF_QCD_closure_corrected.root {input_path}_corrected/FF_QCD.root')  
    os.system(f'mv {input_path}_corrected/FF_ttbar_closure_corrected.root {input_path}_corrected/FF_ttbar.root')  
    os.system(f'mv {input_path}_corrected/FF_W_closure_corrected.root {input_path}_corrected/FF_W.root')  
    os.system(f'mv {input_path}_corrected/bkp/FF_ttbar.root {input_path}_corrected/')  
    if channel != "tt":
        # after running the previous block, run the second block
        clousre_correction(run_double_correction=True, index=2 )
        os.system(f"mkdir -p {input_path}_double_corrected/")
        os.chdir(f"{input_path}_double_corrected/")
        os.system(f'ln -s ../{input_path}/* .')
        os.system(f'mv FF* bkp')
        os.chdir(f"..")
        print(os.getcwd())
        # print("moving files to double corrected folder")
        os.system(f'mv {input_path}/FF_*double_corrected*root {input_path}_double_corrected/')  
        os.system(f'mv {input_path}_double_corrected/FF_Combineddouble_corrected.root {input_path}_double_corrected/FF_Combined.root')  
        os.system(f'mv {input_path}_double_corrected/FF_QCD_double_corrected.root {input_path}_double_corrected/FF_QCD.root')  
        os.system(f'mv {input_path}_double_corrected/FF_ttbar_double_corrected.root {input_path}_double_corrected/FF_ttbar.root')  
        os.system(f'mv {input_path}_double_corrected/FF_W_double_corrected.root {input_path}_double_corrected/FF_W.root')  
        # os.system(f'mv {input_path}_double_corrected/bkp/FF_ttbar.root {input_path}_double_corrected/')  