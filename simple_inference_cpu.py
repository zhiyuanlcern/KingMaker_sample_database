import uproot
import numpy as np
from keras.models import load_model
import matplotlib
import matplotlib.pyplot as plt
import array
import pandas as pd
import json
import os
import ROOT as R
import sys
import tensorflow as tf
import argparse
# sys.path.append('/home/zhiyuanl/PNN/parametricnet/scripts')  
from keras import backend as K
import re
import gc
import psutil
import time
def is_ntuple_readable(file_path, tree_name="ntuple"):
    """
    检查ROOT文件是否有效且包含可读的ntuple树
    
    参数:
        file_path: ROOT文件路径
        tree_name: 要检查的树名(默认为"ntuple")
    
    返回:
        tuple: (是否有效, 错误信息)
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False, f"文件 {file_path} 不存在"
    
    # 检查文件大小
    if os.path.getsize(file_path) == 0:
        return False, f"文件 {file_path} 大小为0"
    
    try:
        # 尝试打开文件
        f = ROOT.TFile(file_path, "READ")
        if not f:
            return False, f"无法打开文件 {file_path}"
        
        if f.IsZombie():
            f.Close()
            return False, f"文件 {file_path} 已损坏(IsZombie)"
        
        # 检查是否正常关闭
        if f.TestBit(ROOT.TFile.kRecovered):
            print(f"警告: 文件 {file_path} 是恢复文件，可能不完整")
        
        # 检查是否存在ntuple树
        tree = f.Get(tree_name)
        if not tree:
            f.Close()
            return False, f"文件 {file_path} 中不存在树 {tree_name}"
        
        # 尝试读取树的条目数
        try:
            n_entries = tree.GetEntries()
            if n_entries <= 0:
                f.Close()
                return False, f"树 {tree_name} 中没有有效条目"
            
            # 尝试读取第一个条目
            tree.GetEntry(0)
        except Exception as e:
            f.Close()
            return False, f"无法读取树 {tree_name}: {str(e)}"
        
        f.Close()
        return True, "文件有效且可读"
    
    except Exception as e:
        if 'f' in locals() and f:
            f.Close()
        return False, f"检查文件时出错: {str(e)}"
def reset_keras():
    """重置Keras状态释放内存"""
    K.clear_session()
    tf.compat.v1.reset_default_graph()
    gc.collect()
def print_memory_usage(label=""):
    """打印当前进程的内存使用情况"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    # RSS: 实际物理内存使用量 (Resident Set Size)
    # VMS: 虚拟内存使用量 (Virtual Memory Size)
    print(f"{label} - RSS: {mem_info.rss / (1024 ** 2):.2f} MB, VMS: {mem_info.vms / (1024 ** 2):.2f} MB")

def column_exists(df, col_name):
    return col_name in df.columns

def get_filtered_columns(input_file, suffixs, treename='ntuple', useful_vars=[]):
    
    no_syst = "True"
    rdf = R.RDataFrame(treename, input_file)
    for v in rdf.GetColumnNames():
        if len(suffixs) > 1 and suffixs[1] in v:
            no_syst = False
    if no_syst:
        if "Run2022" in input_file or "FF_Combined" in input_file:
            suffixs =[""]
            pass
        else:
            print(f"Warning ! no systematics {suffixs[0] } for file {input_file}")
            suffixs = [""]
            pass
    all_columns = []
    columns = []
    for i in rdf.GetColumnNames():
        all_columns.append(str(i))    
    # Ensure all elements in 'all_columns' are strings
    all_columns = [col.decode() if isinstance(col, bytes) else col for col in all_columns]
    
    for suffix in suffixs:
        if suffix == "":
            for column in all_columns:
                if "__" not in column:
                    columns.append(column)
        else:
            for column in all_columns:
                if suffix in column:
                    columns.append(column)

    columns_final = []
    for i in columns:
        if i.split('__', 1)[0]  in useful_vars:
            columns_final.append(i)

    return columns_final
def read_root_with_rdataframe(file_name, treename, columns=[]):
    rdf = R.RDataFrame(treename, file_name)
    np_arrays = rdf.AsNumpy(columns =columns)
    df = pd.DataFrame(np_arrays)
    print(df.head())
    return df

