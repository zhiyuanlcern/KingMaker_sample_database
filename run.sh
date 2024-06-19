
channel="all"
sed -i  's/scopes = \["mt"\]/scopes = ["mt", "et", "tt"]/' lawluigi_configs/KingMaker_lxplus_luigi.cfg

if grep -q 'scopes = \["mt", "et", "tt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg ;
then
echo running for ${channel}; 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletop${channel}_run6_allsyst >> NanoV12_2022MC_singletop${channel}_run6_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_diboson${channel}_run6_allsyst >> NanoV12_2022MC_diboson${channel}_run6_allsyst.log & 

sleep 300
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletop${channel}_run6_allsyst >> NanoV12_2022EEMC_singletop${channel}_run6_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_diboson${channel}_run6_allsyst >> NanoV12_2022EEMC_diboson${channel}_run6_allsyst.log & 


sleep 300
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar${channel}_run6_allsyst >> NanoV12_2022MC_ttbar${channel}_run6_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar${channel}_run6_allsyst >> NanoV12_2022EEMC_ttbar${channel}_run6_allsyst.log & 

sleep 300
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautau${channel}_run6_allsyst >> NanoV12_2022MC_htautau${channel}_run6_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautau${channel}_run6_allsyst >> NanoV12_2022EEMC_htautau${channel}_run6_allsyst.log & 

sleep 300
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_hbb.txt  --workers 1 --production-tag NanoV12_2022MC_hbb${channel}_run6_allsyst >> NanoV12_2022MC_hbb${channel}_run6_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_hbb.txt  --workers 1 --production-tag NanoV12_2022EEMC_hbb${channel}_run6_allsyst >> NanoV12_2022EEMC_hbb${channel}_run6_allsyst.log & 

sleep 300
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets${channel}_run6_allsyst >> NanoV12_2022EEMC_dyjets${channel}_run6_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets${channel}_run6_allsyst >> NanoV12_2022MC_dyjets${channel}_run6_allsyst.log & 
sleep 300
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjets${channel}_run6_allsyst >> NanoV12_2022EEMC_wjets${channel}_run6_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjets${channel}_run6_allsyst >> NanoV12_2022MC_wjets${channel}_run6_allsyst.log & 
sleep 300
fi


# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt   --tag NanoV12_2022MC_singletop${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt   --tag NanoV12_2022MC_diboson${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt   --tag NanoV12_2022MC_ttbar${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt   --tag NanoV12_2022MC_htautau${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_hbb.txt   --tag NanoV12_2022MC_hbb${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt   --tag NanoV12_2022MC_dyjets${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt   --tag NanoV12_2022MC_wjets${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt   --tag NanoV12_2022EEMC_singletop${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt   --tag NanoV12_2022EEMC_diboson${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt   --tag NanoV12_2022EEMC_ttbar${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt   --tag NanoV12_2022EEMC_htautau${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_hbb.txt   --tag NanoV12_2022EEMC_hbb${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt   --tag NanoV12_2022EEMC_dyjets${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt   --tag NanoV12_2022EEMC_wjets${channel}_run6_allsyst >> production_status${channel}_run6_allsyst.txt & 



# sed -i  's/scopes = \["mt", "et", "tt"]/scopes = ["mt"\]/' lawluigi_configs/KingMaker_lxplus_luigi.cfg
# first_chan='mt'

# for channel in   'et' 'tt' 'mt'  ;
# # for channel in  'tt'    ;
# do 

# sed -i  's/scopes = \["'${first_chan}'"\]/scopes = ["'${channel}'"]/g' lawluigi_configs/KingMaker_lxplus_luigi.cfg  ;  

# if grep -q 'scopes = \["'"${channel}"'"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg; 
# then
# echo running for ${channel}; 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --production-tag NanoV12_2022EE${channel}data_run4_rerun >>NanoV12_2022EE${channel}data_run4_rerun.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --production-tag NanoV12_2022${channel}data_run4_rerun >>NanoV12_2022${channel}data_run4_rerun.log & 
# # python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --tag NanoV12_2022EE${channel}data_run4_rerun >> production_status${channel}_run4_rerun.txt &
# # python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --tag NanoV12_2022${channel}data_run4_rerun >> production_status${channel}_run4_rerun.txt & 

# # sleep 4

# fi


# first_chan=${channel}
# done