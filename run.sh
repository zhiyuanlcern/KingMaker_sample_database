# Get the username from the environment variable
USER=$(whoami)

# Get the first letter of the username
FIRST_LETTER=${USER:0:1}

# Define the new path
NEW_PATH="root://eosuser.cern.ch///eos/user/$FIRST_LETTER/$USER/CROWN/ntuples/"
sed -i "s|^wlcg_path =.*|wlcg_path = $NEW_PATH|" lawluigi_configs/KingMaker_lxplus_luigi.cfg
sed -i "s|^base:.*|base: $NEW_PATH|" lawluigi_configs/KingMaker_lxplus_law.cfg




channel="all"
replacement="scopes = [\"mt\", \"et\", \"tt\", \"em\"]"
sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"

if grep -q 'scopes = \["mt", "et", "tt", "em"]' lawluigi_configs/KingMaker_lxplus_luigi.cfg ;
then
echo running for ${channel};

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletop${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_singletop${channel}_Version10_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_diboson${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_diboson${channel}_Version10_allsyst.log & 
# sleep 700

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletop${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_singletop${channel}_Version10_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_diboson${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_diboson${channel}_Version10_allsyst.log & 
# sleep 700

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_ttbar${channel}_Version10_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_ttbar${channel}_Version10_allsyst.log & 
# sleep 700


nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautau${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_htautau${channel}_Version10_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautau${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_htautau${channel}_Version10_allsyst.log & 
# sleep 700


nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_dyjets${channel}_Version10_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_dyjets${channel}_Version10_allsyst.log & 
# sleep 700

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjets${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_wjets${channel}_Version10_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjets${channel}_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_wjets${channel}_Version10_allsyst.log & 
# sleep 700

fi


# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt   --tag NanoV12_2022MC_singletop${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt   --tag NanoV12_2022MC_diboson${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt   --tag NanoV12_2022MC_ttbar${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt   --tag NanoV12_2022MC_htautau${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt   --tag NanoV12_2022MC_dyjets${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt   --tag NanoV12_2022MC_wjets${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt   --tag NanoV12_2022EEMC_singletop${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt   --tag NanoV12_2022EEMC_diboson${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt   --tag NanoV12_2022EEMC_ttbar${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt   --tag NanoV12_2022EEMC_htautau${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt   --tag NanoV12_2022EEMC_dyjets${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt   --tag NanoV12_2022EEMC_wjets${channel}_Version10_allsyst >> KingMaker_logs/production_status${channel}_Version10_allsyst.txt & 


# # # sleep 700
# sleep 20
# # for running data
# for channel in  tt  et   mt   em ; # #  
# do 
# replacement="scopes = [\"${channel}\"]"
# sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"
# if grep -q 'scopes = \["'"${channel}"'"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg; 
# then
# echo running for ${channel}; 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --production-tag NanoV12_2022EE${channel}data_Version10 >>NanoV12_2022EE${channel}data_Version10.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --production-tag NanoV12_2022${channel}data_Version10 >>NanoV12_2022${channel}data_Version10.log & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --tag NanoV12_2022EE${channel}data_Version10 >> KingMaker_logs/production_status${channel}_Version10.txt &
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --tag NanoV12_2022${channel}data_Version10 >> KingMaker_logs/production_status${channel}_Version10.txt & 

# # sleep 700
# sleep 20

# fi
# done



# # Get the username from the environment variable
# USER=$(whoami)

# # Get the first letter of the username
# FIRST_LETTER=${USER:0:1}

# # Define the new path
# NEW_PATH="root://eosuser.cern.ch///eos/user/$FIRST_LETTER/$USER/CROWN/ntuples/"
# sed -i "s|^wlcg_path =.*|wlcg_path = $NEW_PATH|" lawluigi_configs/KingMaker_lxplus_luigi.cfg
# sed -i "s|^base:.*|base: $NEW_PATH|" lawluigi_configs/KingMaker_lxplus_law.cfg




# channel="all"
# replacement="scopes = [\"mt\", \"et\", \"tt\"]"
# sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"

# if grep -q 'scopes = \["mt", "et", "tt"]' lawluigi_configs/KingMaker_lxplus_luigi.cfg ;
# then
# echo running for ${channel};
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_dibosonall_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_dibosonall_Version10_allsyst.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_dibosonall_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_dibosonall_Version10_allsyst.log & 
 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletopall_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_singletopall_Version10_allsyst.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletopall_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_singletopall_Version10_allsyst.log & 

# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbarall_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_ttbarall_Version10_allsyst.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbarall_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_ttbarall_Version10_allsyst.log & 


# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautauall_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_htautauall_Version10_allsyst.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautauall_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_htautauall_Version10_allsyst.log & 


# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjetsall_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_dyjetsall_Version10_allsyst.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjetsall_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_dyjetsall_Version10_allsyst.log & 

# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjetsall_Version10_allsyst >> KingMaker_logs/NanoV12_2022EEMC_wjetsall_Version10_allsyst.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjetsall_Version10_allsyst >> KingMaker_logs/NanoV12_2022MC_wjetsall_Version10_allsyst.log & 




# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets_mm.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets_mm${channel}_Version10 >> KingMaker_logs/NanoV12_2022EEMC_dyjets_mm${channel}_Version10.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets_mm.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets_mm${channel}_Version10 >> KingMaker_logs/NanoV12_2022MC_dyjets_mm${channel}_Version10.log & 


# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar_mm${channel}_Version10 >> KingMaker_logs/NanoV12_2022MC_ttbar_mm${channel}_Version10.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar_mm${channel}_Version10 >> KingMaker_logs/NanoV12_2022EEMC_ttbar_mm${channel}_Version10.log & 
# # sleep 700


# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEmtdata.txt --production-tag NanoV12_2022EE_mm_data_Version10 >>NanoV12_2022EE_mm_data_Version10 & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022mtdata.txt --production-tag NanoV12_2022_mm_data_Version10 >>NanoV12_2022_mm_data_Version10 & 




 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_diboson.txt --workers 1 --production-tag 2023MC_diboson &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_dyjets.txt --workers 1 --production-tag 2023MC_dyjets &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_wjets.txt --workers 1 --production-tag 2023MC_wjets &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_ttbar.txt --workers 1 --production-tag 2023MC_ttbar &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_ggh_htautau.txt --workers 1 --production-tag 2023MC_ggh_htautau &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_vbf_htautau.txt --workers 1 --production-tag 2023MC_vbf_htautau &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_singletop.txt --workers 1 --production-tag 2023MC_singletop &
 
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_mt.txt --workers 1 --production-tag 2023data_mt &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_et.txt --workers 1 --production-tag 2023data_et &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_tt.txt --workers 1 --production-tag 2023data_tt &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_em.txt --workers 1 --production-tag 2023data_em &









python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_diboson.txt --tag 2023MC_diboson >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_dyjets.txt --tag 2023MC_dyjets >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_ggh_htautau.txt --tag 2023MC_ggh_htautau >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_vbf_htautau.txt --tag 2023MC_vbf_htautau >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_wjets.txt --tag 2023MC_wjets >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_singletop.txt --tag 2023MC_singletop >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_ttbar.txt --tag 2023MC_ttbar >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023data_mt.txt --tag 2023data_mt >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023data_et.txt --tag 2023data_et >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023data_tt.txt --tag 2023data_tt >> KingMaker_logs/2023log.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023data_em.txt --tag 2023data_em >> KingMaker_logs/2023log.txt &







#  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_mt.txt --workers 1 --production-tag 2023data_mt_VVVLooseVsJet &
#  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_et.txt --workers 1 --production-tag 2023data_et_VVVLooseVsJet &
#  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_tt.txt --workers 1 --production-tag 2023data_tt_VVVLooseVsJet &
#  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_dyjets.txt --workers 1 --production-tag 2023MC_dyjets_VVVLooseVsJet &
#  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_wjets.txt --workers 1 --production-tag 2023MC_wjets_VVVLooseVsJet &
#  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_ttbar.txt --workers 1 --production-tag 2023MC_ttbar_VVVLooseVsJet &

#  python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_dyjets.txt --tag 2023MC_dyjets_VVVLooseVsJet



# law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_dyjets.txt  --workers 1 --production-tag 2023MC_dyjets_mm${channel}_Version10 & 
# law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_ttbar.txt  --workers 1 --production-tag 2023MC_ttbar_mm${channel}_Version10  & 
# law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023data_mt.txt  --workers 1 --production-tag 2023_mm_data_Version10 & 


python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022MC_dyjets.txt --tag 2022MC_LO_dyjets_allsyst

law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_singletop.txt  --workers 1 --production-tag 2023MC_ttbar_mm${channel}_Version10  & 
law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_singletop.txt  --workers 1 --production-tag 2023MC_singletop_mm${channel}_Version10  


law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022MC_dyjets.txt --workers 1 --production-tag 2022MC_dyjets_VVVLooseVsJet

 python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2022MC_dyjets.txt --tag 2022MC_dyjets_VVVLooseVsJet

 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022MC_dyjets.txt --workers 1 --production-tag 2022MC_LO_dyjets_allsyst &


law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_dyjets.txt --workers 1 --production-tag 2023MC_dyjets &




law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022data_et_skim.txt --workers 1 --production-tag 2022data_et_skim_run &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist    sample_database/2022data_et_skim.txt   --tag 2022data_et_skim_run 
law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022data_et.txt --workers 1 --production-tag 2022data_et_noskim_run &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist    sample_database/2022data_et.txt   --tag 2022data_et_noskim_run 

 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022MC_dyjets_2022postEE.txt --workers 1 --production-tag 2022MC_LO_dyjets_Tight_vsEle_TauES &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist    sample_database/2022MC_dyjets_2022postEE.txt  --tag 2022MC_LO_dyjets_Tight_vsEle_TauES


law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023MC_dyjets.txt --workers 1 --production-tag 2023MC_dyjets_fixTauEs &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist  sample_database/2023MC_dyjets.txt --tag 2023MC_dyjets_fixTauEs


law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022MC_dyjets.txt --workers 1 --production-tag 2022MC_LO_dyjets_allsyst_fix_TauES &

python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022MC_dyjets.txt  --tag 2022MC_LO_dyjets_allsyst_fix_TauES &

law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022MC_dyjets.txt  --production-tag 2022MC_LO_dyjets_nominal_fix_TauES_VVVLoose &
law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_dyjets.txt --production-tag 2023MC_LO_dyjets_nominal_fix_TauES_VVVLoose &


python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022MC_dyjets.txt  --tag 2022MC_LO_dyjets_nominal_fix_TauES_VVVLoose &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2023MC_dyjets.txt  --tag 2023MC_LO_dyjets_nominal_fix_TauES_VVVLoose &



 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022data.txt --production-tag 2022data_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022MC_ttbar.txt --production-tag 2022MC_ttbar_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022MC_wjets.txt  --production-tag 2022MC_wjets_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022MC_dyjets.txt --production-tag 2022MC_dyjets_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022MC_diboson.txt --production-tag 2022MC_diboson_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022MC_singletop.txt --production-tag 2022MC_singletop_looseIso &


 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023data_em.txt --production-tag 2023data_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_ttbar.txt --production-tag 2023MC_ttbar_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_wjets.txt  --production-tag 2023MC_wjets_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_dyjets.txt --production-tag 2023MC_dyjets_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_diboson.txt --production-tag 2023MC_diboson_looseIso &
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2023MC_singletop.txt --production-tag 2023MC_singletop_looseIso &
 

 python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022data.txt --tag 2022data_looseIso
 law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022data.txt --production-tag 2022data_looseIso_2022EE &        
  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022data.txt --production-tag 2022data_looseIso_2022EE_mm & 

  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022data_all.txt    --production-tag 2022data_looseIso_fix_jetveto

  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022data_test.txt    --production-tag 2022data_looseIso_fix_jetveto_test2

  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022data_all.txt    --production-tag 2022data_looseIso_fix_jetveto_test2


  python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022data_all.txt  --tag 2022data_looseIso_fix_jetveto_test2 & 
  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2023data_all.txt    --production-tag 2023data_looseIso_fix_jetveto_test2 &

  law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022EEdata_all.txt    --production-tag 2022data_looseIso_fix_jetveto_test3 &

  python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2023data_all.txt  --tag 2023data_looseIso_fix_jetveto_test2 &
  python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022EEdata_all.txt  --tag 2022data_looseIso_fix_jetveto_test3 &
    

     law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022EEdata_et.txt    --production-tag 2022data_looseIso_fix_jetveto_test3_et &
    
    python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022EEdata_et.txt  --tag 2022data_looseIso_fix_jetveto_test3_et &
    python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022_23data_tt.txt   --tag 2022_2023data_looseIso_fix_jetveto_test3_tt &

    law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022_23data_tt.txt    --production-tag 2022_2023data_looseIso_fix_jetveto_test3_tt &

    law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list  sample_database/2022_23data_tt.txt    --production-tag 2022_2023data_looseIso_fix_jetveto_test4_tt &

    python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022_23data_tt.txt   --tag 2022_2023data_looseIso_fix_jetveto_test4_tt &

    law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/2022_2023data_mt.txt  --workers 1 --production-tag 2022_2023data_looseIso_fix_jetveto_mm & 
    python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/2022_2023data_mt.txt   --tag 2022_2023data_looseIso_fix_jetveto_mm &