def get_systematics(input_file, input_tree, input_vars=["mt_tot", "pt_vis", "m_vis", "phi_1", "phi_2", "eta_1", "eta_2", "met", "pt_1", "pt_2", "pt_tt", "mt_1", "mt_2", "deltaR_ditaupair", "metSumEt", "pzetamissvis", "dxy_1", "metphi", "mTdileptonMET", "m_fastmtt", "pt_fastmtt", "eta_fastmtt"]):
    df1 = R.RDataFrame(input_tree, input_file)
    base_vars = input_vars
    version_suffixes = set()
    base_var_regex = re.compile("(" + "|".join(base_vars) + ")(.*)")
    for colName in df1.GetColumnNames():
        match = base_var_regex.match(str(colName))
        if match and len(match.groups()) > 1:
            suffix = match.group(2)
            if suffix.startswith("__") and "_pf" not in suffix:
                ## test
                # if not "tauEs" in suffix:
                #     continue
                version_suffixes.add(suffix)
    versions = [""]
    versions.extend(version_suffixes)
    return versions

def inference(model_even, model_odd, input_file="test.root", input_var=["pt_1", "pt_2", "mt_tot"], 
              param=[1000,1200], treename="ntuple", extra_var=['Train_weight', 'event'], 
              tag='', json_file='mutau-playground-nob.rootscaler.json', output_file='', bkg_df_= pd.DataFrame()):


    # 确保定义了 column_exists 函数
    def column_exists(df, col_name):
        """检查列是否存在于DataFrame中"""
        return col_name in df.columns

    def prepare_data_with_versions(bkg_df, version, scaler, input_var):
        # 使用原地操作避免创建新列
        scaled_columns = {}
        
        # 预计算缩放参数字典
        var_to_center = dict(zip(scaler['input_vars'], scaler['center']))
        var_to_scale = dict(zip(scaler['input_vars'], scaler['scale']))
        
        result_columns = ["event"]
        
        for var in input_var:
            var_ver = f"{var}{version}"
            
            # 检查带版本的列是否存在
            if column_exists(bkg_df, var_ver):
                col_name = f"scaled_{var_ver}"
                source_col = var_ver
            else:
                col_name = f"scaled_{var}"
                source_col = var
            
            # 检查是否已存在于结果中（避免重复添加）
            if col_name not in result_columns:
                result_columns.append(col_name)
                
                # 获取缩放参数 - 使用原始变量名获取缩放参数
                center_val = var_to_center.get(var, None)  # 使用原始变量名，不带版本后缀
                scale_val = var_to_scale.get(var, None)    # 使用原始变量名，不带版本后缀
                
                if center_val is not None and scale_val is not None:
                    # 直接计算结果，不创建中间列
                    scaled_columns[col_name] = (bkg_df[source_col] - center_val) / scale_val
                else:
                    print(f"Warning: Scaling information not found for {var}")
                    # 如果找不到缩放参数，使用默认值
                    scaled_columns[col_name] = bkg_df[source_col]
        
        # 一次性创建结果DataFrame
        result_df = pd.DataFrame({
            "event": bkg_df["event"].values
        }, index=bkg_df.index)
        
        # 添加缩放列（使用values避免创建副本）
        for col_name, col_data in scaled_columns.items():
            result_df[col_name] = col_data.values
        
        return result_df

    def evaluate_scores(bkg_df_input, version, param, model_odd, model_even, input_var, scaler):
        """评估分数 - 优化内存版本"""
        # 创建结果DataFrame时只包含必要列
        result_df = pd.DataFrame(index=bkg_df_input.index)
        result_df["event"] = bkg_df_input["event"]  # 使用输入数据的事件列
        
        # 确定缩放列名 - 使用实际的列名
        scaled_input_vars = []
        for var in input_var:
            # 尝试带版本的列
            versioned_col = f"scaled_{var}{version}"
            normal_col = f"scaled_{var}"
            
            if versioned_col in bkg_df_input.columns:
                scaled_input_vars.append(versioned_col)
            elif normal_col in bkg_df_input.columns:
                scaled_input_vars.append(normal_col)
            else:
                # 如果都找不到，尝试原始列（但这种情况不应该发生）
                print(f"Warning: Missing scaled column for {var}")
                scaled_input_vars.append(var)
        
        # 计算奇偶事件的索引
        event_vals = bkg_df_input["event"].values
        sel_fold_even = (event_vals % 2 == 0)
        sel_fold_odd = (event_vals % 2 == 1)
        
        # 准备预测数据 - 使用.values避免创建副本
        even_data = bkg_df_input.loc[sel_fold_even, scaled_input_vars].values
        odd_data = bkg_df_input.loc[sel_fold_odd, scaled_input_vars].values
        
        # 获取质量参数的缩放因子
        mass_center = scaler['center'][-1]  # 假设mass是最后一个特征
        mass_scale = scaler['scale'][-1]    # 假设mass是最后一个特征
        
        version_suffix = version if version else ''
        
        # 批量处理所有参数
        predictions = {}
        for p in param:
            # 缩放质量参数
            p_scaled = (p - mass_center) / mass_scale
            
            # 同时预测奇偶事件
            # 为偶数事件添加质量列
            even_data_with_mass = np.column_stack([even_data, np.full(len(even_data), p_scaled)])
            
            # 为奇数事件添加质量列
            odd_data_with_mass = np.column_stack([odd_data, np.full(len(odd_data), p_scaled)])
            
            # 预测 - 只取S列（信号分数）
            even_predic = model_odd.predict(even_data_with_mass, batch_size=100000, verbose=0)[:, 2]
            odd_predic = model_even.predict(odd_data_with_mass, batch_size=100000, verbose=0)[:, 2]
            
            pnn_column = f"PNN_{p}{version_suffix}"
            
            # 创建数组存储结果
            predictions[pnn_column] = np.empty(len(bkg_df_input), dtype=np.float32)
            
            # 填充结果 - 保持正确的事件顺序
            predictions[pnn_column][sel_fold_even] = even_predic.flatten()
            predictions[pnn_column][sel_fold_odd] = odd_predic.flatten()
        
        # 添加预测到结果DataFrame
        for col, data in predictions.items():
            result_df[col] = data
        
        return result_df

    # 主程序部分
    with open(json_file, 'r') as f:
        scaler = json.load(f)
    print("Length of index (input_var + ['mass']):", len(input_var) + 1)
    print("input_var:", input_var)

    # 获取系统误差版本
    try:
        versions = get_systematics(input_file, treename, input_var)
    except:
        if "2HDM" in input_file or "BBH" in input_file:
            match = re.search(r'M-(\d+)_', input_file)
            if match:
                masses = [int(match.group(1))]
                versions = get_systematics(input_file, f'Xtohh{masses[0]}', input_var)
            else:
                print(f"Error: Cannot extract mass from filename: {input_file}")
                versions = []
        else:
            print(f'Error: Cannot load tree {treename} in file {input_file}')
            versions = []

    if not versions:
        print("Warning: No systematics versions found. Using empty version.")
        versions = [""]

    # 只读取必要的列（确保event列被包含）
    necessary_columns = set(["event"] + input_var + extra_var)
    columns = get_filtered_columns(input_file, versions, treename, list(necessary_columns))

    # 读取数据
    bkg_df = read_root_with_rdataframe(input_file, treename, columns) 

    # 处理每个版本
    pnns_per_version = []

    for version in versions:
        # print_memory_usage(f"开始处理系统误差 {version}")
        # print(f"Processing: {version}")
        
        try:
            # 准备数据
            bkg_df_input = prepare_data_with_versions(bkg_df, version, scaler, input_var)
            
            # 评估分数 - 只返回PNN列
            pnn_df = evaluate_scores(
                bkg_df_input=bkg_df_input, 
                version=version, 
                param=param, 
                model_odd=model_odd, 
                model_even=model_even, 
                input_var=input_var,
                scaler=scaler  # 传入scaler
            )
            
            # 只保留PNN列
            score_columns = [c for c in pnn_df.columns if c.startswith("PNN_")]
            pnn_df = pnn_df[score_columns]
            
            # 添加到结果列表
            pnns_per_version.append(pnn_df)
            
            print(f"Finished calculating scores for version: {version}")
        
        except Exception as e:
            print(f"Error processing version {version}: {str(e)}")
            # 添加空DataFrame保持对齐
            empty_df = pd.DataFrame(index=bkg_df.index)
            pnns_per_version.append(empty_df)
        
        finally:
            # 清理内存
            if 'bkg_df_input' in locals():
                del bkg_df_input
            if 'pnn_df' in locals():
                del pnn_df
            gc.collect()
            # print_memory_usage(f"结束处理系统误差 {version}")

    # 合并所有PNN列
    if pnns_per_version:
        final_df = pd.concat(pnns_per_version, axis=1)
    else:
        print("Warning: No PNN scores generated. Creating empty DataFrame.")
        final_df = pd.DataFrame(index=bkg_df.index)

    data = final_df
            

    return data



