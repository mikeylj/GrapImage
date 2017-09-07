# -*- coding: utf-8 -*-


import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, Input
from keras import applications
from keras.utils import to_categorical #多分类
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from keras.models import load_model
import cv2
import os
from keras import backend as K

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# dimensions of our images.
img_width, img_height = 150, 150

top_model_weights_path = './trained_vgg16/bottleneck_fc_model_weights.h5'
train_data_dir = '/home/ylj/tag_sys/GrapImage/new_data_train/train'
validation_data_dir = '/home/ylj/tag_sys/GrapImage/new_data_train/validation'
dic_num = 8

train_num   = 960
test_num    = 320

nb_train_samples = train_num * dic_num
nb_validation_samples = test_num * dic_num
epochs = 50
batch_size = 16

#设定GPU使用内存大小(Tensorflow backend)
def get_session(gpu_fraction=0.3):
    '''Assume that you have 6GB of GPU memory and want to allocate ~2GB'''

    num_threads = os.environ.get('OMP_NUM_THREADS')
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)

    if num_threads:
        return tf.Session(config=tf.ConfigProto(
            gpu_options=gpu_options, intra_op_parallelism_threads=num_threads))
    else:
        return tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

# KTF.set_session(get_session())


def save_bottlebeck_features():
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size)
    np.save(open('./trained_vgg16/bottleneck_features_train.npy', 'w'),
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size)
    np.save(open('./trained_vgg16/bottleneck_features_validation.npy', 'w'),
            bottleneck_features_validation)


def train_top_model():
    train_data = np.load(open('./trained_vgg16/bottleneck_features_train.npy'))
    # train_labels = np.array(
    #     [0] * 3000 + [1] * 3000 + [2] * 3000 + [3] * 3000 + [4] * 2992)
    labels = []
    for i in range(dic_num):
        for j in range(train_num):
            labels.append(i)
    train_labels = np.array(
        labels
    )
    # for k, v in enumerate(train_labels):
    #     print k, '====>', v

    validation_data = np.load(open('./trained_vgg16/bottleneck_features_validation.npy'))
    # validation_labels = np.array(
    #     [0] * 500 + [1] *500 + [2] * 500 + [3] * 500 + [4] * 496)
    labels = []
    for i in range(dic_num):
        for j in range(test_num):
            labels.append(i)
    validation_labels = np.array(
        labels
    )
    print validation_labels.shape
    for k, v in enumerate(validation_labels):
        print k, '====>', v

    train_labels = to_categorical(np.array(train_labels))  # 转numpy数组
    validation_labels = to_categorical(np.array(validation_labels))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(dic_num, activation='softmax'))

    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy', metrics=['accuracy'])

    print train_data.shape
    print train_labels.shape

    print validation_data.shape
    print validation_labels.shape
    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    # model.save_weights(top_model_weights_path)
    model.save_weights(top_model_weights_path)
#训练
save_bottlebeck_features()
train_top_model()

# model = Sequential()
# model =load_model(top_model_weights_path)
# model.compile(loss='binary_crossentropy',
#               optimizer='rmsprop',
#               metrics=['accuracy'])

# img = cv2.imread('./data/train/梅花/125.jpg')
# img = cv2.resize(img,(150,150))
# img = np.reshape(img,[1,150,150,3])
# classes = model.predict_classes(img)
# print classes

# #测试
# datagen = ImageDataGenerator(rescale=1. / 255)
#
# input_tensor = Input(shape=(150,150,3))
# # build the VGG16 network
# # model = applications.VGG16(include_top=False, weights='imagenet')
# model = applications.VGG16(weights='imagenet',include_top= False,input_tensor=input_tensor)
#
# test_data_dir   = 'data/train/'
# generator = datagen.flow_from_directory(
#         test_data_dir,
#         target_size=(img_width, img_height),
#         batch_size=1,
#         class_mode=None,
#         shuffle=False)
# bottleneck_features_train = model.predict_generator(
#         generator, 6000)
# print bottleneck_features_train.shape
#
# # build a classifier model to put on top of the convolutional model
# top_model = Sequential()
# top_model.add(Flatten(input_shape=model.output_shape[1:]))
# top_model.add(Dense(256, activation='relu'))
# top_model.add(Dropout(0.5))
# top_model.add(Dense(dic_num, activation='softmax'))
#
# # note that it is necessary to start with a fully-trained
# # classifier, including the top classifier,
# # in order to successfully do fine-tuning
# top_model.load_weights(top_model_weights_path)



# model.predict()

# print bottleneck_features_train.shape
# #
# classes = top_model.predict(bottleneck_features_train)
# print classes
# i = 1
# for c in classes:
#     print  i, '====>', np.argmax(c)
#     i = i +1



