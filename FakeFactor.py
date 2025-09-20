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
R.TH1.SetDefaultSumw2(True)
R.gROOT.SetBatch(True)

input_path = str(sys.argv[1]) # '2016postVFP_et'
channel = str(sys.argv[2])
era = str(sys.argv[3])
print(input_path, channel)

Htautau = Htautau_selections()
if channel == "tt":
    true_MC_only=Htautau.true_MC_only_tt
else:
    true_MC_only=Htautau.true_MC_only_lt
DR_QCD= Htautau.DR_QCD_tt if channel == "tt" else Htautau.DR_QCD_lt
DR_W= Htautau.DR_W
DR_ttbar=  Htautau.DR_ttbar
if channel == "tt":
    ID = combinecut(Htautau.ID_tt,  Htautau.DR_deeptau_selections[channel])
    Anti_ID = combinecut(Htautau.Anti_ID_tt,Htautau.DR_deeptau_selections[channel])
else:
    ID = combinecut(Htautau.ID_lt,Htautau.DR_deeptau_selections[channel]  ) # 
    Anti_ID = combinecut(Htautau.Anti_ID_lt,Htautau.DR_deeptau_selections[channel])

luminosities = {
    "2016preVFP": 15.1158e3,
    "2016postVFP": 10.0093e3,
    "2017": 41.5e3,
    "2018": 59.8e3,
    "2022EE":8.077009684e3,
    "2022postEE":  26.671609707e3,
    "2023": 0.641474303e3 + 18.062659111e3, # B + C
    "2023BPix": 9.693130053e3, # D 
     }
lumi = luminosities[era]


MC_weight_list = ["genWeight", "btag_weight",  "trg_wgt_ditau_crosstau_2", "genEventSumW" , "Xsec", "ZPtMassReweightWeight"]  # "id_wgt_tau_vsJet_Medium_2",
if channel == "et":
    lepton_selection = combinecut(Htautau.et_triggers_selections[era],Htautau.electron_selections_FF,Htautau.lepton_veto,"mt_1 >0 && jpt_1 > -99 ")
    complete_lepton_selection = lepton_selection
    var = "pt_2"
    MC_weight =  f'(is_data == 0?  (-1) * Xsec * {lumi}* puweight * genWeight/genEventSumW     *  btag_weight   * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30  * id_wgt_tau_vsEle_Tight_2  :  float(1.0))' # * id_wgt_tau_vsJet_Medium_2 
    MC_weight_list.extend(["id_wgt_ele_wpTight" , "id_wgt_tau_vsEle_Tight_2", 'trg_wgt_single_ele30'])
elif channel == "mt":
    lepton_selection = combinecut(Htautau.muon_selections,Htautau.lepton_veto,Htautau.mt_triggers_selections[era],"mt_1 >0 && jpt_1 > -99 ")  ## 
    complete_lepton_selection  = lepton_selection
    var = "pt_2"
    MC_weight =  f'(is_data == 0? (-1) * Xsec   * {lumi} * puweight * genWeight/genEventSumW *  btag_weight   * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1 :  float(1.0) )' #  id_wgt_tau_vsJet_Medium_2 * 
    MC_weight_list.extend(["iso_wgt_mu_1", "id_wgt_mu_1"])
elif channel == "tt":
    lepton_selection = combinecut(Htautau.tt_triggers_selections[era],Htautau.tt_secondtau_selections,Htautau.lepton_veto, "mt_1 >0 && jpt_1 > -99 ")
    # lepton_selection = combinecut(Htautau.tt_secondtau_selections,Htautau.lepton_veto)
    # lepton_selection = combinecut(Htautau.lepton_veto)
    complete_lepton_selection = combinecut(Htautau.tt_secondtau_selections,Htautau.lepton_veto, Htautau.tt_triggers_selections[era], "mt_1 > 0 && jpt_1 > -99 ")
    var = "pt_1"
    MC_weight =  f'(is_data == 0?  (-1) * Xsec *  {lumi}* puweight * genWeight/genEventSumW *    btag_weight   * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 : float(1.0))' # *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1  *
    MC_weight_list.extend([ "trg_wgt_ditau_crosstau_1", "trg_wgt_ditau_crosstau_2"]) # "id_wgt_tau_vsJet_Medium_1",
else:
    exit("wrong channel provided")

print(input_path, channel)



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
                    # h.SetBinError(x,0)
    return h 
def get_bin_uncertainty(hist, bin_index):
    content = hist.GetBinContent(bin_index)
    error = hist.GetBinError(bin_index)
    if content == 0:
        return 0
    return abs(error) / abs(content)
import array

def rebin_histograms(hist1, hist2, low_stats=False):
    nbins = hist1.GetNbinsX()

    bins_to_merge = []
    current_bin = nbins
    threshold =  [0.1,0.2,0.5] if low_stats else [0.03, 0.05,0.2]   #[0.1, 0.3, 0.5]
    while current_bin > 1:
        x_value = hist1.GetBinCenter(current_bin)

        # Set max_uncertainty depending on x value
        
        if x_value < 100:
            max_uncertainty = threshold[0]
        elif x_value < 140:
            max_uncertainty =threshold[1]
        else:
            max_uncertainty = threshold[2]

        uncertainty1 = get_bin_uncertainty(hist1, current_bin)
        uncertainty2 = get_bin_uncertainty(hist2, current_bin)

        # Calculate combined uncertainty
        combined_uncertainty = (uncertainty1**2 + uncertainty2**2)**0.5

        # Check if bins need to be merged
        if (
            combined_uncertainty > max_uncertainty
            or (hist2.GetBinContent(current_bin) == 0.0 and hist2.GetBinError(current_bin) == 0.0)
            or (hist1.GetBinContent(current_bin) == 0.0 and hist1.GetBinError(current_bin) == 0.0) ## numerator can be 0
            or (hist1.GetBinContent(current_bin) /hist2.GetBinContent(current_bin) <= 0.0   )
        ):
            if current_bin > 1:
                # Define new bin edges
                new_bin_edges = [
                    hist1.GetBinLowEdge(bin)
                    for bin in range(1, hist1.GetNbinsX() + 2)
                    if bin != current_bin
                ]
                bins_to_merge.append(current_bin)
                rebin_edges = array.array('d', sorted(set(new_bin_edges)))
                
                # Rebin the histograms
                hist1 = hist1.Rebin(len(rebin_edges) - 1, hist1.GetName(), rebin_edges)
                hist2 = hist2.Rebin(len(rebin_edges) - 1, hist2.GetName(), rebin_edges)

        current_bin -= 1

    return hist1, hist2

def getall_list(input_path,  LO_DY = True):
    '''
    get all samples names in input_path, default to exclude embedding, FF and signal files and include Wjets samples
    '''
    inputfile = []
    for fname in os.listdir(input_path):
        if '.root' not in fname or 'FakeFactor' in fname or 'output' in fname or 'input' in fname or 'Fakes' in fname or "closure" in fname or "Closure" in fname or "pnn" in fname or "tmpsamples" in fname or "correction" in fname:
            continue
        if  'Embedding' in fname :
                continue
        if  'FF' in fname :
                continue
        if ("SUSY" in fname) or ("Xtohh" in fname) or ("2HDM-II" in fname) or ("2HDM" in fname) or ("BBHto2Tau" in fname):
                continue
        if not LO_DY:
            if "DYto2L" in fname:
                continue
        else:
            if "DYto2Tau_MLL" in fname or "DYto2Mu_MLL" in fname or  "DYto2E_MLL" in fname:
                continue
        inputfile.append(input_path + '/' + fname)
    return inputfile
def getdata_list(input_path):
    inputfile = []
    for fname in os.listdir(input_path):
        if "Run202" not in fname:
            continue
        
        inputfile.append(input_path + '/' + fname)
    return inputfile

