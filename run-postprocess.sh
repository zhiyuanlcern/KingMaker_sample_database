
for channel in  'et';
do 
for i in  2022EE 2022postEE;
do 
cd ${i}_${channel}_run4_allsyst
# mkdir -p ${i}_${channel}
# cd ${i}_${channel}_run2_double_corrected
# cd ${i}_signals
for f in ./*root ; 
# do 
do
# echo $f
python /data/bond/zhiyuanl/Plotting/post-process.py  $f  >> postprocess.log&    

done 
cd -
done
done

