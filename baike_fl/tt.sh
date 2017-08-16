cu_dir=$(pwd)
for file in tmp/*  
do  
cd $cu_dir/$file
cat data.log
echo $file
done  
