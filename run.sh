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
sed -i  's/scopes = \["mt"\]/scopes = ["mt", "et", "tt"]/' lawluigi_configs/KingMaker_lxplus_luigi.cfg

if grep -q 'scopes = \["mt", "et", "tt"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg ;
then
echo running for ${channel}; 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt  --workers 1 --production-tag NanoV12_2022MC_singletop${channel}_Version8_allsyst >> NanoV12_2022MC_singletop${channel}_Version8_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt  --workers 1 --production-tag NanoV12_2022MC_diboson${channel}_Version8_allsyst >> NanoV12_2022MC_diboson${channel}_Version8_allsyst.log & 
sleep 300

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt  --workers 1 --production-tag NanoV12_2022EEMC_singletop${channel}_Version8_allsyst >> NanoV12_2022EEMC_singletop${channel}_Version8_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt  --workers 1 --production-tag NanoV12_2022EEMC_diboson${channel}_Version8_allsyst >> NanoV12_2022EEMC_diboson${channel}_Version8_allsyst.log & 
sleep 300

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar${channel}_Version8_allsyst >> NanoV12_2022MC_ttbar${channel}_Version8_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar${channel}_Version8_allsyst >> NanoV12_2022EEMC_ttbar${channel}_Version8_allsyst.log & 
sleep 300

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list Version8_2022missing.txt  --workers 1 --production-tag NanoV12_2022MC_ttbar${channel}_Version8_allsyst >> NanoV12_2022MC_ttbar${channel}_Version8_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list Version8_2022EEmissing.txt  --workers 1 --production-tag NanoV12_2022EEMC_ttbar${channel}_Version8_allsyst >> NanoV12_2022EEMC_ttbar${channel}_Version8_allsyst.log & 
sleep 300

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt  --workers 1 --production-tag NanoV12_2022MC_htautau${channel}_Version8_allsyst >> NanoV12_2022MC_htautau${channel}_Version8_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt  --workers 1 --production-tag NanoV12_2022EEMC_htautau${channel}_Version8_allsyst >> NanoV12_2022EEMC_htautau${channel}_Version8_allsyst.log & 
sleep 300


nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_dyjets${channel}_Version8_allsyst >> NanoV12_2022EEMC_dyjets${channel}_Version8_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt  --workers 1 --production-tag NanoV12_2022MC_dyjets${channel}_Version8_allsyst >> NanoV12_2022MC_dyjets${channel}_Version8_allsyst.log & 
sleep 300

nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt  --workers 1 --production-tag NanoV12_2022EEMC_wjets${channel}_Version8_allsyst >> NanoV12_2022EEMC_wjets${channel}_Version8_allsyst.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt  --workers 1 --production-tag NanoV12_2022MC_wjets${channel}_Version8_allsyst >> NanoV12_2022MC_wjets${channel}_Version8_allsyst.log & 
sleep 300

fi


# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_singletop.txt   --tag NanoV12_2022MC_singletop${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_diboson.txt   --tag NanoV12_2022MC_diboson${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_ttbar.txt   --tag NanoV12_2022MC_ttbar${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_htautau.txt   --tag NanoV12_2022MC_htautau${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_hbb.txt   --tag NanoV12_2022MC_hbb${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_dyjets.txt   --tag NanoV12_2022MC_dyjets${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022MC_wjets.txt   --tag NanoV12_2022MC_wjets${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_singletop.txt   --tag NanoV12_2022EEMC_singletop${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_diboson.txt   --tag NanoV12_2022EEMC_diboson${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_ttbar.txt   --tag NanoV12_2022EEMC_ttbar${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_htautau.txt   --tag NanoV12_2022EEMC_htautau${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config --samplelist  sample_database/Htautau_input_list/NanoV12_2022EEMC_hbb.txt   --tag NanoV12_2022EEMC_hbb${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_dyjets.txt   --tag NanoV12_2022EEMC_dyjets${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EEMC_wjets.txt   --tag NanoV12_2022EEMC_wjets${channel}_Version8_allsyst >> production_status${channel}_Version8_allsyst.txt & 



## for running data
for channel in  et tt mt em;
do 
replacement="scopes = [\"${channel}\"]"
sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"
if grep -q 'scopes = \["'"${channel}"'"\]' lawluigi_configs/KingMaker_lxplus_luigi.cfg; 
then
echo running for ${channel}; 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --production-tag NanoV12_2022EE${channel}data_Version8 >>NanoV12_2022EE${channel}data_Version8_.log & 
nohup law run ProduceSamples --local-scheduler False --analysis tau  --config config --sample-list sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --production-tag NanoV12_2022${channel}data_Version8 >>NanoV12_2022${channel}data_Version8_.log & 
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022EE${channel}data.txt --tag NanoV12_2022EE${channel}data_Version8 >> production_status${channel}_Version8.txt &
# python3 scripts/ProductionStatus.py  --analysis tau  --config config  --samplelist sample_database/Htautau_input_list/NanoV12_2022${channel}data.txt --tag NanoV12_2022${channel}data_Version8 >> production_status${channel}_Version8.txt & 

sleep 300

fi
done