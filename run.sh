#!/bin/bash
#for i in 1 2 3 4 5 ; do law run ProduceSamples --local-scheduler False --analysis tau  --config config_vvvloose_tau  --sample-list samples.zhiyuan.split${i}.txt --workers 1 --production-tag fixbtag_nprebtagjets_newgensum_split${i} &    done
# law run ProduceSamples --local-scheduler False --analysis tau  --config config_vvvloose_tau  --sample-list samples.zhiyuan.ttbar.txt --workers 1 --production-tag em_ttbar &  
# law run ProduceSamples --local-scheduler False --analysis tau  --config config_vvvloose_tau  --sample-list samples.zhiyuan.BSM2.txt --workers 1 --production-tag mt_BSM_2023_02_22 &  
# 
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.tt.cross_checks.txt --workers 1 --production-tag tt_cross_checks_run2 &  
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.tt.cross_checks_run2.txt --workers 1 --production-tag tt_cross_checks_run3 &  


# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split1.txt --workers 1 --production-tag mt_cross_checks_split1 >> mt_cross_checks_split1.txt &  
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split2.txt --workers 1 --production-tag mt_cross_checks_split2 >> mt_cross_checks_split2.txt &  
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split3.txt --workers 1 --production-tag mt_cross_checks_split3 >> mt_cross_checks_split3.txt &  
# law run ProduceSamples --local-scheduler False --analysis tau  --config config_vvvloose_tau  --sample-list samples.zhiyuan.BSM.txt --workers 1 --production-tag mt_BSM_2023_03_06_fix_sumweight >> mt_BSM_2023_03_06_fix_sumweight.txt &  

# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split1.txt --workers 1 --production-tag fastmtt_split1 >> fastmtt_split1.log &  
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split2.txt --workers 1 --production-tag fastmtt_split2 >> fastmtt_split2.log &  
##law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split3.txt --workers 1 --production-tag fastmtt_split3 >> fastmtt_split3.log & 
#law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split4.txt --workers 1 --production-tag fastmtt_split4 >> fastmtt_split4.log & 
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split5.txt --workers 1 --production-tag fastmtt_split5 >> fastmtt_split5.log & 
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split6.txt --workers 1 --production-tag fastmtt_split2 >> fastmtt_split6.log & 
# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split7.txt --workers 1 --production-tag fastmtt_split2 >> fastmtt_split7.log & 

# law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split8.txt --workers 1 --production-tag fastmtt_split5 >> fastmtt_split8.log & 
#nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split3.txt --workers 1 --production-tag etau_split3 >> etau_split3.log & 
#nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split4.txt --workers 1 --production-tag etau_split4 >> etau_split4.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split2.txt --workers 1 --production-tag etau_split2 >> etau_split2.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.et.split1.txt --workers 1 --production-tag etau_split1 >> etau_split1.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.et.split1_missing.txt --workers 1 --production-tag etau_split1_missing >> etau_split1_missing.log & 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.et.split1_missing_missing.txt --workers 1 --production-tag etau_split1_missing_missing >> etau_split1_missing_missing.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split5.txt --workers 1 --production-tag etau_split5 >> etau_split5.log & 

#python3.9 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist samples.zhiyuan.split1.txt  --tag fastmtt_split1 
#python3.9 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist samples.zhiyuan.split2.txt  --tag fastmtt_split2
# python3.9 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist samples.zhiyuan.split2.txt  --tag etau_split2


# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list samples.zhiyuan.split5.txt --workers 1 --production-tag etau_split5 >> etau_split5.log & 
 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list 16singletop-ttbar.txt  --workers 1 --production-tag 16singletop-ttbar >> 16singletop-ttbar.log &
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list 16embedding.txt  --workers 1 --production-tag 16embedding >> 16embedding.log &

