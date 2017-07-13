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
        './images/gh_1.jpg',
        './images/gh_2.jpg',
        './images/gh_3.jpg',
        './images/gh_4.jpg',
        './images/gh_5.jpg',
        './images/hh_1.jpg',
        './images/hh_2.jpg',
        './images/hh_3.jpg',
        './images/hh_4.jpg',
        './images/hh_5.jpg',
        './images/jh_1.jpg',
        './images/jh_2.jpg',
        './images/jh_3.jpg',
        './images/jh_4.jpg',
        './images/jh_5.jpg',
        './images/knx_1.jpg',
        './images/knx_2.jpg',
        './images/knx_3.jpg',
        './images/knx_4.jpg',
        './images/knx_5.jpg',
        './images/mh_1.jpg',
        './images/mh_2.jpg',
        './images/mh_3.jpg',
        './images/mh_4.jpg',
        './images/mh_5.jpg',
        './images/mlh_1.jpg',
        './images/mlh_2.jpg',
        './images/mlh_3.jpg',
        './images/mlh_4.jpg',
        './images/mlh_5.jpg',
        './images/mb_1.jpg',
        './images/mb_2.jpg',
        './images/mb_3.jpg',
        './images/mb_4.jpg',
        './images/mb_5.jpg',
        './images/yjx_1.jpg',
        './images/yjx_2.jpg',
        './images/yjx_3.jpg',
        './images/yjx_4.jpg',
        './images/yjx_5.jpg',

    ]
    # 桂花
    # 荷花
    # 菊花
    # 康乃馨
    # 梅花
    # 茉莉
    # 牡丹
    # 郁金香

    model = load_model('/home/hlgdeep/ai/keras/ImgClassify/vgg_final.h5')
    # for arg in sys.argv:
    #     if "jpg" in arg:
    #         # print arg
    #         img = image.load_img(arg, target_size=(150, 150))
    #         x = image.img_to_array(img).astype(np.float32) / 255
    #         # print(x.shape)
    #         x = np.expand_dims(x, axis=0)
    #         # print(x.shape)
    #         probs = model.predict(x)
    #         print np.argmax(probs)

    for p in image_paths:
        # img = cv2.imread(p)
        #
        # img = cv2.resize(img, (150, 150))
        # img = np.reshape(img, [1, 150, 150, 3])
        # classes = model.predict(img)
        # print np.argmax(classes)

        # model2.load_weights("bottleneck_fc_model.h5")
        # print('Model CAT DOG loaded.')

        img = image.load_img(p, target_size=(150, 150))
        x = image.img_to_array(img).astype(np.float32) / 255
        # print(x.shape)
        x = np.expand_dims(x, axis=0)
        # print(x.shape)
        probs = model.predict(x)
        print p, np.argmax(probs)
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