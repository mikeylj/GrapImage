# -*- coding: utf-8 -*-

import os


root_dir = "download_goo/"
for dirname in os.listdir(root_dir):
	
	if dirname == ".DS_Store":
		continue
#	print dirname+"/data.log"
	lines = open(root_dir+dirname+"/data.log","r").readlines()
#	print lines
	for line_item in lines:
		if not line_item.strip():
			print "empty"
			continue
		arr_data = line_item.strip('\n').split("\t")
		shell_cmd = "wget --user-agent=\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36\" -T2 -w0.5 -t1 \""+arr_data[0]+"\" --referer=\""+arr_data[1]+"\"  -o down_goo.log  -P "+root_dir+dirname+"/"
		print shell_cmd
		ret_value=os.system(shell_cmd)
		print ret_value
		#break
	#print lines
