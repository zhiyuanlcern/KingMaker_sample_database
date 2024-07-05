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

if grep -q 'scopes = \["mt", "et", "tt", "em"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg ;
then
echo running for ${channel}; 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletop${channel}_Version9_allsyst >> NanoV12_2022MC_singletop${channel}_Version9_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_diboson${channel}_Version9_allsyst >> NanoV12_2022MC_diboson${channel}_Version9_allsyst.log & 
sleep 600

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletop${channel}_Version9_allsyst >> NanoV12_2022EEMC_singletop${channel}_Version9_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_diboson${channel}_Version9_allsyst >> NanoV12_2022EEMC_diboson${channel}_Version9_allsyst.log & 
sleep 600

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar${channel}_Version9_allsyst >> NanoV12_2022MC_ttbar${channel}_Version9_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar${channel}_Version9_allsyst >> NanoV12_2022EEMC_ttbar${channel}_Version9_allsyst.log & 
sleep 600


nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautau${channel}_Version9_allsyst >> NanoV12_2022MC_htautau${channel}_Version9_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautau${channel}_Version9_allsyst >> NanoV12_2022EEMC_htautau${channel}_Version9_allsyst.log & 
sleep 600


nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets${channel}_Version9_allsyst_rerun_rerun >> NanoV12_2022EEMC_dyjets${channel}_Version9_allsyst_rerun_rerun.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets${channel}_Version9_allsyst_rerun_rerun >> NanoV12_2022MC_dyjets${channel}_Version9_allsyst_rerun_rerun.log & 
sleep 600

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjets${channel}_Version9_allsyst >> NanoV12_2022EEMC_wjets${channel}_Version9_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjets${channel}_Version9_allsyst >> NanoV12_2022MC_wjets${channel}_Version9_allsyst.log & 
sleep 600

fi


# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt   --tag NanoV12_2022MC_singletop${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt   --tag NanoV12_2022MC_diboson${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt   --tag NanoV12_2022MC_ttbar${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt   --tag NanoV12_2022MC_htautau${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_hbb.txt   --tag NanoV12_2022MC_hbb${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt   --tag NanoV12_2022MC_dyjets${channel}_Version9_allsyst_rerun_rerun >> production_status${channel}_Version9_allsyst_rerun_rerun.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt   --tag NanoV12_2022MC_wjets${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt   --tag NanoV12_2022EEMC_singletop${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt   --tag NanoV12_2022EEMC_diboson${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt   --tag NanoV12_2022EEMC_ttbar${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt   --tag NanoV12_2022EEMC_htautau${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_hbb.txt   --tag NanoV12_2022EEMC_hbb${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt   --tag NanoV12_2022EEMC_dyjets${channel}_Version9_allsyst_rerun_rerun >> production_status${channel}_Version9_allsyst_rerun_rerun.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt   --tag NanoV12_2022EEMC_wjets${channel}_Version9_allsyst >> production_status${channel}_Version9_allsyst.txt & 


# sleep 600
# for running data
for channel in  et tt mt em;
do 
replacement="scopes = [\"${channel}\"]"
sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"
if grep -q 'scopes = \["'"${channel}"'"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg; 
then
echo running for ${channel}; 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --production-tag NanoV12_2022EE${channel}data_Version9 >>NanoV12_2022EE${channel}data_Version9.log & 
# nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --production-tag NanoV12_2022${channel}data_Version9 >>NanoV12_2022${channel}data_Version9.log & 
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --tag NanoV12_2022EE${channel}data_Version9 >> production_status${channel}_Version9.txt &
python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --tag NanoV12_2022${channel}data_Version9 >> production_status${channel}_Version9.txt & 

sleep 600

fi
done