# -*- coding: utf-8 -*-

import os
import imghdr


root_dir = "download_goo/"
for dirname in os.listdir(root_dir):

        if dirname == ".DS_Store":
                continue
#       print dirname+"/data.log"
	flow_name_dir = root_dir + dirname + "/"
	for pic_name in os.listdir( flow_name_dir):
		if pic_name=="data.log":
			continue
		arr_pic_name_ext = os.path.splitext(pic_name)
		if not arr_pic_name_ext[1] == "":
			continue
		pic_full_name = flow_name_dir+pic_name
		pic_type = imghdr.what(pic_full_name)
		os.rename(pic_full_name,pic_full_name+"."+pic_type)
		print "pic_full_name:"+pic_full_name
