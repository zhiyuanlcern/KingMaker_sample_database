
import os
import sys
import ROOT
import array
import numpy as np



lumi = {
    "2022EE":8.077009684e3,
    "2022postEE":  26.671609707e3,
    "2023": 0.641474303e3 + 18.062659111e3, # B + C
    "2023BPix": 9.693130053e3, # D 
}

bin_edges = np.linspace(0.5, 5, 25).tolist()
# bin_edges = [50,0,5]

cuts = {
    "et": "(trg_single_ele30 ==1||trg_single_tau180_2==1)  &&extramuon_veto == 0 && extraelec_veto == 0 && id_tau_vsMu_VLoose_2 > 0 &&   id_tau_vsEle_Tight_2 > 0  && pt_1> 30.0 && pt_2 > 30   ",
    "mt": "(trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_tau180_2==1) && pt_1> 25.0 && extramuon_veto == 0  && extraelec_veto == 0 && (id_tau_vsMu_VLoose_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) ",
    "tt": "(trg_double_tau30_plusPFjet60  ==1 || trg_double_tau30_plusPFjet75  ==1 || trg_double_tau35_mediumiso_hps  ==1 ) && extramuon_veto == 0  && extraelec_veto == 0 && pt_1 > 40 &&  pt_2 > 40  && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0   && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0   && dz_1 < 0.2 && eta_1 < 2.1 && eta_1 > -2.1 && dz_2 < 0.2 && eta_2 < 2.1 && eta_2 > -2.1 && deltaR_ditaupair > 0.5 "
} #cut 无误







# OS_molecule = {
#     "et": "(q_1 * q_2) < 0 && id_tau_vsJet_VVLoose_2 < 1",  #fail VVloose
#     "mt": "(q_1 * q_2) < 0 && id_tau_vsJet_VVLoose_2 < 1",
#     "tt": "(q_1 * q_2) < 0  && id_tau_vsJet_VVLoose_1 < 1 && id_tau_vsJet_VVLoose_2 < 1 "#  && id_tau_vsJet_Medium_2 >= 1 "#  "   # tau_2 pass Medium
# } #q < 0 无误

# OS_denominator = {
#     "et": "(q_1 * q_2) < 0 && id_tau_vsJet_VVLoose_2 >= 1 && id_tau_vsJet_Medium_2 < 1 ",  #pass VVloose. fail medium
#     "mt": "(q_1 * q_2) < 0 && id_tau_vsJet_VVLoose_2 >= 1 && id_tau_vsJet_Medium_2 < 1",
#     "tt": "(q_1 * q_2) < 0  && id_tau_vsJet_VVLoose_1 >= 1 && id_tau_vsJet_VVLoose_2 >= 1 && id_tau_vsJet_Medium_1 < 1 && id_tau_vsJet_Medium_2 >= 1 " # tau_2 pass Medium
# } #q < 0 无误

# SS_molecule = {
#     "et": "(q_1 * q_2) > 0 && id_tau_vsJet_VVLoose_2 < 1",  #fail VVloose
#     "mt": "(q_1 * q_2) > 0 && id_tau_vsJet_VVLoose_2 < 1",
#     "tt": "(q_1 * q_2) > 0  && id_tau_vsJet_VVLoose_1 < 1 && id_tau_vsJet_VVLoose_2 < 1 " #&& id_tau_vsJet_Medium_2 >= 1 " #&& id_tau_vsJet_Medium_2 >= 1"  # tau_2 pass Medium
# } #q < 0 无误

# SS_denominator = {
#     "et": "(q_1 * q_2) > 0 && id_tau_vsJet_VVLoose_2 >= 1 && id_tau_vsJet_Medium_2 < 1 ",  #pass VVloose. fail medium
#     "mt": "(q_1 * q_2) > 0 && id_tau_vsJet_VVLoose_2 >= 1 && id_tau_vsJet_Medium_2 < 1",
#     "tt": "(q_1 * q_2) > 0  && id_tau_vsJet_VVLoose_1 >= 1 && id_tau_vsJet_VVLoose_2 >= 1 && id_tau_vsJet_Medium_1 < 1 && id_tau_vsJet_Medium_2 >= 1  "  # tau_2 pass Medium
# } #q < 0 无误




