# -*- coding: utf-8 -*-

from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os

model = ResNet50(weights='imagenet')

pathName = '/home/ylj/tag_sys/GrapImage/new_baidu_flower'

def getClasses(path):
    for dir_path, dir_names, file_names in os.walk(path):
        if '.DS_Store' in file_names:
            file_names.remove('.DS_Store')
            p = os.path.join(dir_path, '.DS_Store')
            os.remove(p)
            print p
        fileNums = len(file_names)

        print dir_path, fileNums



# img_path = '/home/ylj/tag_sys/PIC_DATA/train/桉叶藤/c_816669_0_3813.jpeg'
# img = image.load_img(img_path, target_size=(224, 224))
# x = image.img_to_array(img)
# x = np.expand_dims(x, axis=0)
# x = preprocess_input(x)
#
# preds = model.predict(x)
# print('Predicted:', decode_predictions(preds, top=3)[0])