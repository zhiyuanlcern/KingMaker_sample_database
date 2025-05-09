import ROOT

# 定义文件和图像的路径
root_file_path = 'Fraction_new.root'
output_image_path = 'ARLoose_mTbtagmt_tot.png'

# 打开 ROOT 文件
root_file = ROOT.TFile(root_file_path, 'READ')

# 获取直方图
hist_data = root_file.Get('data_ARloose_mTbtagmt_tot')
hist_wjets = root_file.Get('wjets_ARloose_mTbtagmt_tot')
hist_ttbar = root_file.Get('ttbar_ARloose_mTbtagmt_tot')

# 检查是否成功加载直方图
if not hist_data or not hist_wjets or not hist_ttbar:
    print("Error: One or more histograms not found.")
    root_file.Close()
    exit()

# 创建画布和TPad以设置背景透明度
canvas = ROOT.TCanvas('canvas', 'Canvas', 800, 600)
pad = ROOT.TPad('pad', 'pad', 0, 0, 1, 1)
pad.SetFillColorAlpha(ROOT.kWhite, 0.9)  # 设置背景色为白色，透明度20%
pad.Draw()
pad.cd()

# 绘制直方图
hist_data.SetLineColor(ROOT.kBlue)
hist_data.SetFillColor(ROOT.kBlue)
hist_data.SetFillStyle(0)  # Solid fill, no transparency
hist_data.SetLineWidth(3)
hist_data.SetTitle('ARLoose_btag')
hist_data.GetXaxis().SetTitle('$\\text{m}_\\text{T}^{\\text{tot}}$\\text{(Gev)}')
hist_data.GetYaxis().SetTitle('Fraction')
hist_data.GetYaxis().SetRangeUser(0, 1.2)
hist_data.Draw('hist')

hist_wjets.SetLineColor(ROOT.kRed)
hist_wjets.SetLineWidth(3)
hist_wjets.SetFillColor(ROOT.kRed)
hist_wjets.SetFillStyle(0)  # Solid fill, no transparency
hist_wjets.Draw('hist same')

hist_ttbar.SetLineColor(ROOT.kYellow)
hist_ttbar.SetFillColor(ROOT.kYellow)
hist_ttbar.SetLineWidth(3)
hist_ttbar.SetFillStyle(0)  # Solid fill, no transparency
hist_ttbar.Draw('hist same')

# 添加图例
legend = ROOT.TLegend(0.79, 0.79, 0.89, 0.89)
legend.SetFillColor(0)  # 使图例背景透明
legend.SetBorderSize(0)  # 去掉图例边框
legend.SetBorderSize(0)  # 去掉图例边框
legend.SetTextSize(0.033)  # 0.05 是字体大小的示例值，可以根据需要调整
legend.AddEntry(hist_data, 'Data', 'l')  # 'l' 表示线条
legend.AddEntry(hist_wjets, 'Wjets', 'l')
legend.AddEntry(hist_ttbar, 'TTbar', 'l')
legend.Draw()

# 保存图像到文件
canvas.SaveAs(output_image_path)

# 关闭 ROOT 文件
root_file.Close()

print(f"Plot saved to {output_image_path}")