#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list 17embedding.txt  --workers 1 --production-tag 17embedding >> 17embedding.log &
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list 16data.txt  --workers 1 --production-tag 16data >> 16data.log &
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list 16diboson-dyjets-wjets-electroweakboson.txt  --workers 1 --production-tag 16diboson-dyjets-wjets-electroweakboson >> 16diboson-dyjets-wjets-electroweakboson.log &
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config  --sample-list 16ggh_htautau-ggh_hbb-vbf_htautau-vbf_hbb-rem_htautau-rem_hbb.txt  --workers 1 --production-tag 16ggh_htautau-ggh_hbb-vbf_htautau-vbf_hbb-rem_htautau-rem_hbb >> 16ggh_htautau-ggh_hbb-vbf_htautau-vbf_hbb-rem_htautau-rem_hbb.log &
 

# /afs/cern.ch/user/z/zhiyuanl/KingMaker/build/16singletop-ttbar/CROWN_tau_config
# ./config_ttbar_2016postVFP 089E6E3A-DFD1-7148-BD6F-F611D22A1B62.root
# /afs/cern.ch/user/z/zhiyuanl/KingMaker/data/jobs/tmpu758uc1r/stdall_9To10.txt
# cmake .. -DANALYSIS=tau  -DCONFIG=config -DSAMPLES=ttbar -DERAS=2016postVFP -DSCOPES=et,mt,tt,em -DTHREADS=20 -DOPTIMIZED=false  -DSHIFTS=none

# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 16data.txt  --tag 16data & done
# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 16singletop-ttbar.txt --tag 16singletop-ttbar & done

# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 16diboson-dyjets-wjets-electroweakboson.txt --tag 16diboson-dyjets-wjets-electroweakboson &
# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 16ggh_htautau-ggh_hbb-vbf_htautau-vbf_hbb-rem_htautau-rem_hbb.txt --tag 16ggh_htautau-ggh_hbb-vbf_htautau-vbf_hbb-rem_htautau-rem_hbb &
# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 16embedding.txt --tag 16embedding &


# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list signal_missing.txt  --workers 1 --production-tag signal_missing-fixed-test >> signal_missing-fixed-test.log &
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list signal_missing_ext1.txt  --workers 1 --production-tag signal_missing-fixed-test >> signal_missing-fixed-test.log &
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list 2022data.txt  --workers 1 --production-tag 2022data >> 2022datatest.log &
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list 2022MC_dyjets.txt  --workers 1 --production-tag 2022MC_dyjets >> 2022MC_dyjets.log &
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list 2022MC_wjets.txt  --workers 1 --production-tag 2022MC_wjets >> 2022MC_wjets.log &

# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist signal_missing.txt --tag signal_missing-fixed-test
# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 2022data.txt --tag 2022data
# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 2022MC_dyjets.txt --tag 2022MC_dyjets
# python3 scripts/ProductionStatus.py --analysis tau --config config --samplelist 2022MC_wjets.txt --tag 2022MC_wjets




#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wg.txt  --workers 1 --production-tag NanoV12_2022MC_wg >> NanoV12_2022MC_wg.log & 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wg.txt  --workers 1 --production-tag NanoV12_2022EEMC_wg >> NanoV12_2022EEMC_wg.log & 

