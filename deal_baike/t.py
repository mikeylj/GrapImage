#coding: utf-8

import os,math
import sys
proc_count = 3  #int(sys.argv[2])
proc_num    = 1  #int(sys.argv[1])

dir_name = []
for i in os.listdir("./"):
    dir_name.append(i)

dir_count = len(dir_name)
count_per_proc = int(math.ceil(float(dir_count)/proc_count))
remainder_count = int(float(dir_count)%proc_count)
print dir_count, count_per_proc,remainder_count

print dir_name

for x in range(count_per_proc):
    pos = (proc_num - 1) * count_per_proc + x
    if pos > dir_count - 1:
        break
    print "pos:", pos, "/", dir_count
    print dir_name[pos]



