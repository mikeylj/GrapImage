# -*- coding: utf-8 -*-

import os
import imghdr
import hashlib


root_dir = "/home/ylj/tag_sys/GrapImage/baike_fl/download/"
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
		print pic_full_name, pic_type

		m2 = hashlib.md5()
		m2.update(pic_full_name)
		filename = m2.hexdigest();
		print filename, flow_name_dir + filename
		os.rename(pic_full_name, flow_name_dir + filename)

		if pic_type:
			os.rename(flow_name_dir + filename,flow_name_dir + filename+"."+pic_type)
		else:
			os.rename(flow_name_dir + filename, flow_name_dir + filename + ".jpg")
		print "pic_full_name:"+pic_full_name