#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets >> NanoV12_2022MC_dyjets.log & 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_diboson >> NanoV12_2022MC_diboson.log & 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar >> NanoV12_2022MC_ttbar.log & 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjets >> NanoV12_2022MC_wjets.log & 
#   nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletop >> NanoV12_2022MC_singletop.log & 
#   nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_hbb.txt  --workers 1 --production-tag NanoV12_2022MC_hbb >> NanoV12_2022MC_hbb.log & 
#   nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautau >> NanoV12_2022MC_htautau.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022data.txt  --workers 1 --production-tag NanoV12_2022data >> NanoV12_2022data.log & 



  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets >> NanoV12_2022EEMC_dyjets.log & 
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_diboson >> NanoV12_2022EEMC_diboson.log & 
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar >> NanoV12_2022EEMC_ttbar.log & 
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjets >> NanoV12_2022EEMC_wjets.log & 
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletop >> NanoV12_2022EEMC_singletop.log & 
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_hbb.txt  --workers 1 --production-tag NanoV12_2022EEMC_hbb >> NanoV12_2022EEMC_hbb.log & 
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautau >> NanoV12_2022EEMC_htautau.log & 
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEdata.txt  --workers 1 --production-tag NanoV12_2022EEdata >> NanoV12_2022EEdata.log & 

  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEdata_et.txt  --workers 1 --production-tag 2022EEdata_et > 2022EEdata_et.log & 
  
  # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list Run3_missingMC.txt  --workers 1 --production-tag Run3_missingMC > Run3_missingMC.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list Run3_missing.txt  --workers 1 --production-tag test >> Run3_missing.log & 





# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_dyjets.txt  --tag NanoV12_2022MC_dyjets  & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_diboson.txt  --tag NanoV12_2022MC_diboson  & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_ttbar.txt  --tag NanoV12_2022MC_ttbar  & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_wjets.txt  --tag NanoV12_2022MC_wjets  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_singletop.txt  --tag NanoV12_2022MC_singletop  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_hbb.txt  --tag NanoV12_2022MC_hbb  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_htautau.txt  --tag NanoV12_2022MC_htautau  & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022data.txt  --tag NanoV12_2022data  & 

#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --tag NanoV12_2022EEMC_dyjets  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --tag NanoV12_2022EEMC_diboson  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --tag NanoV12_2022EEMC_ttbar  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --tag NanoV12_2022EEMC_wjets  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --tag NanoV12_2022EEMC_singletop  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEMC_hbb.txt  --tag NanoV12_2022EEMC_hbb  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --tag NanoV12_2022EEMC_htautau  & 
#  python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022EEdata.txt  --tag NanoV12_2022EEdata  & 









# sed -i 's/scopes = \["em"\]/scopes = ["et"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022etdata.txt --production-tag NanoV12_2022etdata >>NanoV12_2022etdata.log &
# sed -i 's/scopes = \["et"\]/scopes = ["mt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022mtdata.txt --production-tag NanoV12_2022mtdata >>NanoV12_2022mtdata.log &
# sed -i 's/scopes = \["mt"\]/scopes = ["tt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022ttdata.txt --production-tag NanoV12_2022ttdata >>NanoV12_2022ttdata.log &
# sed -i 's/scopes = \["tt"\]/scopes = ["em"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022emdata.txt --production-tag NanoV12_2022emdata >>NanoV12_2022emdata.log &


# sed -i 's/scopes = \["em"\]/scopes = ["et"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEetdata.txt --production-tag NanoV12_2022EEetdata >>NanoV12_2022EEetdata.log &
# sed -i 's/scopes = \["et"\]/scopes = ["mt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEmtdata.txt --production-tag NanoV12_2022EEmtdata >>NanoV12_2022EEmtdata.log &
# sed -i 's/scopes = \["mt"\]/scopes = ["tt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEttdata.txt --production-tag NanoV12_2022EEttdata >>NanoV12_2022EEttdata.log &
# sed -i 's/scopes = \["tt"\]/scopes = ["em"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEemdata.txt --production-tag NanoV12_2022EEemdata >>NanoV12_2022EEemdata.log &



# echo running for et; sed -i 's/scopes = \["em"\]/scopes = ["et"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["et"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022etdata.txt --production-tag NanoV12_2022etdata >>NanoV12_2022etdata.log & 
# sleep 60 ;
# echo running for mt; sed -i 's/scopes = \["et"\]/scopes = ["mt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["mt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022mtdata.txt --production-tag NanoV12_2022mtdata >>NanoV12_2022mtdata.log &
# sleep 60 ;
# echo running for tt; sed -i 's/scopes = \["mt"\]/scopes = ["tt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["tt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022ttdata.txt --production-tag NanoV12_2022ttdata >>NanoV12_2022ttdata.log &
# sleep 60;
# echo running for em; sed -i 's/scopes = \["tt"\]/scopes = ["em"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["em"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022emdata.txt --production-tag NanoV12_2022emdata >>NanoV12_2022emdata.log &



