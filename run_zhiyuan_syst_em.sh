
replacement="shifts = [\"All\"]"
sed -i '/^shifts = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"
replacement="files_per_task = 3"
sed -i '/^files_per_task = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"

replacement="scopes = [\"em\"]"
sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"

sleep 5

law run ProduceSamples --local-scheduler False --analysis tau  --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_all.txt  --workers 1 --production-tag NanoV14_2022MC_all_Version13_syst_em > KingMaker_logs/NanoV12_2022MC_all_Version13_syst.log & 
# python3 scripts/ProductionStatus.py --analysis tau --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2023MC_all.txt --production-tag NanoV14_2023MC_all_Version13_syst_em &

sleep 500
replacement="scopes = [\"em\"]"
sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"

law run ProduceSamples --local-scheduler False --analysis tau  --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2023MC_all.txt  --workers 1 --production-tag NanoV14_2023MC_all_Version13_syst_em > KingMaker_logs/NanoV12_2023MC_all_Version13_syst.log & 
# python3 scripts/ProductionStatus.py --analysis tau --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2022MC_all.txt --production-tag NanoV14_2022MC_all_Version13_syst_em &





sleep 500


replacement="shifts = [\"All\"]"
sed -i '/^shifts = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"
replacement="files_per_task = 1"
sed -i '/^files_per_task = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"

replacement="scopes = [\"em\"]"
sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"


law run ProduceSamples --local-scheduler False --analysis tau  --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2022signal_all.txt  --workers 1 --production-tag NanoV14_2022signal_all_Version13_syst_em > KingMaker_logs/NanoV12_2022signal_all_Version13_syst.log & 
# python3 scripts/ProductionStatus.py --analysis tau --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2023signal_all.txt --production-tag NanoV14_2023signal_all_Version13_syst_em &
sleep 500
replacement="scopes = [\"em\"]"
sed -i '/^scopes = /c\'"$replacement" "lawluigi_configs/KingMaker_lxplus_luigi.cfg"
law run ProduceSamples --local-scheduler False --analysis tau  --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2023signal_all.txt  --workers 1 --production-tag NanoV14_2023signal_all_Version13_syst_em > KingMaker_logs/NanoV12_2023signal_all_Version13_syst.log & 
# python3 scripts/ProductionStatus.py --analysis tau --config config_fullsyst --sample-list sample_database/Htautau_input_list/NanoV12_2022signal_all.txt --production-tag NanoV14_2022signal_all_Version13_syst_em &


