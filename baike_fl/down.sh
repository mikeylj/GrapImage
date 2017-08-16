cu_dir=$(pwd)
for file in download/*  
do  
cd $cu_dir/$file
echo $file
wget -N -T2 -w0.5 -t1  -i data.log -o ../down.log
done