def merge_trees_with_cpp(input_file, pnn_files):
    """
    使用C++高效合并树
    
    参数:
        input_file: 主输入ROOT文件路径
        pnn_files: 要合并的PNN文件路径列表
        output_file: 合并后的输出文件路径
    """
    # 记录开始时间
    start_time = time.time()
    
    # 编译C++代码（如果尚未编译）
    cpp_file = "/data/bond/zhiyuanl/PNN/parametricnet/merge_trees.cpp"
    if not os.path.exists(cpp_file):
        print(f"Error: C++ source file {cpp_file} not found!")
        return
    
    # 检查是否已经编译
    if not hasattr(R, 'merge_trees'):
        print("Compiling C++ code...")
        exit_code = R.gInterpreter.ProcessLine(f".L {cpp_file}+")
        if exit_code != 0:
            print(f"Error compiling C++ code. Exit code: {exit_code}")
            return
    
    # 创建C++的字符串vector
    pnn_vec = R.std.vector['std::string']()
    for f in pnn_files:
        pnn_vec.push_back(f)
    output_file = f'tmptmpcombined_{os.path.basename(input_file)}'
    # 调用C++函数
    print(f"Starting merge with C++ implementation...")
    R.merge_trees(input_file, pnn_vec, output_file)
    
    # 记录结束时间
    end_time = time.time()
    print(f"Total Python execution time: {end_time - start_time:.2f} seconds")
    
    return output_file