first_chan='em'
# for channel in  'mt' 'et' ;
# for channel in 'et'  ;
for channel in  'em' 'tt' ;

do 
echo running for ${channel}; 
sed -i  's/scopes = \["'${first_chan}'"\]/scopes = ["'${channel}'"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  

if grep -q 'scopes = \["'"${channel}"'"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg; 
then

# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --production-tag NanoV12_2022EE${channel}data >>NanoV12_2022EE${channel}data.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --production-tag NanoV12_2022${channel}data >>NanoV12_2022${channel}data.log & 
# sleep 200
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets${channel} >> NanoV12_2022MC_dyjets${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjets${channel} >> NanoV12_2022MC_wjets${channel}.log & 
sleep 600
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletop${channel} >> NanoV12_2022MC_singletop${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_diboson${channel} >> NanoV12_2022MC_diboson${channel}.log & 
sleep 3000
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar${channel} >> NanoV12_2022MC_ttbar${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautau${channel} >> NanoV12_2022MC_htautau${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_hbb.txt  --workers 1 --production-tag NanoV12_2022MC_hbb${channel} >> NanoV12_2022MC_hbb${channel}.log & 
sleep 3000
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets${channel} >> NanoV12_2022EEMC_dyjets${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjets${channel} >> NanoV12_2022EEMC_wjets${channel}.log & 
sleep 3000
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletop${channel} >> NanoV12_2022EEMC_singletop${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_diboson${channel} >> NanoV12_2022EEMC_diboson${channel}.log & 
sleep 3000
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar${channel} >> NanoV12_2022EEMC_ttbar${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautau${channel} >> NanoV12_2022EEMC_htautau${channel}.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_hbb.txt  --workers 1 --production-tag NanoV12_2022EEMC_hbb${channel} >> NanoV12_2022EEMC_hbb${channel}.log & 
sleep 3000


# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist Htautau_input_list/NanoV12_2022MC_dyjets.txt  --tag 

# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist Htautau_input_list/NanoV12_2022EE${channel}data.txt --tag NanoV12_2022EE${channel}data
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist Htautau_input_list/NanoV12_2022${channel}data.txt --tag NanoV12_2022${channel}data

# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist Htautau_input_list/NanoV12_2022MC_singletop.txt   --tag NanoV12_2022MC_singletop${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist Htautau_input_list/NanoV12_2022MC_diboson.txt   --tag NanoV12_2022MC_diboson${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist Htautau_input_list/NanoV12_2022MC_ttbar.txt   --tag NanoV12_2022MC_ttbar${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist Htautau_input_list/NanoV12_2022MC_htautau.txt   --tag NanoV12_2022MC_htautau${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist Htautau_input_list/NanoV12_2022MC_hbb.txt   --tag NanoV12_2022MC_hbb${channel}



# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  Htautau_input_list/NanoV12_2022EEMC_singletop.txt   --tag NanoV12_2022EEMC_singletop${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  Htautau_input_list/NanoV12_2022EEMC_diboson.txt   --tag NanoV12_2022EEMC_diboson${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  Htautau_input_list/NanoV12_2022EEMC_ttbar.txt   --tag NanoV12_2022EEMC_ttbar${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  Htautau_input_list/NanoV12_2022EEMC_htautau.txt   --tag NanoV12_2022EEMC_htautau${channel}
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  Htautau_input_list/NanoV12_2022EEMC_hbb.txt   --tag NanoV12_2022EEMC_hbb${channel}
fi
sleep 10 ;
first_chan=${channel}
done




# first_chan='tt'
# for channel in 'em' ;
# # for channel in 'et'  ;

# do 
# echo running for ${channel}; 
# sed -i  's/scopes = \["'${first_chan}'"\]/scopes = ["'${channel}'"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  

# if grep -q 'scopes = \["'"${channel}"'"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg; 
# then

# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --production-tag NanoV12_2022EE${channel}data >>NanoV12_2022EE${channel}data.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --production-tag NanoV12_2022${channel}data >>NanoV12_2022${channel}data.log & 
# # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --production-tag NanoV12_2022EE${channel}data >>NanoV12_2022EE${channel}data.log & 
# # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --production-tag NanoV12_2022${channel}data >>NanoV12_2022${channel}data.log & 
# # sleep 100
# sleep 10 ;
# fi
# first_chan=${channel}
# done



# echo running for mt; sed -i 's/scopes = \["et"\]/scopes = ["mt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["mt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEmtdata.txt --production-tag NanoV12_2022EEmtdata >>NanoV12_2022EEmtdata.log &
# sleep 60 ;
# echo running for tt; sed -i 's/scopes = \["mt"\]/scopes = ["tt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["tt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEttdata.txt --production-tag NanoV12_2022EEttdata >>NanoV12_2022EEttdata.log &
# sleep 60;
# echo running for em; sed -i 's/scopes = \["tt"\]/scopes = ["em"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["em"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEemdata.txt --production-tag NanoV12_2022EEemdata >>NanoV12_2022EEemdata.log &




#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets >> NanoV12_2022MC_dyjets.log & 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_diboson >> NanoV12_2022MC_diboson.log & 
# #  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar >> NanoV12_2022MC_ttbar.log & 
#  nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjets >> NanoV12_2022MC_wjets.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletop >> NanoV12_2022MC_singletop.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_hbb.txt  --workers 1 --production-tag NanoV12_2022MC_hbb >> NanoV12_2022MC_hbb.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautau >> NanoV12_2022MC_htautau.log & 
# # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022data.txt  --workers 1 --production-tag NanoV12_2022data >> NanoV12_2022data.log & 



#   nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets >> NanoV12_2022EEMC_dyjets.log & 
#   nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_diboson >> NanoV12_2022EEMC_diboson.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar >> NanoV12_2022EEMC_ttbar.log & 
#   nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjets >> NanoV12_2022EEMC_wjets.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletop >> NanoV12_2022EEMC_singletop.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_hbb.txt  --workers 1 --production-tag NanoV12_2022EEMC_hbb >> NanoV12_2022EEMC_hbb.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautau >> NanoV12_2022EEMC_htautau.log & 
#   # nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEdata.txt  --workers 1 --production-tag NanoV12_2022EEdata >> NanoV12_2022EEdata.log & 


# echo running for et; sed -i 's/scopes = \["em"\]/scopes = ["et"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ; grep -q 'scopes = \["et"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/missing__dyjets.txt --production-tag missing__dyjets_et >>missing__dyjets._etlog & 
# sleep 60 ;
# echo running for mt; sed -i 's/scopes = \["et"\]/scopes = ["mt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["mt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/missing__dyjets.txt --production-tag missing__dyjets_mt >>missing__dyjets_mt.log &
# sleep 60 ;
# echo running for tt; sed -i 's/scopes = \["mt"\]/scopes = ["tt"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["tt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/missing__dyjets.txt --production-tag missing__dyjets_tt >>missing__dyjets_tt.log &
# sleep 60;
# echo running for em; sed -i 's/scopes = \["tt"\]/scopes = ["em"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  grep -q 'scopes = \["em"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg && nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/missing__dyjets.txt --production-tag missing__dyjets_em >>missing__dyjets_em.log &


# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list Run3_missing.txt  --workers 1 --production-tag test >> Run3_missing.log & 


