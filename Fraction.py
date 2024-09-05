import os
import sys
import ROOT
import array
import numpy as np



# Define the variable for mt_tot
variable = "mt_tot"

lumi = {
    "2022EE": 7.875e3,
    "2022postEE": 26.337e3
}

#bin_edges = np.linspace(0, 5, 31).tolist()


cuts = {
    "et": "(trg_single_ele30 ==1|| trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)  &&extramuon_veto == 0 && extraelec_veto == 0 && id_tau_vsMu_VLoose_2 > 0 &&   id_tau_vsEle_Tight_2 > 0  && pt_1> 30.0 && pt_2 > 30   && (q_1 * q_2) < 0 && id_tau_vsJet_Medium_2 < 1 ",
    "mt": "(trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)&& pt_1> 25.0 &&extramuon_veto == 0  && extraelec_veto == 0 &&(id_tau_vsMu_Tight_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) && (q_1 * q_2) < 0 && id_tau_vsJet_Medium_2 < 1 ",
    "tt": "(trg_double_tau30_plusPFjet60  ==1 || trg_double_tau30_plusPFjet75  ==1 || trg_double_tau35_mediumiso_hps  ==1 ||  trg_single_deeptau180_1  ==1 || trg_single_deeptau180_2  ==1) && extramuon_veto == 0  && extraelec_veto == 0 && pt_1 > 40 &&  pt_2 > 40  && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0   && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0   && dz_1 < 0.2 && eta_1 < 2.1 && eta_1 > -2.1 && dz_2 < 0.2 && eta_2 < 2.1 && eta_2 > -2.1 && deltaR_ditaupair > 0.5  &&   (q_1 * q_2) < 0  && id_tau_vsJet_Medium_1 < 1 && id_tau_vsJet_Medium_2 >= 1"
}

gen_cut = "(gen_match_2 == 6)"
nob = "(nbtag == 0)"
btag = "(nbtag >= 1)"
tight_mT = "(mt_1 < 40.0)"
loose_mT = "(mt_1 > 40.0 && mt_1 < 70.0)"




weight_expressions = {
    "et": {
        "2022postEE": 'Xsec * {0} * puweight * genWeight / genEventSumW * id_wgt_tau_vsEle_Tight_2 * btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2 * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2 * trg_wgt_single_ele30',
        "2022EE": 'Xsec * {0} * puweight * genWeight / genEventSumW * id_wgt_tau_vsEle_Tight_2 * btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2 * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2 * trg_wgt_single_ele30'
    },
    "mt": {
        "2022postEE": 'Xsec * {0} * puweight * genWeight / genEventSumW * btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1 * trg_wgt_ditau_crosstau_2 * id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1',
        "2022EE": 'Xsec * {0} * puweight * genWeight / genEventSumW * btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1 * trg_wgt_ditau_crosstau_2 * id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1'
    },
    "tt": {
        "2022postEE": 'Xsec * {0} * puweight * genWeight / genEventSumW * btag_weight * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 * FF_weight * trg_wgt_ditau_crosstau_1 * trg_wgt_ditau_crosstau_2',
        "2022EE": 'Xsec * {0} * puweight * genWeight / genEventSumW * btag_weight * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 * FF_weight * trg_wgt_ditau_crosstau_1 * trg_wgt_ditau_crosstau_2'
    }
}

def load_files(folder, channel):
    if channel == "et":
        return ROOT.RDataFrame("ntuple", f"{folder}/EGamma*.root")
    elif channel == "mt":
        return ROOT.RDataFrame("ntuple", f"{folder}/*Muon*.root")
    elif channel == "tt":
        return ROOT.RDataFrame("ntuple", f"{folder}/Tau*.root")
    else:
        raise ValueError("Invalid channel specified")

