#include <TFile.h>
#include <TTree.h>
#include <vector>
#include <string>
#include <iostream>

void merge_trees(const char* main_file, const std::vector<std::string>& pnn_files, const char* output_file) {
    // 1. 打开主文件
    TFile* main_f = TFile::Open(main_file, "READ");
    TTree* main_tree = (TTree*)main_f->Get("ntuple");
    Long64_t n_entries = main_tree->GetEntries();
    
    // 2. 打开所有PNN文件
    std::vector<TFile*> pnn_files_holder;
    std::vector<TTree*> pnn_trees;
    
    for (const auto& fname : pnn_files) {
        TFile* f = TFile::Open(fname.c_str(), "READ");
        if (!f) continue;
        
        TTree* tree = (TTree*)f->Get("ntuple");
        if (tree && tree->GetEntries() == n_entries) {
            pnn_files_holder.push_back(f);
            pnn_trees.push_back(tree);
        } else {
            f->Close();
        }
    }
    
    // 3. 创建输出文件
    TFile* out_f = TFile::Open(output_file, "RECREATE");
    TTree* out_tree = main_tree->CloneTree(0);
    
    // 4. 添加新分支并管理存储空间
    std::map<std::string, float> branch_values;  // 存储所有分支值的映射
    
    for (size_t i = 0; i < pnn_trees.size(); i++) {
        TObjArray* br_list = pnn_trees[i]->GetListOfBranches();
        for (int j = 0; j < br_list->GetEntries(); j++) {
            TBranch* br = (TBranch*)br_list->At(j);
            const char* br_name = br->GetName();
            
            // 跳过主树已有的分支
            if (main_tree->GetBranch(br_name)) continue;
            
            // 如果分支尚未创建，则创建它
            if (branch_values.find(br_name) == branch_values.end()) {
                float value = 0;
                branch_values[br_name] = value;
                out_tree->Branch(br_name, &branch_values[br_name], (std::string(br_name) + "/F").c_str());
            }
            
            // 设置PNN树的分支地址
            pnn_trees[i]->SetBranchAddress(br_name, &branch_values[br_name]);
        }
    }
    
    // 5. 合并数据
    for (Long64_t i = 0; i < n_entries; i++) {
        main_tree->GetEntry(i);
        
        // 从所有PNN树读取数据
        for (auto tree : pnn_trees) {
            tree->GetEntry(i);
        }
        
        out_tree->Fill();
        
        // 进度显示
        if (i % 100000 == 0) {
            std::cout << "Processing entry " << i << "/" << n_entries << std::endl;
        }
    }
    
    // 6. 保存结果
    out_tree->Write();
    out_f->Close();
    main_f->Close();
    
    // 清理PNN文件
    for (auto f : pnn_files_holder) {
        f->Close();
    }
    
    std::cout << "Merge completed. Output saved to " << output_file << std::endl;
}