OS_molecule = {
    "et": "(q_1 * q_2) < 0 && id_tau_vsJet_Medium_2 < 1",  #fail VVloose
    "mt": "(q_1 * q_2) < 0 && id_tau_vsJet_Medium_2 < 1",
    "tt": "(q_1 * q_2) < 0  && id_tau_vsJet_Medium_1 < 1  "#  && id_tau_vsJet_Medium_2 >= 1 "#  "   # tau_2 pass Medium
} #q < 0 无误

OS_denominator = {
    "et": "(q_1 * q_2) < 0 && id_tau_vsJet_Medium_2 >= 1  ",  #pass VVloose. fail medium
    "mt": "(q_1 * q_2) < 0 && id_tau_vsJet_Medium_2 >= 1 ",
    "tt": "(q_1 * q_2) < 0  && id_tau_vsJet_Medium_1 >= 1  " # tau_2 pass Medium
} #q < 0 无误

SS_molecule = {
    "et": "(q_1 * q_2) > 0 && id_tau_vsJet_Medium_2 < 1",  #fail VVloose
    "mt": "(q_1 * q_2) > 0 && id_tau_vsJet_Medium_2 < 1",
    "tt": "(q_1 * q_2) > 0  && id_tau_vsJet_Medium_1 < 1  " #&& id_tau_vsJet_Medium_2 >= 1 " #&& id_tau_vsJet_Medium_2 >= 1"  # tau_2 pass Medium
} #q < 0 无误

SS_denominator = {
    "et": "(q_1 * q_2) > 0 && id_tau_vsJet_Medium_2 >= 1  ",  #pass VVloose. fail medium
    "mt": "(q_1 * q_2) > 0 && id_tau_vsJet_Medium_2 >= 1 ",
    "tt": "(q_1 * q_2) > 0  && id_tau_vsJet_Medium_1 >= 1   "  # tau_2 pass Medium
} #q < 0 无误




######无误
gen_cut = "(gen_match_2 == 6)"

nob = "(nbtag == 0)"

btag = "(nbtag >= 1)"
######

####无误
weight_dict ={"mt" : {}, "et": {}, "tt": {}, "em": {}, "mm":{}}
weight_dict["mt"]["2022postEE"] = 'Xsec   * {0} * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1' # id_wgt_tau_vsJet_Medium_2 *
weight_dict["mt"]["2022EE"] =weight_dict["mt"]["2023"] =weight_dict["mt"]["2023BPix"]= weight_dict["mt"]["2022postEE"]
weight_dict["et"]["2022postEE"] =  'Xsec * {0}* puweight * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2  *  btag_weight * FF_weight * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30  '  #  id_wgt_tau_vsJet_Medium_2  *
weight_dict["et"]["2022EE"] =weight_dict["et"]["2023"] =weight_dict["et"]["2023BPix"]= weight_dict["et"]["2022postEE"]
weight_dict["tt"]["2022postEE"]  =   'Xsec *  {0}* puweight * genWeight/genEventSumW *    btag_weight    *  FF_weight * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 ' # 
weight_dict["tt"]["2022EE"] =weight_dict["tt"]["2023"] =weight_dict["tt"]["2023BPix"]= weight_dict["tt"]["2022postEE"]
weight_dict["em"] = {"2022postEE": '(Xsec * genWeight *  {0} / genEventSumW)* (trg_wgt_single_ele30 * trg_single_ele30 > 0 + 1 * trg_single_ele30 < 1 ) * id_wgt_ele_wpTight * id_wgt_mu_2 * btag_weight * puweight * (trg_wgt_single_mu24 * trg_single_mu24 > 0 + 1 * trg_single_mu24 < 1 )'   .format(lumi)}
weight_dict["em"]["2022EE"] =weight_dict["em"]["2023"] =weight_dict["em"]["2023BPix"]= weight_dict["em"]["2022postEE"]

####3



def load_files(folder, channel):
    #无误
    if channel == "et":
        return ROOT.RDataFrame("ntuple", f"{folder}/EGamma*.root")
    elif channel == "mt":
        return ROOT.RDataFrame("ntuple", f"{folder}/*Muon*.root")
    elif channel == "tt":
        return ROOT.RDataFrame("ntuple", f"{folder}/Tau*.root")
    else:
        raise ValueError("Invalid channel specified")

def set_negative_bins_to_zero(histogram):
    for i in range(histogram.GetNbinsX()):
        if histogram.GetBinContent(i+1) < 0:
            histogram.SetBinContent(i+1, 0)