def main(folder, channel, era):
    # bin_edges = [0,  50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
    #            250, 300,3000]
    # if lumi[era] < 10e3:
    bin_edges = [0,  60,  80,  100,  120, 140,  160, 180,  200,
                250, 300,3000]
    ROOT.ROOT.EnableImplicitMT()
    output_file = ROOT.TFile(f"Fraction_{era}_{channel}.root", "RECREATE")

     # Ensure default sum of squares is enabled
    ROOT.TH1.SetDefaultSumw2(True)

    # 读取数据
    df_data = load_files(folder, channel)
    df_ttbar = ROOT.RDataFrame("ntuple", f"{folder}/TTto*.root")
    df_wjets = ROOT.RDataFrame("ntuple", f"{folder}/WtoLNu-4Jets*.root")
    df_dyjets = ROOT.RDataFrame("ntuple", f"{folder}/DYto*.root")

    # 设置 cut 和 weight
    base_cut = cuts[channel]
    weight_data = "1"
    weight_expr = weight_expressions[channel][era].format(lumi[era])

    # 定义新的数据帧，将权重计算为新列
    df_data = df_data.Define("weight", weight_expr)
    df_ttbar = df_ttbar.Define("weight", weight_expr)
    df_wjets = df_wjets.Define("weight", weight_expr)
    df_dyjets = df_dyjets.Define("weight", weight_expr)

    # 定义要绘制的图形组合
    regions = {
        "tight_mTnob": f"{base_cut} && {nob} && {tight_mT}",
        "loose_mTnob": f"{base_cut} && {nob} && {loose_mT}",
        "tight_mTbtag": f"{base_cut} && {btag} && {tight_mT}",
        "loose_mTbtag": f"{base_cut} && {btag} && {loose_mT}"
    }

    for name, region_cut in regions.items():
      # 创建直方图
        hist_data = df_data.Filter(region_cut).Histo1D((variable, variable, len(bin_edges) - 1, array.array('d', bin_edges)), variable)
        hist_data.SetName(f"data_AR{name}")
        # hist_data.Write()

       # TTbar histograms
        hist_ttbar = df_ttbar.Filter(f"{region_cut} && {gen_cut}").Histo1D((variable, variable, len(bin_edges) - 1, array.array('d', bin_edges)), variable, "weight").GetValue()
        hist_ttbar.SetName(f"ttbar_AR{name}")
        # hist_ttbar.Write()

       # WJets histograms
        hist_wjets = df_wjets.Filter(f"{region_cut} && {gen_cut}").Histo1D((variable, variable, len(bin_edges) - 1, array.array('d', bin_edges)), variable, "weight").GetValue()
        hist_wjets.SetName(f"wjets_AR{name}")
        # hist_wjets.Write()

        # # DYJets histograms
        hist_dyjets = df_dyjets.Filter(f"{region_cut} && {gen_cut}").Histo1D(("mt_tot", "mt_tot", len(bin_edges) - 1, array.array('d', bin_edges)), "mt_tot", "weight").GetValue()
        hist_dyjets.SetName(f"dyjets_AR{name}")

        # QCD histograms
        hist_qcd = hist_data.Clone(f"QCD_AR{name}")
        hist_qcd.SetName(f"QCD_AR{name}")

        hist_ttbar_forqcd = df_ttbar.Filter(f"{region_cut}").Histo1D((variable, variable, len(bin_edges) - 1, array.array('d', bin_edges)), variable, "weight").GetValue()
        hist_wjets_forqcd = df_wjets.Filter(f"{region_cut}").Histo1D((variable, variable, len(bin_edges) - 1, array.array('d', bin_edges)), variable, "weight").GetValue()
        hist_dyjets_forqcd = df_dyjets.Filter(f"{region_cut}").Histo1D((variable, variable, len(bin_edges) - 1, array.array('d', bin_edges)), variable, "weight").GetValue()

        hist_qcd.Add(hist_ttbar_forqcd, -1)
        hist_qcd.Add(hist_wjets_forqcd, -1)
        hist_qcd.Add(hist_dyjets_forqcd, -1)





        # 计算每个bin的 qcd, wjets, ttbar 的比例
        n_bins = hist_qcd.GetNbinsX()

        # Set all negative bin values to 0
        def set_negative_bins_to_zero(hist):
           for bin in range(1, hist.GetNbinsX() + 1):
              if hist.GetBinContent(bin) < 0:
                 hist.SetBinContent(bin, 0)
        # hist_sum.Write()

        set_negative_bins_to_zero(hist_qcd)


        hist_qcd_fraction = hist_qcd.Clone(f"data_AR{name}mt_tot")

        hist_ttbar_fraction = hist_ttbar.Clone(f"ttbar_AR{name}mt_tot")
        hist_wjets_fraction = hist_wjets.Clone(f"wjets_AR{name}mt_tot")








        hist_sum = hist_qcd.Clone(f"Sum{name}")
        hist_sum.Add(hist_wjets)
        hist_sum.Add(hist_ttbar)




        hist_qcd_fraction.Divide(hist_sum)
        hist_ttbar_fraction.Divide(hist_sum)
        hist_wjets_fraction.Divide(hist_sum)


        # 设置直方图的横轴标签和关闭统计框
        def customize_histogram(hist):
          hist.GetXaxis().SetTitle('\\text{m}_\\text{T}^{\\text{tot}}\\text{(Gev)}')
          hist.SetStats(False)

        customize_histogram(hist_qcd_fraction)
        customize_histogram(hist_ttbar_fraction)
        customize_histogram(hist_wjets_fraction)
        




        hist_qcd_fraction.Write()
        hist_ttbar_fraction.Write()
        hist_wjets_fraction.Write()




    output_file.Close()



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Fraction.py <folder> <channel> <era>")
        sys.exit(1)

    folder = sys.argv[1]
    channel = sys.argv[2]
    era = sys.argv[3]
    main(folder, channel, era)




