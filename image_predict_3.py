#coding: utf-8

import keras
from keras.models import load_model
from keras.models import Sequential
import cv2
import numpy as np
from keras.preprocessing import image
import sys

if __name__ == '__main__':
    image_paths = [
        # 'test_img/train/桂花/3701.jpg',
        # 'test_img/train/桂花/3702.jpg',
        # 'test_img/train/桂花/3703.jpg',
        # 'test_img/train/梅花/4879.jpg',
        # 'test_img/train/梅花/4880.jpg',
        # 'test_img/train/梅花/4881.jpg',
        # 'test_img/train/牡丹/6.jpg',
        # 'test_img/train/牡丹/12.jpg',
        # 'test_img/train/牡丹/23.jpg',
        # 'test_img/train/荷花/3367.jpg',
        # 'test_img/train/荷花/3368.jpg',
        # 'test_img/train/荷花/3369.jpg',
        # 'test_img/train/菊花/7713.jpg',
        # 'test_img/train/菊花/7714.jpg',
        # 'test_img/train/菊花/7715.jpg',
        '/home/yulijun/tag_sys/test/flower/test_img/knx_1.jpg',
        '/home/yulijun/tag_sys/test/flower/test_img/knx_2.jpg',
        '/home/yulijun/tag_sys/test/flower/test_img/knx_3.jpg',

    ]
    model = load_model('/home/yulijun/tag_sys/test/flower/vgg_final.h5')
    for arg in sys.argv:
        if "jpg" in arg:
            # print arg
            img = image.load_img(arg, target_size=(150, 150))
            x = image.img_to_array(img).astype(np.float32) / 255
            # print(x.shape)
            x = np.expand_dims(x, axis=0)
            # print(x.shape)
            probs = model.predict(x)
            print np.argmax(probs)

    # for p in image_paths:
    #     # img = cv2.imread(p)
    #     #
    #     # img = cv2.resize(img, (150, 150))
    #     # img = np.reshape(img, [1, 150, 150, 3])
    #     # classes = model.predict(img)
    #     # print np.argmax(classes)
    #
    #     # model2.load_weights("bottleneck_fc_model.h5")
    #     # print('Model CAT DOG loaded.')
    #
    #     img = image.load_img(p, target_size=(150, 150))
    #     x = image.img_to_array(img).astype(np.float32) / 255
    #     # print(x.shape)
    #     x = np.expand_dims(x, axis=0)
    #     # print(x.shape)
    #     probs = model.predict(x)
    #     print np.argmax(probs)
    #
    #     # img = cv2.imread(p)
    #     # img = cv2.resize(img, (150, 150)).astype(np.float32) / 255.
    #     # # print img
    #     # img = img.reshape(1,  img.shape[0], img.shape[1], img.shape[2],)
    #     #
    #     # # feature = model1.predict(img)
    #     # probs = model.predict(img)
    #     # print "probs: ", np.argmax(probs)
    #
    #
    #
    #
    #     # prediction = probs.argmax(axis=1)
    #     # print "prediction: ", prediction
    #
    #     # bottom_features = vgg16(p)
    #     #
    #     # prediction = head_model(bottom_features)
    #     # print p
    #     # print prediction
    #     # # prediction, probability = head_model(bottom_features)
    #     # #
    #     # # print(prediction, probability)
    #
    # # print('the program is done')