def main(folder, channel, era):
    ROOT.ROOT.EnableImplicitMT()
    output_file = ROOT.TFile(f"Fraction_{era}_{channel}_OS_SS.root", "RECREATE")

    # Ensure default sum of squares is enabled
    ROOT.TH1.SetDefaultSumw2(True)

    # 读取数据
    df_data = load_files(folder, channel)
    df_ttbar = ROOT.RDataFrame("ntuple", f"{folder}/TTto*.root")
    df_wjets = ROOT.RDataFrame("ntuple", f"{folder}/WtoLNu-4Jets_*.root")
    df_dyjets = ROOT.RDataFrame("ntuple", f"{folder}/DYto2*.root")

    # 设置 cut 和 weight
    base_cut = cuts[channel]


    OS_cut_molecule = OS_molecule[channel]
    SS_cut_molecule = SS_molecule[channel]

    OS_cut_denominator = OS_denominator[channel]
    SS_cut_denominator = SS_denominator[channel]
    
    #####


    weight_expr = weight_dict[channel][era].format(lumi[era])

    # 定义新的数据帧，将权重计算为新列
    df_data = df_data.Define("weight", weight_expr)
    df_ttbar = df_ttbar.Define("weight", weight_expr)
    df_wjets = df_wjets.Define("weight", weight_expr)
    df_dyjets = df_dyjets.Define("weight", weight_expr)

    # 定义要绘制的图形组合
    regions = {
       "nob": {
           "OS_M": f"{base_cut} && {nob} && {OS_cut_molecule}",
           "SS_M": f"{base_cut} && {nob} && {SS_cut_molecule}",

           "OS_D": f"{base_cut} && {nob} && {OS_cut_denominator}",
           "SS_D": f"{base_cut} && {nob} && {SS_cut_denominator}"
      },
       "btag": {
          "OS_M": f"{base_cut} && {btag} && {OS_cut_molecule}",
          "SS_M": f"{base_cut} && {btag} && {SS_cut_molecule}",

          "OS_D": f"{base_cut} && {btag} && {OS_cut_denominator}",
          "SS_D": f"{base_cut} && {btag} && {SS_cut_denominator}"
      }
    }

    # 合并后的循环
    for name, region_cuts in regions.items():
        os_cut_M = region_cuts["OS_M"]
        ss_cut_M = region_cuts["SS_M"]
        os_cut_D = region_cuts["OS_D"]
        ss_cut_D = region_cuts["SS_D"]

        try:
            if "btag" in name:
                bin_edges = np.linspace(0.5, 5, 12).tolist()
            else:
                bin_edges = np.linspace(0.5, 5, 25).tolist()
                
            # Data 无误
            hist_data_os_M = df_data.Filter(os_cut_M).Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair")
            hist_data_ss_M = df_data.Filter(ss_cut_M).Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair")



            hist_data_os_D = df_data.Filter(os_cut_D).Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair")
            hist_data_ss_D = df_data.Filter(ss_cut_D).Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair")
  



            # QCD直方图 无误
            hist_qcd_os_M = hist_data_os_M.Clone(f"qcd_OS_{name}_M")
            hist_qcd_ss_M = hist_data_ss_M.Clone(f"qcd_SS_{name}_M")

            hist_qcd_os_D = hist_data_os_D.Clone(f"qcd_OS_{name}_D")
            hist_qcd_ss_D = hist_data_ss_D.Clone(f"qcd_SS_{name}_D")



            # 减去 ttbar, wjets 和 dyjets 对于 QCD 的贡献 无误
            hist_ttbar_forqcd_os_M = df_ttbar.Filter(f"{os_cut_M} && gen_match_1 != 6 && gen_match_2 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_wjets_forqcd_os_M = df_wjets.Filter(f"{os_cut_M} && gen_match_1 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_dyjets_forqcd_os_M = df_dyjets.Filter(f"{os_cut_M}").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()

            hist_ttbar_forqcd_os_D = df_ttbar.Filter(f"{os_cut_D} && gen_match_1 != 6 && gen_match_2 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_wjets_forqcd_os_D = df_wjets.Filter(f"{os_cut_D} && gen_match_1 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_dyjets_forqcd_os_D = df_dyjets.Filter(f"{os_cut_D}").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()




            hist_ttbar_forqcd_ss_M = df_ttbar.Filter(f"{ss_cut_M} && gen_match_1 != 6 && gen_match_2 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_wjets_forqcd_ss_M = df_wjets.Filter(f"{ss_cut_M} && gen_match_1 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_dyjets_forqcd_ss_M = df_dyjets.Filter(f"{ss_cut_M}").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()

            hist_ttbar_forqcd_ss_D = df_ttbar.Filter(f"{ss_cut_D} && gen_match_1 != 6 && gen_match_2 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_wjets_forqcd_ss_D = df_wjets.Filter(f"{ss_cut_D} && gen_match_1 != 6").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()
            hist_dyjets_forqcd_ss_D = df_dyjets.Filter(f"{ss_cut_D}").Histo1D(("deltaR_ditaupair", "deltaR_ditaupair", len(bin_edges) - 1, array.array('d', bin_edges)), "deltaR_ditaupair", "weight").GetValue()



            ######## OS 无误
            # hist_qcd_os_M.Add(hist_ttbar_forqcd_os_M, -1)
            # hist_qcd_os_M.Add(hist_wjets_forqcd_os_M, -1)
            hist_qcd_os_M.Add(hist_dyjets_forqcd_os_M, -1)

            # hist_qcd_os_M.Write()

            # hist_qcd_os_D.Add(hist_ttbar_forqcd_os_D, -1)
            # hist_qcd_os_D.Add(hist_wjets_forqcd_os_D, -1)
            hist_qcd_os_D.Add(hist_dyjets_forqcd_os_D, -1)    

            # hist_qcd_os_D.Write()       



            ######## SS 无误
            # hist_qcd_ss_M.Add(hist_ttbar_forqcd_ss_M, -1)
            # hist_qcd_ss_M.Add(hist_wjets_forqcd_ss_M, -1)
            hist_qcd_ss_M.Add(hist_dyjets_forqcd_ss_M, -1)

            # hist_qcd_ss_M.Write()


            # hist_qcd_ss_D.Add(hist_ttbar_forqcd_ss_D, -1)
            # hist_qcd_ss_D.Add(hist_wjets_forqcd_ss_D, -1)
            hist_qcd_ss_D.Add(hist_dyjets_forqcd_ss_D, -1)

            # hist_qcd_ss_D.Write()


          # 将所有负值的 bin 设置为 0
            # set_negative_bins_to_zero(hist_qcd_os_M)
            # set_negative_bins_to_zero(hist_qcd_os_D)           
            # set_negative_bins_to_zero(hist_qcd_ss_M)
            # set_negative_bins_to_zero(hist_qcd_ss_D)



                
          # 1. 计算OS区域
            hist_qcd_OS_real = hist_qcd_os_M.Clone(f"qcd_OS_{name}_M")
            hist_qcd_OS_real.Divide(hist_qcd_os_D)
            # hist_qcd_OS_real.Write()

         # 2.  计算SS区域

            hist_qcd_SS_real = hist_qcd_ss_M.Clone(f"qcd_SS_{name}_M")
            hist_qcd_SS_real.Divide(hist_qcd_ss_D)
            # hist_qcd_SS_real.Write()


         # 3. 计算结果
            hist_qcd_OS_SS_real = hist_qcd_SS_real.Clone(f"qcd_OS_{name}_real")
            hist_qcd_OS_SS_real.Divide(hist_qcd_OS_real)



            hist_qcd_OS_SS_real.SetName(f"qcd_OS_SS_{name}")
            if "btag" in name:
                f1 = ROOT.TF1('f1', "pol4" ,0.5, 5)  # 
            else:
                f1 = ROOT.TF1('f1', "[2] + TMath::Landau(x, [0], [1], false) + [3] *x" ,0.5, 5)  # 
            h_fit = hist_qcd_OS_SS_real.Fit("f1", "ESQR")
            n_params= f1.GetNpar()
            
            for i in range(n_params):
                    param_value = f1.GetParameter(i)
                    param_error = f1.GetParError(i)
                    print("first fit: Parameter {}: Value = {}, Error = {}".format(i, param_value, param_error))
            
            c = ROOT.TCanvas()
            hist_qcd_OS_SS_real.Draw()
            # h_fit.Draw("")
            c.Print(f"qcd_OS_SS_{name}_{channel}_{era}.png")



  
            def customize_histogram(hist):
              hist.GetXaxis().SetTitle('deltaR_ditaupair')
              hist.SetStats(False)

            customize_histogram(hist_qcd_OS_SS_real)
            hist_qcd_OS_SS_real.Write()
            

        except RuntimeError as e:
            print(f"Error processing {name}: {e}")

    output_file.Close()

if __name__ == "__main__":
    folder = sys.argv[1]
    channel = sys.argv[2]
    era = sys.argv[3]
    main(folder, channel, era)





