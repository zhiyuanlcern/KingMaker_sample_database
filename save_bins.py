import ROOT
import sys

# 打开 ROOT 文件
# root_file = ROOT.TFile.Open("2022postEE_mt_Version11_nominal_output_PNN_100_ggH_signal_.root")
root_file = ROOT.TFile.Open(sys.argv[1])
# 定义需要遍历的目录列表
outname = sys.argv[1].strip("_signal_.root")
    
directories = ["nob1", "nob2", "nob3", "nob4", "nob5","btag"]
for dir_name in directories:
    # 进入目录
    dir_obj = root_file.Get(dir_name)
    if not dir_obj:
        print(f"目录 {dir_name} 不存在，跳过！")
        continue
    
    # 获取直方图 data_obs
    hist = dir_obj.Get("data_obs")
    if not hist:
        print(f"目录 {dir_name} 中未找到 data_obs，跳过！")
        continue
    
    # 提取 X 轴 bin edges
    x_axis = hist.GetXaxis()
    n_bins = x_axis.GetNbins()
    bin_edges = [x_axis.GetBinLowEdge(i) for i in range(1, n_bins + 2)]  # 包含最后一个边界
    
    # 写入 TXT 文件
    with open(f"bin_edges/{outname}{dir_name}_bin_edges.txt", "w") as f:
        f.write("[")
        for edge in bin_edges:
            f.write(f"{edge},")
        f.write("]")
    
    # print(f"目录 {dir_name} 的 bin edges 已保存至 {dir_name}_bin_edges.txt")

# 关闭 ROOT 文件
root_file.Close()


# for f in 2022postEE_mt_Version11_nominal_output_PNN_100_ggH_signal_.root 2022postEE_et_Version11_nominal_output_PNN_100_ggH_signal_.root 2022postEE_tt_Version11_nominal_output_PNN_100_ggH_signal_.root 2022postEE_em_Version11_nominal_output_PNN_100_ggH_signal_.root ;
# do python save_bins.py $f &
# done

# for f in 2023_mt_Version11_nominal_output_PNN_100_ggH_signal_.root 2023_et_Version11_nominal_output_PNN_100_ggH_signal_.root 2023_tt_Version11_nominal_output_PNN_100_ggH_signal_.root 2023_em_Version11_nominal_output_PNN_100_ggH_signal_.root ;
# do python save_bins.py $f &
# done

# for f in 2022postEE_mt_Version11_nominal_output_PNN_200_ggH_signal_.root 2022postEE_et_Version11_nominal_output_PNN_200_ggH_signal_.root 2022postEE_tt_Version11_nominal_output_PNN_200_ggH_signal_.root 2022postEE_em_Version11_nominal_output_PNN_200_ggH_signal_.root ;
# do python save_bins.py $f &
# done

# for f in 2023_mt_Version11_nominal_output_PNN_200_ggH_signal_.root 2023_et_Version11_nominal_output_PNN_200_ggH_signal_.root 2023_tt_Version11_nominal_output_PNN_200_ggH_signal_.root 2023_em_Version11_nominal_output_PNN_200_ggH_signal_.root ;
# do python save_bins.py $f &
# done



# for f in 2022EE_mt_Version11_nominal_output_PNN_100_ggH_signal_.root 2022EE_et_Version11_nominal_output_PNN_100_ggH_signal_.root 2022EE_tt_Version11_nominal_output_PNN_100_ggH_signal_.root 2022EE_em_Version11_nominal_output_PNN_100_ggH_signal_.root ;
# do python save_bins.py $f &
# done

# for f in 2023BPix_mt_Version11_nominal_output_PNN_100_ggH_signal_.root 2023BPix_et_Version11_nominal_output_PNN_100_ggH_signal_.root 2023BPix_tt_Version11_nominal_output_PNN_100_ggH_signal_.root 2023BPix_em_Version11_nominal_output_PNN_100_ggH_signal_.root ;
# do python save_bins.py $f &
# done
# wait 
# for f in 2022EE_mt_Version11_nominal_output_PNN_200_ggH_signal_.root 2022EE_et_Version11_nominal_output_PNN_200_ggH_signal_.root 2022EE_tt_Version11_nominal_output_PNN_200_ggH_signal_.root 2022EE_em_Version11_nominal_output_PNN_200_ggH_signal_.root ;
# do python save_bins.py $f &
# done

# for f in 2023BPix_mt_Version11_nominal_output_PNN_200_ggH_signal_.root 2023BPix_et_Version11_nominal_output_PNN_200_ggH_signal_.root 2023BPix_tt_Version11_nominal_output_PNN_200_ggH_signal_.root 2023BPix_em_Version11_nominal_output_PNN_200_ggH_signal_.root ;
# do python save_bins.py $f &
# done