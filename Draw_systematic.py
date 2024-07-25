import uproot
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import awkward as ak
import ROOT as R

def get_variable(tree, var_base, var_suffix=""):
    var_name = f"{var_base}{var_suffix}"
    if var_name in tree.keys():
        var = tree[var_name]
        dtype = var.dtype
        # print(var_name, dtype)
        if not np.issubdtype(dtype, np.number) or dtype == np.uint8 or dtype == np.int16:
            var = var.astype(np.int32)
        return var
    else:
        var = tree[var_base]
        dtype = var.dtype
        # print(var_name, dtype)
        if not np.issubdtype(dtype, np.number) or dtype == np.uint8 or dtype == np.int16:
            var = var.astype(np.int32)       
        return var
# Function to save numpy arrays as ROOT histograms
def save_hist_to_root(hist_data, bins, var, output_file):
    if os.path.exists(output_file):
        root_file = R.TFile(output_file, "UPDATE")
    else:
        root_file = R.TFile(output_file, "RECREATE")
    hist_name = f"{var}"
    root_hist = R.TH1F(hist_name, hist_name, len(bins)-1, bins)
    for i, count in enumerate(hist_data[var]):
        root_hist.SetBinContent(i+1, count)
    root_hist.Write()
    root_file.Close()
def main(folder_path, era,variables, suffixs,   channel, btag):
    os.system(f'mkdir -p {folder_path}_output')
    def check_finshed(filename):
        f_strip = filename.replace(".root", "")
        if "2HDM" in filename:
            match = re.search(r'Hto2Tau_M-(\d+)', filename)
            masses_check = [int(match.group(1))]
            m = masses_check[0]
            if str(m) not in var and (var != "mt_tot") :
                print(f"no need to run for PNN score {folder_path}_output/{f_strip}_era_{var + suffixs[1]}_{btag}")
                return 1
        
        if os.path.exists(f"{folder_path}_output/{f_strip}_era_{var + suffixs[1]}_{btag}.png") and os.path.exists(f"{folder_path}_output/{f_strip}_era_{var + suffixs[1]}_{btag}.root"):
            print(f"already finshed running for {folder_path}_output/{f_strip}_era_{var + suffixs[1]}_{btag}")
            return 1
        else:
            return 0
    if "" not in suffixs: 
            suffixs.insert(0, "")
    if era == "2022EE":
        lumi = 7.875e3
    elif era == "2022postEE":
        lumi = 26.337e3
    else:
        raise ValueError("Error: Year not found {}".format(era))
    # 遍历文件夹中的所有 ROOT 文件
    for filename in os.listdir(folder_path):
        f_strip = filename.replace(".root", "")
        finished = True
        for var in variables:
            if check_finshed(filename):
                continue
            else: 
                finished = False
        if finished:
            continue
        # 初始化空列表来存储所有文件中的数据
        data = {}
        weights = {}
        if not filename.endswith(".root"):
            continue
        for var in variables:
            for suffix in suffixs:
                data[var + suffix] = []
                weights[var + suffix] = []
        if filename.endswith(".root"):
            file_path = os.path.join(folder_path, filename)
            print("reading file: ", filename)
            # 打开 ROOT 文件
            rdf = R.RDataFrame("ntuple", file_path)
            # file = uproot.open(file_path)
            # 获取 TTree
            # tree = file["ntuple"]
            tree = rdf.AsNumpy()
            print('converting rdf to numpy')
            # 提取变量数据并累积
            
            for suffix in suffixs:
                print(f"processing {suffix}")
                extramuon_veto = get_variable(tree, "extramuon_veto",suffix)
                extraelec_veto = get_variable(tree, "extraelec_veto",suffix)
                eta_1 = get_variable(tree, "eta_1",suffix)
                dz_1 = get_variable(tree, "dz_1",suffix)
                dxy_1 = get_variable(tree, "dxy_1",suffix)
                iso_1 = get_variable(tree, "iso_1",suffix)
                phi_2 = get_variable(tree,"phi_2",suffix)
                deltaR_ditaupair = get_variable(tree, "deltaR_ditaupair",suffix)
                pt_1 = get_variable(tree, "pt_1",suffix)
                eta_2 = get_variable(tree, "eta_2",suffix)
                dz_2 = get_variable(tree, "dz_2",suffix)
                dxy_2 = get_variable(tree, "dxy_2",suffix)
                iso_2 = get_variable(tree, "iso_2",suffix)
                pt_2 = get_variable(tree, "pt_2",suffix)
                nbtag = get_variable(tree, "nbtag",suffix)
                q_1 = get_variable(tree, "q_1",suffix)
                q_2 = get_variable(tree, "q_2",suffix)
                puweight = get_variable(tree, "puweight",suffix)
                Xsec = get_variable(tree, "Xsec",suffix)
                genWeight = get_variable(tree, "genWeight",suffix)
                genEventSumW = get_variable(tree, "genEventSumW",suffix)
                gen_match_2 = get_variable(tree, "gen_match_2",suffix)
                is_wjets = get_variable(tree, "is_wjets",suffix)
                btag_weight = get_variable(tree, "btag_weight",suffix)
                if channel == "em":
                    id_wgt_ele_wpTight = get_variable(tree, "id_wgt_ele_wpTight",suffix)
                    id_wgt_mu_2 = get_variable(tree, "id_wgt_mu_2",suffix)
                    trg_cross_mu23ele12 = get_variable(tree, "trg_cross_mu23ele12",suffix)
                    trg_cross_mu8ele23 = get_variable(tree, "trg_cross_mu8ele23",suffix)
                    trg_single_ele30 = get_variable(tree, "trg_single_ele30",suffix)
                    trg_single_ele32 = get_variable(tree, "trg_single_ele32",suffix)
                    trg_single_ele35 = get_variable(tree, "trg_single_ele35",suffix)
                    trg_single_mu24 = get_variable(tree, "trg_single_mu24",suffix)
                    trg_single_mu27 = get_variable(tree, "trg_single_mu27",suffix)
                    trg_wgt_single_mu24 = get_variable(tree, "trg_wgt_single_mu24",suffix)
                    trg_wgt_single_ele30 = get_variable(tree, "trg_wgt_single_ele30",suffix)
                if channel == "mt":
                    trg_cross_mu20tau27_hps = get_variable(tree, "trg_cross_mu20tau27_hps")
                    trg_single_tau180_2 = get_variable(tree, "trg_single_tau180_2")
                    trg_single_mu24 = get_variable(tree, "trg_single_mu24")
                    trg_single_mu27 = get_variable(tree, "trg_single_mu27")
                    id_tau_vsMu_Loose_2 = get_variable(tree, "id_tau_vsMu_Loose_2")
                    id_tau_vsJet_Medium_2 = get_variable(tree, "id_tau_vsJet_Medium_2")
                    id_tau_vsEle_VVLoose_2 = get_variable(tree, "id_tau_vsEle_VVLoose_2")
                    id_wgt_tau_vsJet_Medium_2 = get_variable(tree, "id_wgt_tau_vsJet_Medium_2")
                    FF_weight = get_variable(tree, "FF_weight")
                    iso_wgt_mu_1 = get_variable(tree, "iso_wgt_mu_1")
                    trg_wgt_ditau_crosstau_2 = get_variable(tree, "trg_wgt_ditau_crosstau_2")
                    id_wgt_tau_vsMu_Tight_2 = get_variable(tree, "id_wgt_tau_vsMu_Tight_2")
                    id_wgt_mu_1 = get_variable(tree, "id_wgt_mu_1")
                if channel == 'et': 
                    trg_single_ele30 = get_variable(tree, "trg_single_ele30")    
                    trg_single_ele32 = get_variable(tree, "trg_single_ele32")
                    trg_single_ele35 = get_variable(tree, "trg_single_ele35")
                    trg_single_tau180_2 = get_variable(tree, "trg_single_tau180_2")
                    id_tau_vsMu_VLoose_2 = get_variable(tree, "id_tau_vsMu_VLoose_2")
                    id_tau_vsEle_Tight_2 = get_variable(tree, "id_tau_vsEle_Tight_2")
                    id_tau_vsJet_Medium_2 = get_variable(tree, "id_tau_vsJet_Medium_2")
                    id_wgt_tau_vsJet_Medium_2 = get_variable(tree, "id_wgt_tau_vsJet_Medium_2")
                    FF_weight = get_variable(tree, "FF_weight")
                    id_wgt_tau_vsEle_Tight_2 = get_variable(tree, "id_wgt_tau_vsEle_Tight_2")
                    id_wgt_ele_wpTight = get_variable(tree, "id_wgt_ele_wpTight")
                    trg_wgt_single_ele30 = get_variable(tree, "trg_wgt_single_ele30")
                    trg_wgt_ditau_crosstau_2 = get_variable(tree, "trg_wgt_ditau_crosstau_2")
                if channel == "tt":
                    trg_double_tau30_plusPFjet60 = get_variable(tree, "trg_double_tau30_plusPFjet60")
                    trg_double_tau30_plusPFjet75 = get_variable(tree, "trg_double_tau30_plusPFjet75")
                    trg_double_tau35_mediumiso_hps = get_variable(tree, "trg_double_tau35_mediumiso_hps")
                    trg_single_deeptau180_1 = get_variable(tree, "trg_single_deeptau180_1")
                    trg_single_deeptau180_2 = get_variable(tree, "trg_single_deeptau180_2")
                    id_tau_vsJet_Medium_1 = get_variable(tree, "id_tau_vsJet_Medium_1")
                    id_tau_vsEle_VVLoose_1 = get_variable(tree, "id_tau_vsEle_VVLoose_1")
                    id_tau_vsMu_VLoose_1 = get_variable(tree, "id_tau_vsMu_VLoose_1")
                    id_tau_vsJet_Medium_2 = get_variable(tree, "id_tau_vsJet_Medium_2")
                    id_tau_vsEle_VVLoose_2 = get_variable(tree, "id_tau_vsEle_VVLoose_2")
                    id_tau_vsMu_VLoose_2 = get_variable(tree, "id_tau_vsMu_VLoose_2")
                    id_wgt_tau_vsJet_Medium_2 = get_variable(tree, "id_wgt_tau_vsJet_Medium_2")
                    id_wgt_tau_vsJet_Medium_1 = get_variable(tree, "id_wgt_tau_vsJet_Medium_1")
                    FF_weight = get_variable(tree, "FF_weight")
                    trg_wgt_ditau_crosstau_1  = get_variable(tree, "trg_wgt_ditau_crosstau_1 ")
                    trg_wgt_ditau_crosstau_2 = get_variable(tree, "trg_wgt_ditau_crosstau_2")
                selection_dic = {} 
                if channel == "mt":
                    selection_dic["mt"] = (((trg_cross_mu20tau27_hps==1)|(trg_single_mu24==1)|(trg_single_mu27==1)|(trg_single_tau180_2==1)) & \
                        (pt_1 > 25.0) & (pt_2 > 30) & (extramuon_veto == 0)  &  (extraelec_veto == 0) & \
                        (id_tau_vsMu_Loose_2 > 0) & (id_tau_vsJet_Medium_2 > 0) & (id_tau_vsEle_VVLoose_2 > 0 ) & \
                        (( (gen_match_2 != 6) & (is_wjets>0) ) | (is_wjets <1)  ) &  ((q_1 * q_2) < 0) )
                    selection_dic["nob_mt"] = selection_dic["mt"] & (nbtag == 0)
                    selection_dic["btag_mt"] = selection_dic["mt"] & (nbtag == 1)
                elif channel == "et":
                    selection_dic["et"] = (((trg_single_ele30 ==1)| (trg_single_ele32==1)|(trg_single_ele35==1)|(trg_single_tau180_2==1))& \
                        (pt_1 > 30) & (pt_2 > 30)  &  (extramuon_veto == 0)  & (extraelec_veto == 0) & \
                        (id_tau_vsMu_VLoose_2 > 0)  & (id_tau_vsEle_Tight_2 > 0) & (id_tau_vsJet_Medium_2 > 0 ) & \
                        ((   (gen_match_2 != 6) & (is_wjets>0) ) | (is_wjets <1)  ) & ((q_1 * q_2) < 0) )  # 
                    selection_dic["nob_et"] = selection_dic["et"] & (nbtag == 0)
                    selection_dic["btag_et"] = selection_dic["et"] & (nbtag == 1)
                    if era == "2022postEE":
                        selection_dic["nob_et"] = selection_dic["et"] & (nbtag == 0) &~  (  ( (phi_2>1.8) & (phi_2< 2.7) & (eta_2 > 1.5)  & (eta_2<2.2) ) )
                        selection_dic["btag_et"] = selection_dic["et"] & (nbtag == 1) &~ (  ( (phi_2>1.8) & (phi_2< 2.7) & (eta_2 > 1.5)  &(eta_2<2.2) ) )
                elif channel == "tt":
                    selection_dic["tt"] = ((trg_double_tau35_mediumiso_hps==1) | (trg_single_deeptau180_1==1) | (trg_single_deeptau180_2==1) | (trg_double_tau30_plusPFjet60==1) | (trg_double_tau30_plusPFjet75==1))& \
                        (pt_1 > 40) & (pt_2 > 40) & (extramuon_veto == 0) & (extraelec_veto == 0) & \
                        (dz_1 < 0.2) & (dz_2 < 0.2) & (eta_1 < 2.1) & (eta_1 > -2.1) & (eta_2 < 2.1) & (eta_2 > -2.1) & \
                        ((id_tau_vsJet_Medium_1 > 0) & (id_tau_vsEle_VVLoose_1 > 0) & (id_tau_vsMu_VLoose_1 > 0))& \
                        ((id_tau_vsJet_Medium_2 > 0) & (id_tau_vsEle_VVLoose_2 > 0) & (id_tau_vsMu_VLoose_2 > 0))& \
                        (deltaR_ditaupair > 0.5) & ((q_1 * q_2) < 0)
                    selection_dic["btag_tt"] = selection_dic["tt"] & (nbtag ==1) 
                    selection_dic["nob_tt"] = selection_dic["tt"] & (nbtag ==0)
                elif channel == "em":
                    selection_dic["em"] = ((extramuon_veto == 0) & (extraelec_veto == 0) & \
                                ((trg_cross_mu23ele12 == 1) | (trg_cross_mu8ele23 == 1) | (trg_single_ele30 == 1) |
                                (trg_single_ele32 == 1) | (trg_single_ele35 == 1) | (trg_single_mu24 == 1) | (trg_single_mu27 == 1)) & \
                                ((eta_1 > -2.4) & (eta_1 < 2.4) & (dz_1 < 0.2) & (dxy_1 < 0.045) & (iso_1 < 0.15) & \
                                (deltaR_ditaupair > 0.3) & (pt_1 > 15)) & \
                                ((eta_2 > -2.4) & (eta_2 < 2.4) & (dz_2 < 0.2) & (dxy_2 < 0.045) & (iso_2 < 0.2) & (pt_2 > 15)) & \
                                (nbtag == 0) & ((q_1 * q_2) < 0))
                else:
                    print("wrong channel provided!! ")
                # selection = ((nbtag == 0))
                # 应用筛选条件
                print("applying selection")
                selection = selection_dic[f'{btag}_{channel}']
                for var in variables:
                    ## skip for finshed files
                    if check_finshed(filename):
                        continue
                    data[var + suffix ].append(get_variable(tree, var, suffix)[selection])

 
                # 计算 train_weight
                train_weight_dic = {}
                if channel =="em":
                    train_weight_dic["em"] = (Xsec * lumi * genWeight / genEventSumW *((trg_wgt_single_ele30 * (trg_single_ele30 > 0) + 1 * (trg_single_ele30 < 1)) *id_wgt_ele_wpTight * id_wgt_mu_2 * btag_weight * puweight *(trg_wgt_single_mu24 * (trg_single_mu24 > 0) + 1 * (trg_single_mu24 < 1))))
                elif channel =="tt":
                    train_weight_dic["tt"] = Xsec * lumi * puweight * genWeight/genEventSumW * btag_weight *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 * FF_weight * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 
                elif channel == "mt":
                    train_weight_dic["mt"] = Xsec * lumi * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight *id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1 
                elif channel == "et":
                    train_weight_dic["et"] = Xsec * lumi *  puweight * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2  *  btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2  * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30 
                train_weight = train_weight_dic[channel]
                # 应用筛选条件并累积权重数据
                for var in variables:
                    if check_finshed(filename):
                        continue
                    weights[var + suffix].append(train_weight[selection])


        # 绘制主图上的直方图
        colors = ['blue', 'red', 'green']
        hist_data = {}
        for j, var in enumerate(variables):
            if check_finshed(filename):
                        continue
            # 创建主图和子图
            fig, (ax_main, ax_ratio) = plt.subplots(nrows=2, ncols=1, sharex=True, 
                                                gridspec_kw={'height_ratios': [3, 1]}, figsize=(8, 6))
            for i, suffix in enumerate(suffixs):
                if var == "mt_tot":
                    bins = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,2100.0,5000.0]
                else:
                    bins = np.linspace(0, 1, 2001).tolist() 
                hist_data[var+suffix], bins, _ = ax_main.hist(data[var+suffix], bins=bins, histtype='step', 
                                                    label=var, color=colors[(i+j) % len(colors)], weights=weights[var+suffix])

            # 设置x轴为对数刻度
            # ax_main.set_xscale('log')

            # 添加主图标题和标签
            ax_main.set_title(f'{var}')
            ax_main.set_ylabel('Events')
            ax_ratio.set_ylim(0.8, 1.2)
            ax_main.legend()

            # 计算和绘制比例图
            # print(hist_data)
            ratio_up = np.divide(hist_data[var + suffixs[1]], hist_data[var], out=np.zeros_like(hist_data[var + suffixs[1]]), where=hist_data[var]!=0)
            ratio_down = np.divide(hist_data[var + suffixs[2]], hist_data[var], out=np.zeros_like(hist_data[var + suffixs[2]]), where=hist_data[var]!=0)

            # 绘制比例图
            ax_ratio.hist(bins[:-1], bins, weights=ratio_up, histtype='step', label='mt_tot_up / btag', color='red')
            ax_ratio.hist(bins[:-1], bins, weights=ratio_down, histtype='step', label='mt_tot_down / btag', color='green')
            ax_ratio.axhline(1, color='black', linestyle='--')
            # 设置比例图标签
            ax_ratio.set_xlabel(f'{var}')
            ax_ratio.set_ylabel('Ratio')
            ax_ratio.legend()

            # 保存图形为文件
            # Save histograms to a ROOT file
            # save_hist_to_root(hist_data, bins, variables, "output_histograms.root")
            
            plt.savefig(f"{folder_path}_output/{f_strip}_era_{var + suffixs[1]}_{btag}.png")
            # plt.clf()
            for suffix in suffixs:
                save_hist_to_root(hist_data, bins, var+suffix,  f"{folder_path}_output/{f_strip}_era_{var + suffixs[1]}_{btag}.root")
            print(f"Figure saved as {folder_path}_output/{f_strip}_era_{var + suffixs[1]}_{btag}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot btag variables from ROOT files with weights.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing ROOT files')
    parser.add_argument('--shift', nargs='+', type=str, help='Shift to plot (e.g., __jesUncTotalUp)')
    parser.add_argument('--era', type=str, default='2022postEE', help='input era, 2022postEE or 2022EE')
    parser.add_argument('--channel', type=str, default='mt', help='decay channel, mt, et, tt, em')
    parser.add_argument('--btag', type=str, default='nob', help='btag selection, nob, btag')
    parser.add_argument('--PNN', type=int, default=1, help='run PNN score or mt_tot')
    args = parser.parse_args()
    bins = np.linspace(0, 1, 2001).tolist()  # 2001 points to get 2000 intervals
    # bins = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,2100.0,5000.0]

    # variables = [args.variables, args.variables + args.shift[0], args.variables + args.shift[1]]
    mass = [60,65, 70,75, 80, 85, 90, 95, 100, 105, 110, 115, 120,   125,  130, 135, 140,  160,  180, 200,250]
    PNN_vars= [f"PNN_{m}" for m in mass]
    PNN_vars.append("mt_tot")
    main(args.folder_path,args.era, PNN_vars, args.shift, args.channel, args.btag)
    