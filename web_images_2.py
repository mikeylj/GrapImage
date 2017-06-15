# -*- coding: utf-8 -*-


import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.utils import to_categorical #多分类
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from keras.models import load_model
# import cv2
import os
from keras import backend as K

# dimensions of our images.
img_width, img_height = 150, 150

top_model_weights_path = '/home/ylj/tag_sys/PIC_DATA/bottleneck_fc_model_weights.h5'
train_data_dir = '/home/ylj/tag_sys/PIC_DATA/train'
validation_data_dir = '/home/ylj/tag_sys/PIC_DATA/validation'
nb_train_samples = 168000
nb_validation_samples = 42000
epochs = 50
batch_size = 16


train_datas = os.listdir(train_data_dir)
validation_datas = os.listdir(validation_data_dir)
if '.DS_Store' in train_datas:
    train_datas.remove('.DS_Store')
if '.DS_Store' in validation_datas:
    validation_datas.remove('.DS_Store')

train_type_count = len(train_datas)
validation_type_count = len(validation_datas)

print train_type_count
print validation_type_count
# os._exit(0)

#设定GPU使用内存大小(Tensorflow backend)
def get_session(gpu_fraction=0.7):
    '''Assume that you have 6GB of GPU memory and want to allocate ~2GB'''

    num_threads = os.environ.get('OMP_NUM_THREADS')
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)

    if num_threads:
        return tf.Session(config=tf.ConfigProto(
            gpu_options=gpu_options, intra_op_parallelism_threads=num_threads))
    else:
        return tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

KTF.set_session(get_session())


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
    np.save(open('bottleneck_features_train.npy', 'w'),
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size)
    np.save(open('bottleneck_features_validation.npy', 'w'),
            bottleneck_features_validation)


def train_top_model():
    train_data = np.load(open('bottleneck_features_train.npy'))

    train_labels = np.zeros(4800)
    for i in range(1, train_type_count):
        x = np.zeros(4800) + i
        train_labels = np.concatenate((train_labels,x),axis=0)
    # train_labels = np.array(
    #     [0] * 1500 + [1] * 1500 + [2] * 1500 + [3] * 1500 + [4] * 1500 + [5] * 1500 + [6] * 1500 + [7] * 1500)

    validation_data = np.load(open('bottleneck_features_validation.npy'))
    # validation_labels = np.array(
    #     [0] * 500 + [1] *500 + [2] * 500 + [3] * 500 + [4] * 500 + [5] * 500 + [6] * 500 + [7] * 500)
    validation_labels   = np.zeros(1200)
    for i in range(1, validation_type_count):
        x = np.zeros(1200) + i
        validation_labels = np.concatenate((validation_labels,x),axis=0)

    print train_labels.shape
    print validation_labels.shape
    # print validation_labels
    # os._exit(0)


    train_labels = to_categorical(np.array(train_labels))  # 转numpy数组
    validation_labels = to_categorical(np.array(validation_labels))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(35, activation='softmax'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])

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
# # build the VGG16 network
# model = applications.VGG16(include_top=False, weights='imagenet')
# test_data_dir   = 'test_img/train'
# generator = datagen.flow_from_directory(
#         test_data_dir,
#         target_size=(img_width, img_height),
#         batch_size=1,
#         class_mode=None,
#         shuffle=False)
# bottleneck_features_train = model.predict_generator(
#         generator, 15 // 1)
# # print bottleneck_features_train.shape
#
# model =load_model(top_model_weights_path)
#
#
# # model.predict()
#
# print bottleneck_features_train.shape
# # #
# classes = model.predict(bottleneck_features_train)
# print classes
#
# for c in classes:
#     print np.argmax(c)



