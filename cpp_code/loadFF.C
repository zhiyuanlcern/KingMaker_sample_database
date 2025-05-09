// {
// // TFile* f = new TFile("fixbtag_nprebtagjets/FakeFactor.root"); // here to be modify
// TFile* f_fraction = new TFile("Fraction_new.root"); // here to be modify
// map<TString,TH1F*> Weights;
// // std::vector<TString> DR = {"DR_ttbar", "DR_W", "DR_QCD"};
// // std::vector<TString> region = {"nob_loose_mT", "nob_tight_mT", "btag_tight_mT","btag_loose_mT" } ;
// std::vector<TString> DR = {"data", "wjets", "ttbar"};
// std::vector<TString> region = {"tight_mTnob", "tight_mTbtag", "loose_mTnob","loose_mTbtag" } ;

//   for (auto& d : DR){
//     for (auto& r : region){
//       // "FF/DR_W/FFDR_Wpt_20preb0
//       // TString histname = "FF/"  + d  + "/FF" + d  + "pt_2" + n + r  ;
//       TString histname = d + "_AR" + r + "mt_tot";
//       TH1F* h = (TH1F*) f_fraction ->Get(histname); 
//       h->SetDirectory(0);
//       Weights[histname] = h;    
//     }
//   }
// }

///////

#include <TFile.h>
#include <TH1F.h>
#include <TString.h>
#include <map>
#include <vector>
#include <string>
map<TString,TH1F*> Weights;
void loadFF(TString era, TString channel) {
    // 构造文件名
    TString filename = "sample_database/fractions/Fraction_" + era + "_" + channel + ".root";
    std::cout<< filename << std::endl;
    // 打开文件
    TFile* f_fraction = new TFile(filename); // 动态加载根文件
    std::cout<< f_fraction << std::endl;
    // 定义权重字典
    

    // 定义 DR 和 region 向量
    std::vector<TString> DR = {"data", "wjets", "ttbar"};
    std::vector<TString> region = {"tight_mTnob", "tight_mTbtag", "loose_mTnob", "loose_mTbtag"};

    for (auto& d : DR) {
        for (auto& r : region) {
            TString histname = d + "_AR" + r + "mt_tot";
            std::cout<< histname << std::endl;
            TH1F* h = (TH1F*) f_fraction->Get(histname);
            h->SetDirectory(0);
            Weights[histname] = h;
        }
    }
}





// #include <TFile.h>
// #include <TH1F.h>
// #include <TString.h>
// #include <TCanvas.h>
// #include <map>
// #include <vector>
// #include <string>

// void loadFF(TString era, TString channel) {
//     // 构造文件名
//     TString filename = "Fraction_" + era + "_" + channel + ".root";
    
//     // 打开文件
//     TFile* f_fraction = new TFile(filename); // 动态加载根文件

//     // 定义权重字典
//     std::map<TString, TH1F*> Weights;

//     // 定义 DR 和 region 向量
//     std::vector<TString> DR = {"QCD", "WJets", "TTbar"};
//     std::vector<TString> region = {"tight_nob", "tight_btag", "loose_nob", "loose_btag"};

//     for (auto& d : DR) {
//         for (auto& r : region) {
//             TString histname = d + "_Fraction_AR" + r;
//             TH1F* h = (TH1F*)f_fraction->Get(histname);

//             // 检查是否成功获取直方图
//             if (!h || h->GetEntries() == 0) {
//                 printf("Warning: Histogram %s not found or is empty in file %s\n", histname.Data(), filename.Data());
//                 continue;
//             }

//             h->SetDirectory(0); // 从文件分离
//             Weights[histname] = h;

//             // 创建一个新的画布
//             TCanvas* c = new TCanvas("c", "c", 800, 600);
            
//             // 在画布上绘制直方图
//             h->Draw();

//             // 保存画布为 PDF 文件
//             TString pdfFilename = histname + ".png";
//             c->SaveAs(pdfFilename);

//             // 释放画布内存
//             delete c;
//         }
//     }

//     // 关闭 ROOT 文件
//     f_fraction->Close();
//     delete f_fraction;
// }




// data_ARtight_mTnobmt_tot
// wjets_ARtight_mTnobmt_tot
// ttbar_ARtight_mTnobmt_tot
// data_ARtight_mTbtagmt_tot
// wjets_ARtight_mTbtagmt_tot
// ttbar_ARtight_mTbtagmt_tot
// data_ARloose_mTnobmt_tot
// wjets_ARloose_mTnobmt_tot
// ttbar_ARloose_mTnobmt_tot
// data_ARloose_mTbtagmt_tot
// wjets_ARloose_mTbtagmt_tot
// ttbar_ARloose_mTbtagmt_tot