if __name__ == "__main__":
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)

    import warnings

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',  type=str)
    parser.add_argument('--tag',  type=str, default="run1")
    parser.add_argument('--input_vars', nargs='+', type=str)
    parser.add_argument('--extra_vars', nargs='+', type=str, default = ['Train_weight', 'event'])
    parser.add_argument('--even_model', type=str, default="modeleven-mutau-playground-nob.root.h5")
    parser.add_argument('--odd_model', type=str, default="modelodd-mutau-playground-nob.root.h5")
    parser.add_argument('--json_file',  type=str, default="mutau-playground-nob.rootscaler.json")
    parser.add_argument('--compare', type = int, default=0)
    parser.add_argument('--lowmass', type = int, default=0)
    parser.add_argument('--treename', type = str, default='ntuple')
    args = parser.parse_args()

    input_vars = args.input_vars
    print(input_vars)
    tag = args.tag
    # if args.lowmass:
    #     masses = [60,70, 80,  90,  100,  110,  120,    130,  140,  160,  180,] #65,75,85,95,105,115,125,135, 200,250
    # else:
    #     masses = [300,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200,3500,]


    

    # masses_group =[[60,70, 80,], [90,  100,  110],  [120, 65,75, ] , [85,95,105] , [115,125,  130],  [140,  160,  180], [135, 200,250]] 
    # masses_group =[[60,70, 80,]] 
    # masses_group =[[60, 80,   100,   125,  160, 200] ] 
    masses =[60,70, 80, 90,  100, 110,  120, 65 ,75,85,95,105,115,125,  130,  140,  160,  180, 135, 200,250] 
    
    # pnn_files =["PNN_tmp_60TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8Run3Summer23BPixNanoAODv12_tt_bkp.root",     "PNN_tmp_70TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8Run3Summer23BPixNanoAODv12_tt_bkp.root",     "PNN_tmp_80TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8Run3Summer23BPixNanoAODv12_tt_bkp.root",     ]
    # merge_trees_with_cpp(args.input_file,pnn_files) 
    pnn_files = []
    # for masses in masses_group:
    run=False
    rdf = R.RDataFrame(args.treename, args.input_file)
    input_file = args.input_file
    for m in masses:
        finished = False
        print_memory_usage(f"开始处理质量点 {m}")
        bkg_df_initial =  pd.DataFrame()
        result_df_initial =pd.DataFrame()
        if "PNN_tmp" in input_file:
            print("this should not run on the PNN tmp file")
            sys.exit()
        score_output_filename = f'PNN_tmp_{tag}{m}{os.path.basename(args.input_file)}'
        
        if "2HDM" in args.input_file or "BBH" in args.input_file:
            match = re.search(r'M-(\d+)_', args.input_file)
            masses_check = [int(match.group(1))]
            if int(m) != int(masses_check[0]):
                print(f"signal samples skipping for mass {m}")
                continue
            if f'PNN_{masses_check[0]}' in rdf.GetColumnNames():
                    print(f"{args.input_file} has already finished PNN calculation. Nice.")
                    sys.exit(0)
                    # continue
            else: 
                run = True
            
    
        if f'PNN_{m}' in rdf.GetColumnNames():
            print(f"{args.input_file} has already finished PNN {m} calculation. Nice.")
            continue
        else:
            run = True
        if os.path.exists(f'PNN_tmp_{tag}{m}{os.path.basename(input_file)}'):
                print(f"文件 {score_output_filename} 已经存在")
                
                if f'PNN_{m}' in rdf.GetColumnNames():
                    print(f"{args.input_file} 文件存在并且已经合并. Nice.")
                    continue
                else:
                    if is_ntuple_readable(score_output_filename):
                        print(f"文件 {score_output_filename} 存在且没有问题，但未合并到主文件")
                        pnn_files.append(score_output_filename)
                        continue
        
    if run:
        if gpus:
            strategy = tf.distribute.MirroredStrategy()
            with strategy.scope():
                model_even = load_model(args.even_model)
                model_odd = load_model(args.odd_model)
        else:
            model_even = load_model(args.even_model)
            model_odd = load_model(args.odd_model)    


        for m in masses:
            if "2HDM" in args.input_file or "BBH" in args.input_file:
                match = re.search(r'M-(\d+)_', args.input_file)
                masses_check = [int(match.group(1))]
                if int(m) != int(masses_check[0]):
                    print(f"signal samples skipping for mass {m}")
                    continue
            score_output_filename = f'PNN_tmp_{tag}{m}{os.path.basename(args.input_file)}'
            print(f"开始处理质量点 {m}")
            print_memory_usage(f"质量点 {m} - 推理前")
            df_result = inference(model_even, model_odd,  input_file, input_vars,  [m], 
                        args.treename, args.extra_vars, tag, args.json_file, score_output_filename,bkg_df_initial)
            
            print_memory_usage(f"质量点 {m} - 推理后")
            print(f"saving to file {score_output_filename}")
            print_memory_usage(f"质量点 {m} - 转换为RDF前")
            final_result_df = R.RDF.FromPandas(df_result)

            final_result_df.Snapshot(args.treename, score_output_filename)    
            del final_result_df, df_result
        
    
            pnn_files.append(score_output_filename)
            print_memory_usage(f"质量点 {m} - 释放内存后")
    if pnn_files:
        print_memory_usage("合并树前")
        merge_trees_with_cpp(args.input_file,pnn_files) 
        print_memory_usage("合并树后")
        reset_keras()

        
    else:
        print(f"finished for masses {masses}")
        
    del rdf,score_output_filename
    
    
    
    
    gc.collect()
    
    completed_all = True
    
    if completed_all:
        os.system(f'mv tmptmpcombined_{tag}{os.path.basename(args.input_file)} {args.input_file}')
        # os.system(f'rm {score_output_filename}')
    # for m in masses:
    #     os.system(f"rm PNN_tmp_{tag}{m}{os.path.basename(args.input_file)}")



    print("All masses processed.")
        