def get_df(input_path, save_ttbar_data=False, save_fraction=False):
    R.TH1.SetDefaultSumw2(True)
    df_d = {}
    print(combinecut(DR_QCD, ID, lepton_selection))
    # binning = [30,40,50,60,70,80,90,100,120,140,200,350,500]
    samples = getall_list(input_path)
    
    samples_data = getdata_list(input_path)
    
    print(samples_data)
    df0 = R.RDataFrame('ntuple', samples) 
    df_data = R.RDataFrame('ntuple',samples_data )
    print(f"Finish getting df, entries : {df0.Count().GetValue() }")
    print("QCD Fakes samples",samples)
    # df_d['DR_QCDID'] = df_onlyW.Filter(combinecut(DR_QCD, ID, lepton_selection)).Define('genWeight_tmp',f'{MC_weight}')
    # df_d['DR_QCDAnti'] = df_onlyW.Filter(combinecut(DR_QCD, Anti_ID, lepton_selection)).Define('genWeight_tmp',f'{MC_weight}')
    df_d['DR_QCDID'] = df0.Filter(combinecut(DR_QCD, ID, lepton_selection, true_MC_only)).Define('genWeight_tmp',f'{MC_weight}')
    df_d['DR_QCDAnti'] = df0.Filter(combinecut(DR_QCD, Anti_ID, lepton_selection, true_MC_only)).Define('genWeight_tmp',f'{MC_weight}')
    print(f"Finish getting QCD df, entries of QCD ID: {df_d['DR_QCDID'].Count().GetValue() }")
    print(f"Finish getting QCD df, entries of QCD Anti ID: {df_d['DR_QCDAnti'].Count().GetValue() }")

    if channel == "tt":
        ## for tt channel, only need to proceed QCD DR
        return df_d

    df_ttbar0 = R.RDataFrame('ntuple', input_path+'/TT*root') ## for ttbar, fakes are small, using only MC to calculate 
    # print(f"Finish getting ttbar df, entries : {df_ttbar0.Count().GetValue() }")
    if save_ttbar_data:
        ## keep data with ttbar MC together
        df_d['DR_ttbarID']   = df0.Filter(combinecut('(  ( gen_match_2 != 6 && is_ttbar>0 ) || (is_ttbar <1)  )', DR_ttbar, ID , lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
        df_d['DR_ttbarAnti'] = df0.Filter(combinecut('(  ( gen_match_2 != 6 && is_ttbar>0 ) || (is_ttbar <1)  )', DR_ttbar,Anti_ID, lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
    else:
        ## using only MC to calculate 
        df_d['DR_ttbarID']   = df_ttbar0.Filter(combinecut('gen_match_2 ==  6','is_ttbar >= 1', DR_ttbar, ID,  lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
        df_d['DR_ttbarAnti'] = df_ttbar0.Filter(combinecut('gen_match_2 ==  6','is_ttbar >= 1', DR_ttbar, Anti_ID,  lepton_selection)).Define('genWeight_tmp',  f'{MC_weight}')
        # print(f"Finish getting ttbar df,  {df_ttbar0.Count().GetValue() }")
        # print(f"Finish getting ttbar df, entries of ttbar ID: {df_d['DR_ttbarID'].Count().GetValue() }")
        # print(f"Finish getting ttbar df, entries of ttbar AntiID: {df_d['DR_ttbarAnti'].Count().GetValue() }")
    df_d['DR_WID']   = df0.Filter(combinecut(true_MC_only, DR_W, ID, lepton_selection )).Define('genWeight_tmp',f'{MC_weight}')
    df_d['DR_WAnti'] = df0.Filter(combinecut(true_MC_only, DR_W, Anti_ID, lepton_selection )).Define('genWeight_tmp',f'{MC_weight}')
    # print(f"Finish getting df, entries : {df_noW.Count().GetValue() }")
    # print(f"Finish getting W df, entries of W Anti ID: {df_d['DR_WAnti'].Count().GetValue() }")
    # print(f"Finish getting W df, entries of W ID: {df_d['DR_WID'].Count().GetValue() }")

    
    return df_d
def get_FF_f(df_d, FF_input,run =False, syst = False):
    R.TH1.SetDefaultSumw2(True)
    h_d = {}
    #r = [30,40,50,60,70,80,90,100,120,140,200,350]
    # binning = [30,40,50,60,70,80,90,100,120,140,200,350,500]
    # if lumi < 10e3:
    #     binning = [30,40,50,70,90,120,150,200,500]
    c = R.TCanvas()
    for DR in cut_dic:
        if DR == "DR_QCD" or lumi < 10e3:
            # binning = [30,35,40,45,50,55,60,70,80,100,120,140,200,400]
            binning = ('FF_h', 'FF_h' ,74,30,400)
            if channel =="tt":
                # binning = [35,45,50,55,60,65,70,80,90,100,120,140,200,400]
                binning = ('FF_h', 'FF_h' ,73,35,400)
        else:
            # binning = [30,35,40,45,50,55,60,70,80,100,120,140,200,400]
            binning = ('FF_h', 'FF_h' ,74,30,400)
        for tau_id in ID_dic: 
            for npreb in nprebjets_dic:
                for ratio in ratio_dic:
                    if run:
                        # h_d[DR+tau_id+npreb+ratio] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, 'genWeight_tmp')
                        h_d[DR+tau_id+npreb+ratio] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Histo1D(binning,var, 'genWeight_tmp')
                        if syst: 
                            ## logic for ttbar / wjets stat up/down
                            #if is_ttbar: # up: redefine genWeight_tmp = genWeight_tmp * 1.4 # down: redefine genWeight_tmp =  genWeight_tmp * 0.6
                            #if is_wjets: # up: redefine genWeight_tmp = genWeight_tmp * 1.2 # down: redefine genWeight_tmp = genWeight_tmp * 0.8
                            # h_d[DR+tau_id+npreb+ratio+"__FF_ttbarUp"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_ttbarUp", "is_ttbar? 1.4 * genWeight_tmp : genWeight_tmp ").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_ttbarUp")
                            # h_d[DR+tau_id+npreb+ratio+"__FF_ttbarDown"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_ttbarDown", "is_ttbar? 0.6 * genWeight_tmp : genWeight_tmp").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_ttbarDown")
                            # h_d[DR+tau_id+npreb+ratio+"__FF_wjetsDown"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_wjetsDown", "is_wjets? 1.2 * genWeight_tmp : genWeight_tmp").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_wjetsDown")
                            # h_d[DR+tau_id+npreb+ratio+"__FF_wjetsUp"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_wjetsUp", "is_wjets? 0.8 * genWeight_tmp : genWeight_tmp").Histo1D(('FF_h', 'FF_h' ,len(binning)-1, array.array('d', binning)),var, DR+tau_id+npreb+ratio+"__FF_wjetsUp")

                            h_d[DR+tau_id+npreb+ratio+"__FF_ttbarUp"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_ttbarUp", "is_ttbar? 1.4 * genWeight_tmp : genWeight_tmp ").Histo1D( binning,var, DR+tau_id+npreb+ratio+"__FF_ttbarUp")
                            h_d[DR+tau_id+npreb+ratio+"__FF_ttbarDown"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_ttbarDown", "is_ttbar? 0.6 * genWeight_tmp : genWeight_tmp").Histo1D( binning,var, DR+tau_id+npreb+ratio+"__FF_ttbarDown")
                            h_d[DR+tau_id+npreb+ratio+"__FF_wjetsDown"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_wjetsDown", "is_wjets? 1.2 * genWeight_tmp : genWeight_tmp").Histo1D( binning,var, DR+tau_id+npreb+ratio+"__FF_wjetsDown")
                            h_d[DR+tau_id+npreb+ratio+"__FF_wjetsUp"] = df_d[DR+tau_id].Filter(combinecut(ID_dic[tau_id], nprebjets_dic[npreb], ratio_dic[ratio])).Define(DR+tau_id+npreb+ratio+"__FF_wjetsUp", "is_wjets? 0.8 * genWeight_tmp : genWeight_tmp").Histo1D( binning,var, DR+tau_id+npreb+ratio+"__FF_wjetsUp")
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
    binning_1 = [30,35,40,45,50, 55,60,65,70,80,90,100, 120,150,200,400]
    binning_2 = [30,35,40,45,50,60,80,100, 120,150,400]
    binning_3 = [30,40,50,80,120, 150,400]
    binning_dict = {
        "0" : binning_1,
        "1p25" : binning_2,
        "1p5" : binning_3,
    }
    
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
                    # if DR != "DR_ttbar":
                        
                    #     num = remove_neg(num)
                    #     den = remove_neg(den)
                    if DR == "DR_QCD" and channel != "tt":  

                        rebin_edges = array.array('d', sorted(set(binning_dict[ratio])))
                        num = num.Rebin(len(rebin_edges) - 1, num.GetName(), rebin_edges)
                        den = den.Rebin(len(rebin_edges) - 1, den.GetName(), rebin_edges)
                        # num, den = rebin_histograms(num, den,True)
                    else:
                        # num, den = rebin_histograms(num, den,False)
                        
                        rebin_edges = array.array('d', sorted(set(binning_dict[ratio])))
                        num = num.Rebin(len(rebin_edges) - 1, num.GetName(), rebin_edges)
                        den = den.Rebin(len(rebin_edges) - 1, den.GetName(), rebin_edges)
                    # print(num, den)
                    FF = num.Clone()
                    FF.Divide(den)
                    # FF_processed = remove_neg(FF)
                    # remove the negative bins in FF
                    # FF_processed.SetMaximum(1.0)
                    # FF_processed.SetMinimum(0)

                    FF_processed = FF
                    write(FF_processed, f'FakeFactor/{DR}' ,'FF' + DR + var + npreb + ratio + sys, FF_output)  
def Fit_FF(DR, npreb, ratio,  var = 'pt_2', Produce_tot_stat_Syst = False, syst= ""):
    R.TH1.SetDefaultSumw2(True)
    print(f"running for {'FF'+DR+var + npreb + ratio + syst}")
    if DR ==  "DR_ttbar" and npreb == "0preb":
        return 0
    ## function to fit Fake factor. Save the fitted result to a TGraph in root file
    fnew = R.TFile.Open(input_path + '/FakeFactor.root', 'r')
    ff_h = get('FF'+DR+var + npreb + ratio + syst, f'FakeFactor/{DR}', fnew )
    # for i in range(0, ff_h.GetNbinsX()+1):
    #     if ff_h.GetBinContent(i) > 1:
    #         ff_h.SetBinContent(i, 0)
    # ff_h = remove_neg(ff_h)
    ff_original = ff_h.Clone()
  
    ff_h = ff_h.Clone()
    
    f1 = R.TF1('f1', " [2] + TMath::Landau(x, [0], [1], false) + [3] *x " ,30, 400)
    # f2 = R.TF1('FF1'+DR+var + npreb + ratio + syst, " [2] + TMath::Landau(x, [0], [1], false)",30, 120)
    R.TVirtualFitter.SetPrecision(1e-6)
    R.TVirtualFitter.SetMaxIterations(10000)
    f1.SetParameter(0, 1.0)
    f1.SetParameter(1, 1.0)
    f1.SetParameter(2, 1.0)

    if ff_h.GetNbinsX() > 4 or channel == "tt":
        # repeat fit up to 100 times until the fit converges properly
        rep = True
        count = 0
        bad_fit =False
        error_thresold = 6 if channel == "tt" else 1
        while rep:
            h_Fit = ff_h.Fit("f1",'NSR')
            rep = int(h_Fit) != 0
            n_params = f1.GetNpar()  # Get the number of parameters in the function
            if not rep or count>10:
                # ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(h_uncert, 0.68)
                fit = f1
                for i in range(n_params):
                    param_value = fit.GetParameter(i)
                    param_error = fit.GetParError(i)
                    print("first fit: Parameter {}: Value = {}, Error = {}".format(i, param_value, param_error))
                    
                    if abs(param_error/param_value) > error_thresold or  param_value==0.0 or param_error==0.0: 
                        bad_fit = True
                break
            count+=1
        
        count = 0
        rep = True
        bad_fit_2 = False
        if  bad_fit:
            # bad_fit =False
            print("Fit failed, trying shorter range for fit")
            f2 = R.TF1('f2', "pol2" ,30, 150)
            f3 = R.TF1('f3', "pol0", 150,400)
            while rep:
                h_Fit = ff_h.Fit("f2",'NSR')
                ff_h2 = ff_h.Clone()
                n_params = f2.GetNpar() 
                rep = int(h_Fit) != 0
                fit = f2
                if not rep or count>10:
                    # ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(h_uncert, 0.68)
                    fit = f2
                    for i in range(n_params):
                        param_value = f2.GetParameter(i)
                        param_error = f2.GetParError(i)
                        if param_value==0.0 or param_error==0.0:
                            bad_fit_2 = True
                        if abs(param_error/param_value) > 5. or  param_value==0.0 or param_error==0.0: 
                            bad_fit_2 = True
                    break
                count+=1
        if  bad_fit_2:
            print("Fit failed again, trying pol1 for fit")
            f3 = R.TF1('f3', " pol1 " ,30, 150)
            h_Fit = ff_h.Fit("f3",'NSR')
            fit = f3
            
        fit.SetName(ff_h.GetName()+'_fit')
        fit.Print("all")
        print(str(fit.GetExpFormula('p')).lower())
        # h_Fit = ff_h.Fit(f1,"ESQrobust","",30.0,400.0)
        # if channel == "tt":
        #     h_Fit = ff_h.Fit(f1,"ESQrobust","",40.0,400.0)
        # bad_fit = False
        # try:
        #     fit_status = h_Fit.Status()
        # except: 
        #     fit_status = -1
        #     chi_2 = -1
        #     bad_fit = True
        # print("Fit Status:", fit_status)
        # Print out the fitted parameters
        n_params = fit.GetNpar()  # Get the number of parameters in the function

        print("Fitted parameters:")
        for i in range(n_params):
            param_value = fit.GetParameter(i)
            param_error = fit.GetParError(i)
            print("Parameter {}: Value = {}, Error = {}".format(i, param_value, param_error))
    
        print(int(ff_h.GetBinLowEdge(ff_h.GetNbinsX()+1)) - int(ff_h.GetBinLowEdge(1)) +1 )
        nbins = int(int(ff_h.GetBinLowEdge(ff_h.GetNbinsX()+1)) - int(ff_h.GetBinLowEdge(1)) +1)
        fitter =  R.TVirtualFitter.GetFitter()
        h_uncert = R.TH1D(ff_h.GetName()+'_uncert',"",nbins,int(ff_h.GetBinLowEdge(1)),int(ff_h.GetBinLowEdge(ff_h.GetNbinsX()+1)))
        fitter.GetConfidenceIntervals(h_uncert, 0.68)
    
    else:
        bad_fit=False
        pass
    nbins = int(int(ff_h.GetBinLowEdge(ff_h.GetNbinsX()+1)) - int(ff_h.GetBinLowEdge(1)) +1)
    # Now the "ff_h" histogram has the fitted function values as the
    # bin contents and the confidence intervals as bin errors, we can directly use that 
    ff_h.SetStats(False)
    # ff_h.SetFillColor(870)
    
    ## drawing and saving 
    dummy_hist = R.TH1F("dummy", ";pT;Fake Factor", 1, 30, 400)
    if channel == "tt":
        dummy_hist = R.TH1F("dummy", ";pT;Fake Factor", 1, 35, 400)
    dummy_hist.SetStats(False)  # Turn off stats box
    actual_max = 0
    for bin in range(0, ff_h.GetNbinsX() + 1):
        bin_content = ff_h.GetBinContent(bin)
        if bin_content > actual_max:
            actual_max = bin_content
    if actual_max >0.25:
        ymax  = 0.6
    elif actual_max > 0.1:
        ymax = 0.3
    else:
        ymax = 0.15
    dummy_hist.GetYaxis().SetRangeUser(0,ymax)
    
    c = R.TCanvas("p1", "p1", 1000,600)
    dummy_hist.Draw()
    
    ## now save the fit result to TGraph        
    n_bins = ff_h.GetNbinsX()
    graph = R.TGraph(nbins)

    for bin in range(0, n_bins + 1):
        if ff_h.GetBinContent(bin) < 0:
            ff_h.SetBinContent(bin, 0)
        if ff_original.GetBinContent(bin) < 0:
            ff_original.SetBinContent(bin, 0)
    # ff_h.Draw("e3 same")
    # ff_h.Draw('same')
    ff_original.SetStats(False)
    ff_original.Draw('same')

    graph_up = R.TGraph(nbins )
    graph_down = R.TGraph(nbins)
    
    for bin in range (int(ff_h.GetBinLowEdge(1)), 150):
        if ff_h.GetNbinsX() > 4 or channel == "tt":
            bin_content = fit.Eval(bin) if  fit.Eval(bin)> 0 else 0
            bin_err = h_uncert.GetBinError(bin -int(ff_h.GetBinLowEdge(1)) )
        else:
            i_bin = ff_original.FindBin(bin)
            bin_content =ff_original.GetBinContent(i_bin)
            bin_err =ff_original.GetBinError(i_bin)
        # print(bin, bin_err)
    
        graph.SetPoint(bin, bin, bin_content)

                
        bin_content_down = bin_content - bin_err if bin_content - bin_err >0  else 0
        bin_content_up = bin_content + bin_err if bin_content + bin_err >0   else  0
        # bin_content_down = bin_content - bin_err 
        # bin_content_up = bin_content + bin_err 
        graph_down.SetPoint(bin, bin, bin_content_down )
        graph_up.SetPoint(bin, bin, bin_content_up )
    print("status of bad fit: ", bad_fit)
    if bad_fit:
        ## do the fit for second part:
        f3 = R.TF1('f3', " pol0 " ,150, 400)
        h_Fit_2 = ff_h2.Fit("f3", "NSR")
        fit =f3
        fitter =  R.TVirtualFitter.GetFitter()
        h_uncert = R.TH1D(ff_h.GetName()+'_uncert',"",nbins,int(ff_h.GetBinLowEdge(1)),int(ff_h.GetBinLowEdge(ff_h.GetNbinsX()+1)))
        fitter.GetConfidenceIntervals(h_uncert, 0.68)
    last_bin = False
    # bin_current =  ff_original.FindBin(120)
    for bin in range ( 150,400):
        
        if ff_h.GetNbinsX() > 4 or channel == "tt":
            bin_content = fit.Eval(bin) if  fit.Eval(bin)> 0 else 0
            bin_err = h_uncert.GetBinError(bin -int(ff_h.GetBinLowEdge(1)) )
        else:
            i_bin = ff_original.FindBin(bin)
            bin_content =ff_original.GetBinContent(i_bin)
            bin_err =ff_original.GetBinError(i_bin)
        # print(bin, bin_err)
        i_bin = ff_original.FindBin(bin)
        
        # print(" looking for bins:  found bin at: " , i_bin)
        bin_original = ff_original.GetBinContent(i_bin)
        bin_original_error = ff_original.GetBinError(i_bin)
        fix_last_bin = True
        if bin_original - bin_original_error> bin_content and bin >=200 and ff_original.GetBinLowEdge(i_bin+1) - ff_original.GetBinLowEdge(i_bin) > 50 and fix_last_bin  or i_bin >= ff_h.GetNbinsX():
        # if i_bin >= ff_h.GetNbinsX():
                
            bin_content = bin_original
            bin_err = min( bin_original_error, bin_content)
            
            graph.SetPoint(bin, bin, bin_content)
            
            
            # print("check bin content", bin_original, bin_content)
        else:
            graph.SetPoint(bin, bin, bin_content)
            if i_bin >= ff_h.GetNbinsX():
                fix_last_bin =False
    
                
        bin_content_down = bin_content - bin_err if bin_content - bin_err >0  else 0
        bin_content_up = bin_content + bin_err if bin_content + bin_err >0   else  0
        # bin_content_down = bin_content - bin_err 
        # bin_content_up = bin_content + bin_err 
        graph_down.SetPoint(bin, bin, bin_content_down )
        graph_up.SetPoint(bin, bin, bin_content_up )


    # graph.SetPoint(0, ff_h.GetBinCenter(0), ff_h.GetBinContent(1))
    # if Produce_tot_stat_Syst:
    #     graph_down.SetPoint(0,  ff_h.GetBinCenter(0), ff_h.GetBinContent(1) -  ff_h.GetBinError(1) if  (ff_h.GetBinContent(1) -  ff_h.GetBinError(1) ) > 0 else 0 )
    #     graph_up.SetPoint(0,  ff_h.GetBinCenter(0), ff_h.GetBinContent(1) +  ff_h.GetBinError(1) if  (ff_h.GetBinContent(1) +  ff_h.GetBinError(1) ) < 1 else 2 *(ff_h.GetBinContent(1) +  ff_h.GetBinError(1) ) )

    # graph.GetXaxis().SetRangeUser(ff_h.GetXaxis().GetXmin(),ff_h.GetXaxis().GetXmax() )
    # graph.SetPoint(n_bins+1, 1000, bin_content)
    graph.SetLineColor(910)
    graph.Draw("same")
    graph_down.SetLineColor(860)
    graph_up.SetLineColor(810)
    graph_down.Draw("same")
    graph_up.Draw("same")
    import ctypes

    # graph_up.GetXaxis().SetRangeUser(ff_h.GetXaxis().GetXmin(),ff_h.GetXaxis().GetXmax() )
    # graph_down.GetXaxis().SetRangeUser(ff_h.GetXaxis().GetXmin(),ff_h.GetXaxis().GetXmax() )
    # graph_up.SetPoint(n_bins+1, 1000, bin_content_up)
    # graph_down.SetPoint(n_bins+1, 1000, bin_content_down)

    # Number of bins
    n_points = graph_down.GetN()
    # Create a graph to fill the area between graph_down and graph_up
    graph_filled = R.TGraph(2 * 400)

    # Fill the graph with points from graph_down (in order) and graph_up (in reverse order)
    for i in range(n_points):
        # Use ctypes.c_double to pass references
        x_down, y_down = ctypes.c_double(), ctypes.c_double()
        x_up, y_up = ctypes.c_double(), ctypes.c_double()

        # Get the points for graph_down
        graph_down.GetPoint(i, x_down, y_down)
        graph_filled.SetPoint(i, x_down.value, y_down.value)  # Access the .value attribute to get the actual float value

        # Get the points for graph_up
        graph_up.GetPoint(n_points - 1 - i, x_up, y_up)
        graph_filled.SetPoint(n_points + i, x_up.value, y_up.value) 

    # Set the fill color and style for the filled area
    graph_filled.SetFillColor(870)
    graph_filled.SetFillStyle(3001)  # Optional: Set the fill style (3001 is a solid fill)

    # Draw the filled area graph
    graph_filled.Draw("f")  # 'f' option fills the area


    # Create a TGraph from the histogram
    # Save the graph to a ROOT file
    output_file = R.TFile(f"{input_path}/FakeFactor_fitted.root", "UPDATE") if os.path.exists(f"{input_path}/FakeFactor_fitted.root") else  R.TFile(f"{input_path}/FakeFactor_fitted.root", "RECREATE")
    graph.Write(f"FF{DR}{var}{npreb}{ratio}{syst}")
    if Produce_tot_stat_Syst:
        graph_up.Write(f"FF{DR}{var}{npreb}{ratio}__FF_tot_StatUp")
        graph_down.Write(f"FF{DR}{var}{npreb}{ratio}__FF_tot_StatDown")
    output_file.Close()
    c.Print( input_path +'/FF'+DR+var + npreb + ratio + syst+'.png')
    fnew.Close()
def produce_fake(df_dict, input_path, systematics = [], save_DR = True ,index = 10):
    '''
    input_path, sample_list, final_string:dictionary of key DR names and values FF string
    produce fakes template in Anti ID regions and for each DRs
    in fact the selections for each DR is not applied here. Only the FF for each DR is applied
    '''
    samples = getall_list(input_path)
    if not os.path.exists(f'{input_path}/tmpsamples_withW.root'):
    # if 1>0:
        command = "hadd -f2 " + f'{input_path}/tmpsamples_withW.root' + " " + " ".join(samples)
        # Execute the command using os.system
        result = os.system(command)
        if result != 0:
            print("Error:  hadding failed. try hadd the following by hand: ")
            print(command)
            sys.exit(-1)

    print("using weight:  ",  f'({MC_weight})/{lumi}')
    # R.gDebug=3
    ## the lumi is divided only once here. Otherwise the normalisation is wrong
    df_withW = R.RDataFrame('ntuple', f'{input_path}/tmpsamples_withW.root').Filter(combinecut(Anti_ID,Htautau.lepton_veto, complete_lepton_selection, true_MC_only)).Define('genWeight_tmp',  
        f'({MC_weight})/{lumi}') #.Redefine("genWeight_tmp", f" is_data == 0? genWeight_tmp/{lumi} :genWeight_tmp  ")
    df_data = R.RDataFrame('ntuple', getdata_list(input_path)).Filter(combinecut(Anti_ID,Htautau.lepton_veto, complete_lepton_selection)).Define('genWeight_tmp',  
        f'({MC_weight})/{lumi}') #.Redefine("genWeight_tmp", f" is_data == 0? genWeight_tmp/{lumi} :genWeight_tmp  ")


    columns = list(df_data.GetColumnNames() )
    print("printing data list:   ", getdata_list(input_path))
    # print("printing data columns:      " , columns)
    output_column = columns
    ## many columns are not present in data, using only data columns to save
    systematics.insert(0,"") ##  add the nominal in the syst list, nominal is alaways run
    ## systematics example: _FF_tot_StatUp
    cpp_code_initial =f""" TFile* f_FakeFactor{index} = new TFile("{input_path}/FakeFactor_fitted.root");"""
    R.gInterpreter.Declare(cpp_code_initial)
    
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
                    float interpolate_{npreb}_{ratio}_{DR}{syst}{index}(float x) {{
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
            print(f"combined_weight_str, {combined_weight_str}")
            # if channel=="tt":
            df0= df_withW ## in practice the MC subtaction leave a small gap in the SR. The MC subtraction is very small and shouldn't cause any difference
            # else:
                # df0 = df_withW if DR == "W" else df_withW

            if syst == "":
                if "FF_weight" not in df0.GetColumnNames():
                    df_dict[DR] = df0.Define("FF_weight", f"genWeight_tmp * ({combined_weight_str}) " ).Filter("FF_weight != 0")
                else:
                    df_dict[DR] = df0.Redefine("FF_weight", f"genWeight_tmp * ({combined_weight_str}) " ).Filter("FF_weight != 0")
                
                df_dict[DR] = df_dict[DR].Redefine(
                    'genWeight', "float(1.0)").Redefine('is_fake', 'true' ).Redefine("puweight", "double(1.0)")
                for w in MC_weight_list:
                    df_dict[DR] = df_dict[DR].Redefine(w, "float(1.0)")
                # df_dict[DR] = df_dict[DR].Redefine('id_wgt_tau_vsJet_Medium_2',  'float(1)')
                df_dict[DR] = df_dict[DR].Redefine('id_tau_vsJet_Medium_1' if channel == "tt" else 'id_tau_vsJet_Medium_2',  'int(1)')
                # if channel == "tt":
                #     df_dict[DR] = df_dict[DR].Redefine('id_wgt_tau_vsJet_Medium_1',  'float(1)')
                    #.Filter("genWeight != 0")
            else:
                if f'FF_weight{syst}' not in df_dict[DR].GetColumnNames():
                    df_dict[DR] = df_dict[DR].Define(f'FF_weight{syst}', f"genWeight_tmp * ({combined_weight_str}) " )
                else:
                    df_dict[DR] = df_dict[DR].Redefine(f'FF_weight{syst}', f"genWeight_tmp * ({combined_weight_str}) " )

            
    for syst in systematics: 
        if f"FF_weight{syst}" not in output_column:
            output_column.append(f"FF_weight{syst}")
    for o in output_column:
        if o not in df_dict[DR].GetColumnNames():
            print(o, "not found!!!!!!!!! ")
    for o in columns:
        if o not in df_dict[DR].GetColumnNames():
            print(o, "not found in data!!!!!!!!!")
    # DR_speical_cut = {'QCD': "1>0"} if channel =="tt" else {'W': Htautau.W_true_only, 'QCD' : "1>0", 'ttbar': f"{Htautau.ttbar_true_only} && {Htautau.W_true_only}" }
    # if save_DR:
        # for DR in df_dict:
        # for DR in ["ttbar"]:            
            # print("processing ",DR)
            # print("saving DR with columns:  ", output_column)
            # print('checking output coloumn', output_column)
            # for c in output_column:
                # if str(c) not in df_dict[DR].GetColumnNames():
                    # print(f'================   ERROR: {c} not in output column')
            # df_dict[DR].Filter(DR_speical_cut[DR]).Snapshot("ntuple", f"{input_path}/FF_{DR}.root", output_column)
            ## modify 1
            # df_dict[DR].Filter(DR_speical_cut[DR]).Snapshot("ntuple", f"{input_path}/FF_{DR}.root")
            # df_dict[DR]  =  df_dict[DR].Filter(DR_speical_cut[DR]) 
            
    return  output_column
def combine_Fakes(input_path, df_dict,  apply_fraction = False, systematics = [], tag = ""):
    '''
    fraction: root file storing the fraction in mt_tot
    '''
    # histogram name: wjets_ARtight_mTnobmt_tot
    
    DRs = ["data"] if channel == "tt" else ["data", "wjets", "ttbar"]
    # DRs = ["data"] if channel == "tt" else ["wjets"]
    DR_name = {"data":"QCD",    "wjets":"W",    "ttbar":"ttbar" } ## the naming follow the names in produce_fake
    
    systematics.insert(0,"")  ##  add the nominal in the syst list, nominal is alaways run
    for DR in DRs:
        df = df_dict[ DR_name[DR] ]
        for syst in systematics:
            # for tt channel, nothing to be updated
            if apply_fraction:
                if channel !="tt": 
                    df = df.Redefine(f'FF_weight{syst}', f'GetmTtotweights{DR}(mt_tot,nbtag,mt_1 ) * FF_weight{syst}')
                    # print(f"checking pos 3 {DR} FF_weight", df.Mean("FF_weight").GetValue())
                    # df = df.Redefine(f'genWeight{syst}', f'FF_weight{syst}')
                    # print("I am here 14 ", df.Count().GetValue())
        df = df.Filter("FF_weight !=0")
        df.Snapshot('ntuple', f'{input_path}/Fakes_mttot_tmp{tag}{DR}.root')
        print(f"finishing saving temporary fakes file to :{input_path}/Fakes_mttot_tmp{tag}{DR}.root ")
    
    if channel != "tt": 
        in_file  = f"{input_path}/Fakes_mttot_tmp{tag}data.root {input_path}/Fakes_mttot_tmp{tag}wjets.root {input_path}/Fakes_mttot_tmp{tag}ttbar.root "
    else:
        in_file  = f"{input_path}/Fakes_mttot_tmp{tag}data.root "
    os.system(f'hadd -f2 {input_path}/FF_Combined{tag}.root {in_file}')
def clousre_correction(df_dict, run_double_correction = True, index = 1):
    ## produce closure correction for each channel.
    ## tt: correction bin in eta_1
    ## mt,et: correction bin in C_QCD, C_W
    run = 1
    if run_double_correction:
        tmp_tag = "2"
    else:
        tmp_tag = "1"
    c = R.TCanvas()
    h_n ={}
    h_d ={}
    df_num = {}
    df_den = {}

    ## make a copy of df_den from df_dict
    for i in df_dict:
        df_den[i] =  df_dict[i].Define("dummy", "eta_2")

    corr = {}
    h_setting = {}
    if channel == "et":
        selection = combinecut( Htautau.et_triggers_selections[era],Htautau.electron_selections_FF,Htautau.lepton_veto,Htautau.et_tau_selections[era])
    elif channel == "mt":
        selection = combinecut( Htautau.mt_triggers_selections[era],Htautau.muon_selections,Htautau.lepton_veto,Htautau.mt_tau_selections[era])  
    elif channel == "em":
        selection = combinecut( Htautau.em_triggers_selections[era],Htautau.em_electron_selection,Htautau.em_muon_selection,Htautau.lepton_veto)
    elif channel == "tt":
        selection = combinecut( Htautau.tt_triggers_selections[era],Htautau.tt_secondtau_selections,Htautau.tt_leadingtau_selections,Htautau.lepton_veto)
    for DR in (["QCD"] if channel == "tt" else ["QCD", "W"]):
        ## for ttbar, I haven't figured out a way to correct    
        bins = 20
        # if lumi < 10e3:
        #     bins= 10
        if channel =="tt":
            var =  "mt_1"
            var_2 = "met"
            binning_var_2 = [0,5,10, 15, 20, 25, 30,35,40,45,50,60,70,80,100,120,150,200]
            h_setting[DR] = ( f"Correction;{var};Closure Correction", bins, -2.3, 2.3)
            h_setting[f"{DR}_{var_2}"] = ( f"Correction;{var_2};Closure Correction",len(binning_var_2)-1, array.array('d', binning_var_2))
        else:
            # var = f"C_{DR}"  
            # var= f"C_{DR}"
            # var=f"C_{DR}"
            # var = "met"  
            var="eta_2"
            # var_2 = "eta_2"
            var_2 = "mt_2"
            binning_var_2 = [0,5,10, 15, 20, 25, 30,35,40,45,50,60,70,80,100,120,150,200]
            # binning = [20,30,35,40,45,50,55,60,65,70,75,80,90,100,150] if DR =="W" else [20,30,35,40,45,50,55,60,70,80,120]
            binning = [0,10,20,30,40,50,60,70,80,90,100,120, 150,200]

            # binning = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1,1.2,1.3,1.4,1.5,1.6] if DR =="W" else [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1,1.2,1.3,1.4,1.5,1.6]
            # h_setting[DR] = ( f"Correction;{var};Closure Correction",bins,-2.5,2.) if DR == "QCD" else ( f"Correction;{var};Closure Correction",bins,-5,6)    
            h_setting[DR] = ( f"Correction;{var};Closure Correction",bins,-2.5,2.5)
            
            # h_setting[f"{DR}_{var_2}"] = ( f"Correction;{var_2};Closure Correction", 20, -2.4, 2.4)
            h_setting[f"{DR}_{var_2}"] = ( f"Correction;{var_2};Closure Correction",len(binning_var_2)-1, array.array('d', binning_var_2))
        
        samples = getall_list(input_path)
        
        df_num[DR] = R.RDataFrame('ntuple', samples) 
        ## modify 1
        # df_den[DR] = R.RDataFrame('ntuple', f"{input_path}/FF_{DR}.root") 
        
        if DR == "QCD":     
            df_num["QCD"] = df_num[DR].Filter(combinecut(true_MC_only, DR_QCD, ID, selection)).Define(f'genWeight_tmp{tmp_tag}',f'{MC_weight}')
            df_den["QCD"] = df_den[DR].Filter(combinecut(true_MC_only, DR_QCD, ID, selection)).Define(f'genWeight_tmp{tmp_tag}',f'FF_weight * {lumi} ')
            print(f"Finish getting QCD df, entries of QCD ID: {df_num['QCD'].Count().GetValue() }")
        if DR == "W":
            df_num["W"]= df_num[DR].Filter(combinecut(true_MC_only, DR_W, ID, selection )).Define(f'genWeight_tmp{tmp_tag}',f'{MC_weight}')
            df_den["W"] = df_den[DR].Filter(combinecut(true_MC_only, DR_W, ID, selection )).Define(f'genWeight_tmp{tmp_tag}',f'FF_weight * {lumi} ')
            print(f"Finish getting W df, entries of W ID: {df_num['W'].Count().GetValue() }")
    if run:
        if run_double_correction:
            closure_input  = R.TFile.Open('/'.join([input_path,'double_closure_input.root']), 'RECREATE' ) 
        else:
            closure_input  = R.TFile.Open('/'.join([input_path,'closure_input.root']), 'RECREATE' ) 
        
        for DR in df_num:
            print(df_num)
            print("DR:            ", DR)
            # var=f"C_{DR}"
            # var_2 = "mt_2"
            # write(h, directory, name,fout): "Write `h` to dir `directory` with name `name` in file `fout`"
            print(f"generating histograms of {DR}")
            if run_double_correction:

                h_n[f"{DR}_{var_2}"] = df_num[DR].Histo1D((f"input_num_{DR}_{var_2}",*h_setting[f"{DR}_{var_2}"]),var_2, f'genWeight_tmp{tmp_tag}')
                h_d[f"{DR}_{var_2}"] = df_den[DR].Histo1D((f"input_den_{DR}_{var_2}",*h_setting[f"{DR}_{var_2}"]),var_2, f'genWeight_tmp{tmp_tag}')
                write(h_n[f"{DR}_{var_2}"], "", f'closure_{DR}_{var_2}_num',closure_input)
                write(h_d[f"{DR}_{var_2}"], "", f'closure_{DR}_{var_2}_den',closure_input)
            else:
                h_n[DR] = df_num[DR].Histo1D((f"input_num_{DR}",*h_setting[DR]),var, f'genWeight_tmp{tmp_tag}')
                h_d[DR] = df_den[DR].Histo1D((f"input_den_{DR}",*h_setting[DR]),var, f'genWeight_tmp{tmp_tag}')
                write(h_n[DR], "", f'closure_{DR}_num',closure_input)
                write(h_d[DR], "", f'closure_{DR}_den',closure_input)

    else:
        if run_double_correction:
            closure_input  = R.TFile.Open('/'.join([input_path,'double_closure_input.root']), 'READ' ) 
        else:
            closure_input  = R.TFile.Open('/'.join([input_path,'closure_input.root']), 'READ' ) 
        
        # closure_input  = R.TFile.Open('/'.join([input_path,'closure_input.root']),'READ' ) 
        for DR in df_num:
            
            if run_double_correction:

                h_n[f"{DR}_{var_2}"] =  get(f'closure_{DR}_{var_2}_num', "",closure_input )
                h_d[f"{DR}_{var_2}"] =  get(f'closure_{DR}_{var_2}_den', "",closure_input )
            else:
                h_n[DR] =  get(f'closure_{DR}_num', "",closure_input )
                h_d[DR] =  get(f'closure_{DR}_den', "",closure_input )
    # Finished generate numerator and denominator
    
    # if run:
    closure_output  = R.TFile.Open('/'.join([input_path,'double_corrections.root']),'RECREATE' )  if run_double_correction else  R.TFile(f"{input_path}/closure_corrections.root", "RECREATE")
    for DR in (["QCD"] if channel == "tt" else ["QCD", "W"]):
        if run:
            
            if run_double_correction:

                num_eta_2 = h_n[f"{DR}_{var_2}"].GetValue()
                den_eta_2 = h_d[f"{DR}_{var_2}"].GetValue()
            else:
                num = h_n[DR].GetValue()
                den = h_d[DR].GetValue()
        else:
            if run_double_correction:

                num_eta_2 = h_n[f"{DR}_{var_2}"]
                den_eta_2 = h_d[f"{DR}_{var_2}"]
            else:
                num = h_n[DR]
                den = h_d[DR]
 
        if run_double_correction:

            closure_eta_2 = num_eta_2.Clone()
            closure_eta_2.Scale( den_eta_2.Integral()/closure_eta_2.Integral() )
            closure_eta_2.Divide(den_eta_2)
            closure_eta_2 = remove_neg(closure_eta_2)
            corr[f"{DR}_{var_2}"] = closure_eta_2
            write(closure_eta_2, '' ,f'closure_{DR}_{var_2}', closure_output)  
        else: 
            closure = num.Clone()
            closure.Divide(den)
            corr[DR] = closure
            write(closure, '' ,f'closure_{DR}', closure_output)  


    # fit closure. Save the fitted result to a TGraph in root file
    
    output_file = R.TFile(f"{input_path}/closure_double_corrections_fitted.root", "RECREATE") if run_double_correction else  R.TFile(f"{input_path}/closure_corrections_fitted.root", "RECREATE")
    c = R.TCanvas("p1", "p1", 1000,600)
    c.cd()
    for DR in corr:
        ff_h = corr[DR]
        ff_original = ff_h.Clone()
        
        hint = ff_h.Clone()
        # f1 = R.TF1('closure_{DR}', " ([0] + [1] *x + [2] *x*x + [3] *x*x*x  + [4] *x*x*x*x) + [5] *x*x*x*x*x)", -2.1, 2.1)
        # h_Fit = ff_h.Fit(f1,"ESRQ","",-2.1,2.1)
        if var_2 in DR:
            f2 = R.TF1('f2', " [2] +  TMath::Landau(x, [0], [1], false) + [3]*x " ,0, 200)
            # f_Fit = ff_h.Fit("pol6" ,"ESRQ", "",ff_h.GetXaxis().GetXmin(), ff_h.GetXaxis().GetXmax()) ## pol6 gives best result
            f_Fit = ff_h.Fit(f2 ,"ESRQ", "",ff_h.GetXaxis().GetXmin(), ff_h.GetXaxis().GetXmax()) ## pol6 gives best result
        else:
            f_Fit = ff_h.Fit("pol4" ,"ESRQ", "",ff_h.GetXaxis().GetXmin(), ff_h.GetXaxis().GetXmax()) ## pol6 gives best result

        ## this step calculates the error of one sigma
        R.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint,0.68)

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
        if actual_max > 2:
            for bin in range(0, ff_h.GetNbinsX() + 1):
                print(f"bin {bin}, value {ff_h.GetBinContent(bin)}")
        actual_max = min(actual_max, 2)
        dummy_hist.GetYaxis().SetRangeUser(0., min(1, actual_max *3))
        # dummy_hist.Draw()
        # hint.Draw("e3 same")
        print(f"hint.Integral() {hint.Integral()}")
        # ff_original.SetStats(False)
        print(f"ff_original.Integral() {ff_original.Integral()}")
        ff_original.Draw('same')
        ## now save the fit result to TGraph        
        n_bins = hint.GetNbinsX()
        graph = R.TGraph(n_bins+1)
        


        h_result = hint if var_2 in DR else ff_original
        for bin in range(0, n_bins + 1):
            # For variable bin widths, use GetBinCenter to get the correct bin center
            bin_center = h_result.GetBinCenter(bin)
            bin_content = h_result.GetBinContent(bin)    
            # bin_err = h_result.GetBinError(bin)
            graph.SetPoint(bin, bin_center, bin_content)
        graph.SetPoint(0, h_result.GetBinCenter(0), h_result.GetBinContent(1))
        graph.SetPoint(n_bins+1, h_result.GetBinCenter(n_bins), h_result.GetBinContent(n_bins))
            
        graph.GetXaxis().SetRangeUser(h_result.GetXaxis().GetXmin(),h_result.GetXaxis().GetXmax() )
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
    if run_double_correction:
        cpp_code_initial =f""" TFile* f_closure{index} = new TFile("{input_path}/closure_double_corrections_fitted.root");"""
    else:
        cpp_code_initial =f""" TFile* f_closure{index} = new TFile("{input_path}/closure_corrections_fitted.root");"""
    R.gInterpreter.Declare(cpp_code_initial)
    ## modify 1
    # df_dict = {}
    
    if run_double_correction:
        tag = "double_corrected"
    else:
        tag = "closure_corrected"
    for DR in (['QCD'] if channel =="tt" else ['W', 'QCD']):
            # var=f"C_{DR}"
            ## modify 1
            # df_dict[DR] =R.RDataFrame('ntuple', f"{input_path}/FF_{DR}.root") 
            
            # Construct the graph name
            graph_name = f"closure_{DR}"
            # Generate the C++ code for the interpolation function
            cpp_code = f"""
            
            TGraph* graph_closure_{DR}{index} = (TGraph*)f_closure{index}->Get("{graph_name}");
            float interpolate_closure_{DR}{index}(float x) {{
                return graph_closure_{DR}{index}->Eval(x);
            }}

            """
            # Declare the function
            R.gInterpreter.Declare(cpp_code)
            weight_str = f"interpolate_closure_{DR}{index}({var})"
            # if run_double_correction:

            if  run_double_correction:                  # for mt, et double correction
                ## additional corrections applied for {var_2}
                graph_name = f"closure_{DR}_{var_2}"
                cpp_code = f"""    
                TGraph* graph_closure_{DR}{index}_{var_2} = (TGraph*)f_closure{index}->Get("{graph_name}");
                float interpolate_closure_{DR}{index}_{var_2}(float x) {{
                    return graph_closure_{DR}{index}_{var_2}->Eval(x);
                }}

                """
                R.gInterpreter.Declare(cpp_code)
                weight_str = f"(interpolate_closure_{DR}{index}_{var_2}({var_2}))" ## apply the double correction
            
            if "FF_weight" not in df_dict[DR].GetColumnNames():
                print("ERROR:   FF_weight not found")
                sys.exit(-1)
            else:
                OS_SS_Scale = 1
                ## here for redefining the new weight
                if run_double_correction:
                    if DR=="QCD" and channel == "tt":
                    # if channel == "tt" or run_double_correction:


                        file_OSSS = R.TFile.Open(f"sample_database/fractions/Fraction_{era}_{channel}_OS_SS.root", 'r')
                        h_OSSS = get('qcd_OS_SS_nob',"", file_OSSS )
                        f_OSSS = R.TF1('f1_nob', "  [2] + TMath::Landau(x, [0], [1], false) + [3] *x " ,0.5, 5)
                        f_OSSS.SetParameters(1.0, 0., 1.0, -0.1)
                        f_OSSS.SetParLimits(0, 0, 10)
                        f_OSSS.SetParLimits(1, 0, 10)
                        h_fitOSSS = h_OSSS.Fit("f1_nob", "ESQR")
                        
                        param_value0= f_OSSS.GetParameter(0)
                        param_value1= f_OSSS.GetParameter(1)
                        param_value2= f_OSSS.GetParameter(2)
                        param_value3= f_OSSS.GetParameter(3)
                        c_osss = R.TCanvas()
                        h_OSSS.Draw("")
                        c_osss.Print(f"Fraction_nob_{era}_{channel}_OS_SS.png")
                        btag_h_OSSS = get('qcd_OS_SS_btag',"", file_OSSS )
                        btag_f_OSSS = R.TF1('f2_btag', " pol4" ,0.5, 5)
                        btag_h_fitOSSS = btag_h_OSSS.Fit("f2_btag", "ESQR")
                        btag_param_value0= btag_f_OSSS.GetParameter(0)
                        btag_param_value1= btag_f_OSSS.GetParameter(1)
                        btag_param_value2= btag_f_OSSS.GetParameter(2)
                        btag_param_value3= btag_f_OSSS.GetParameter(3)
                        btag_param_value4= btag_f_OSSS.GetParameter(4)
                        c_btagosss = R.TCanvas()
                        btag_h_OSSS.Draw("")
                        c_btagosss.Print(f"Fraction_btag_{era}_{channel}_OS_SS.png")
                        # OS_SS_Scale = " (1.1 + pow(1.15, ((deltaR_ditaupair + 0.3) * (-15))))"    
                        # OS_SS_Scale =  " 0.9 * (1. + pow(1.15, ((deltaR_ditaupair + 0.3) * (-2.5))))"   
                        # OS_SS_Scale =  f" 1.05* ({param_value2} + TMath::Landau(deltaR_ditaupair, {param_value0}, {param_value1}, false) + {param_value3} *deltaR_ditaupair )"
                        # OS_SS_Scale = "2 "
                        OS_SS_Scale =  f"(nbtag == 0?   ({param_value2} + TMath::Landau(deltaR_ditaupair, {param_value0}, {param_value1}, false) + {param_value3} *deltaR_ditaupair ) : ({btag_param_value0} +  {btag_param_value1} * deltaR_ditaupair + {btag_param_value2} * deltaR_ditaupair*deltaR_ditaupair + {btag_param_value3} *deltaR_ditaupair*deltaR_ditaupair*deltaR_ditaupair    + {btag_param_value4} *deltaR_ditaupair*deltaR_ditaupair*deltaR_ditaupair*deltaR_ditaupair    ))"   
                        print("printing OS_SS_Scale  =====================================================")
                        print(OS_SS_Scale)
                    if DR == "QCD" and channel != "tt":
                        OS_SS_Scale = 1.2
                    
                # OS_SS_Scale = " (1.1 + pow(1.15, ((deltaR_ditaupair + 0.3) * (-15))))" if ((channel == "tt") or run_double_correction ) and DR=="QCD"   else 1 ### only apply for QCD fakes and the final correction
                # OS_SS_Scale = " (1.1 + pow(1.15, ((deltaR_ditaupair + 0.3) * (-15))))" if ( run_double_correction ) and DR=="QCD"   else 1 ### only apply for QCD fakes and the final correction
                # OS_SS_Scale = 1

                # if channel == "tt":
                #     OS_SS_Scale =  " (1.1 + pow(1.15, ((deltaR_ditaupair + 0.2) * (-5))))" 
                    # OS_SS_Scale = 1
                

                # "( 1.4 - deltaR_ditaupair * 0.12 + 0.012 * deltaR_ditaupair * deltaR_ditaupair )"
                
                if run_double_correction and DR=="W" :
                    # DR_W_factor = "( pt_1  > 60? 1 : 1.2)"  ## 1.2 factor taken From 50-70 region 
                    DR_W_factor = "1"  ## 1.2 factor taken From 50-70 region 
                # if run_double_correction:
                #     OS_SS_Scale = f"({OS_SS_Scale} * 1.2)"  ## FF calculated without trigger selections allow more stats, but result in a FF 20% smaller than using trigger sel
                # OS_SS_Scale =  1.1
                # print(f"checking pos 1 {DR} FF_weight", df_dict[DR].Mean("FF_weight").GetValue())
                print(f"applying OS_SS scale {OS_SS_Scale}")
                
                # if channel== "tt" or ( DR == "QCD" and run_double_correction) :
                if DR == "QCD" and run_double_correction:
                    df_dict[DR] = df_dict[DR].Redefine("FF_weight", f"( {cut_dic[f'DR_{DR}']}) ? FF_weight * 1 : FF_weight * {OS_SS_Scale}")  ## OS_SS only apply to SR, DR unaffected
                if DR== "W" and run_double_correction:
                    df_dict[DR] = df_dict[DR].Redefine("FF_weight", f" mt_1 > 70 ? FF_weight * 1 : FF_weight * {DR_W_factor}")  ## OS_SS only apply to SR, DR unaffected
                df_dict[DR] = df_dict[DR].Define(f"FF_weight_tmp{tmp_tag}", "FF_weight")
                ## modify 1                
                # df_dict[DR] = df_dict[DR].Define("FF_weight__FF_closureDown", f"FF_weight").Define(
                #     "FF_weight__FF_closureUp",   f"FF_weight * ({weight_str}) * ({weight_str})"  ) ## multiply two times for up, no for down

                if run_double_correction:
                    df_dict[DR] = df_dict[DR].Redefine("FF_weight__FF_closureDown", f"FF_weight").Redefine(
                        "FF_weight__FF_closureUp",   f"FF_weight * ({weight_str}) * ({weight_str})"  ) ## multiply two times for up, no for down
                else:
                    df_dict[DR] = df_dict[DR].Define("FF_weight__FF_closureDown", f"FF_weight").Define(
                        "FF_weight__FF_closureUp",   f"FF_weight * ({weight_str}) * ({weight_str})"  ) ## multiply two times for up, no for down
                print(weight_str)
                
                df_dict[DR] = df_dict[DR].Redefine("FF_weight", f"FF_weight_tmp{tmp_tag} * ({weight_str})" )

                for s in ["__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown"]:
                    df_dict[DR] = df_dict[DR].Redefine(f"FF_weight{s}", f"FF_weight{s} * ({weight_str}) * {OS_SS_Scale}" )
            # print(f"checking pos 2 {DR} FF_weight", df_dict[DR].Mean("FF_weight").GetValue())

    ## modify 1
    # df_dict={}
    # if channel != "tt" :
        ## modify 1
        # df_dict["ttbar"]= R.RDataFrame('ntuple', f"{input_path}/FF_ttbar.root")
        #     .Define(
        #     "FF_weight__FF_closureDown", f"FF_weight").Define(
        #     "FF_weight__FF_closureUp", f"FF_weight").Define(
        #     f"FF_weight_tmp{tmp_tag}", f"FF_weight")
    if run_double_correction and channel!= "tt":
        df_dict["ttbar"]= df_dict["ttbar"].Define(
                "FF_weight__FF_closureDown", f"FF_weight").Define(
                "FF_weight__FF_closureUp", f"FF_weight").Define(
                f"FF_weight_tmp{tmp_tag}", f"FF_weight")
    
    ## modify 1
    # for DR in (["QCD"] if channel == "tt" else ["QCD", "W"]):
    #     df_dict[DR] = R.RDataFrame("ntuple", f"{input_path}/FF_{DR}_{tag}.root")
    # columns = list(df_dict["QCD"].GetColumnNames())
    if run_double_correction : 
    # if run_double_correction or channel== "tt":     
        for DR in df_dict:
            df_dict[DR].Snapshot("ntuple", f"{input_path}/FF_{DR}.root")
    # if ((channel == "tt") or run_double_correction ):
    if ( run_double_correction ):    
        combine_Fakes(input_path,df_dict, True, 
        ["__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown", "__FF_closureDown", "__FF_closureUp" ],
        # [], 
        tag = tag)


if __name__ == '__main__':        
    df_dict = {}
    i = 10
    ###
    run = 0
    ###
    
    if run:
        df_d = get_df(input_path) # acquire dataframe 
    else:
        df_d = 1
        
    FF_input  = R.TFile.Open('/'.join([input_path,'FF_input.root']), 'RECREATE' if run else 'READ' ) 
    h_n = get_FF_f(df_d, FF_input,run, syst=True) # acquire histogram, save them in FakeFactor.root. if run, this functions will get the histograms from the dataframe; else get it from existing FF_input.root
    FF_output = R.TFile.Open('/'.join([input_path,'FakeFactor.root']), 'RECREATE' ) 
    write_FF_f(h_n, FF_output, syst=True) # save the calculated FF from the last step in FakeFactor.root 
    FF_input.Close()
    FF_output.Close()
    R.DisableImplicitMT() ## R.EnableImplicitMT() # I dont know why but it causes the TVirtualFitter.GetFitter() fail
    output_file = R.TFile(f"{input_path}/FakeFactor_fitted.root", "RECREATE")
    output_file.Close()
    for DR in cut_dic:
        for npreb in nprebjets_dic:
                for ratio in ratio_dic:
                    Fit_FF(DR,npreb, ratio,  var,Produce_tot_stat_Syst = True, syst="") ## Produce FF_tot_stat systematics
                    for sys in ["__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsDown","__FF_wjetsUp"  ]:
                        Fit_FF(DR,npreb, ratio,  var,Produce_tot_stat_Syst = False, syst= sys) ## Produce FF_ttbar, FF_Wjets systematics
    ###
    run = 1
    # ## 
    columns = produce_fake(df_dict, input_path, [
            "__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown"
            ], save_DR = True, index =i)
    
    DR_name = [ "QCD", "W", "ttbar"]  if channel != "tt" else ["QCD"]
    if channel != "tt":
        R.gROOT.ProcessLine(f'.L sample_database/cpp_code/loadFF.C')
        R.loadFF(era,channel)
    DRs = ["data"] if channel == "tt" else ["data", "wjets", "ttbar"]
    for DR in DRs:
        if channel != "tt":
                GetmTtotweights_code =f'''
                auto GetmTtotweights{DR} =[] (float mt_tot, int nbtag, float mt_1 ) {{
                    float W = 0;
                    // nob = "( nbtag == 0 ) "
                    // btag = "( nbtag >= 1 ) "
                    // tight_mT = " ( mt_1 < 50.0) "
                    // loose_mT = " ( mt_1 > 50.0 && mt_1 < 70.0 ) "

                    if (nbtag  == 0 ){{
                        if (  mt_1 > 50.0 && mt_1 < 70.0) {{
                            W = Weights["{DR}_ARloose_mTnobmt_tot"]->GetBinContent( Weights["{DR}_ARloose_mTnobmt_tot"]->FindBin(mt_tot) ) ;
                        }}    
                        else if (mt_1 < 50.0 ) {{
                            W = Weights["{DR}_ARtight_mTnobmt_tot"]->GetBinContent( Weights["{DR}_ARtight_mTnobmt_tot"]->FindBin(mt_tot) ) ;
                        }}    
                        else {{
                            W = 0 ;}}
                    }}
                    else {{
                        if ( mt_1 > 50.0 && mt_1 < 70.0) {{
                            W = Weights["{DR}_ARloose_mTbtagmt_tot"]->GetBinContent( Weights["{DR}_ARloose_mTbtagmt_tot"]->FindBin(mt_tot) ) ;
                        }}    
                        else if (mt_1 < 50.0 ) {{
                            W = Weights["{DR}_ARtight_mTbtagmt_tot"]->GetBinContent( Weights["{DR}_ARtight_mTbtagmt_tot"]->FindBin(mt_tot) ) ;
                        }}    
                        else {{
                            W = 0 ;}}
                    }}
                    return W ;
                }};
                '''
                # print(GetmTtotweights_code)
                # R.gROOT.LoadMacro('cpp_code/loadFF.C') # load FF histograms /or any other histograms into a dictionary called Weights with key [histname] 
                R.gInterpreter.Declare(GetmTtotweights_code) 

    # for DR in DR_name:
    #     df_dict[DR] = R.RDataFrame("ntuple", f"{input_path}/FF_{DR}.root")
    # combine_Fakes(input_path,df_dict, True,["__FF_tot_StatDown", "__FF_tot_StatUp", "__FF_ttbarUp","__FF_ttbarDown", "__FF_wjetsUp","__FF_wjetsDown"] )

    clousre_correction(df_dict, run_double_correction=False , index=1)
    # if channel != "tt":
    clousre_correction(df_dict, run_double_correction=True, index=2 )    


    tag = "double_corrected" # if channel != "tt" else "closure_corrected"
    os.system(f'mv {input_path}/FF_Combined{tag}.root {input_path}/FF_Combined.root')  
    os.system(f'mv {input_path}/FF_QCD_{tag}.root {input_path}/FF_QCD.root')  
    os.system(f'mv {input_path}/FF_ttbar_{tag}.root {input_path}/FF_ttbar.root')  
    os.system(f'mv {input_path}/FF_W_{tag}.root {input_path}/FF_W.root')  
    os.system(f'mv {input_path}_{tag}/bkp/FF_ttbar.root {input_path}_{tag}/')  
    