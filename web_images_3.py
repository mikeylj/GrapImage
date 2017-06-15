# -*- coding: utf-8 -*-

from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, Input
from keras.engine.training import Model
import numpy as np
from keras.utils import to_categorical #多分类

# path to the model weights files.
# weights_path = '../keras/examples/vgg16_weights.h5'
top_model_weights_path = '/home/ylj/tag_sys/PIC_DATA/bottleneck_fc_model_weights.h5'
# dimensions of our images.
img_width, img_height = 150, 150

train_data_dir = '/home/ylj/tag_sys/PIC_DATA/train'
validation_data_dir = '/home/ylj/tag_sys/PIC_DATA/validation'
nb_train_samples = 168000
nb_validation_samples = 42000
epochs = 50
batch_size = 16

# build the VGG16 network
input_tensor = Input(shape=(150,150,3))
# model = applications.VGG16(weights='imagenet', include_top=False)
base_model = applications.VGG16(weights='imagenet',include_top= False,input_tensor=input_tensor)
# print('Model loaded.')

# build a classifier model to put on top of the convolutional model
top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(35, activation='softmax'))

# note that it is necessary to start with a fully-trained
# classifier, including the top classifier,
# in order to successfully do fine-tuning
top_model.load_weights(top_model_weights_path)

# add the model on top of the convolutional base
# model.add(top_model)
model = Model(inputs= base_model.input, outputs= top_model(base_model.output))

# set the first 25 layers (up to the last conv block)
# to non-trainable (weights will not be updated)
for layer in model.layers[:25]:
    layer.trainable = False

# compile the model with a SGD/momentum optimizer
# and a very slow learning rate.
model.compile(loss='binary_crossentropy',
              optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])

# # prepare data augmentation configuration
# train_datagen = ImageDataGenerator(
#     rescale=1. / 255,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True)
#
# test_datagen = ImageDataGenerator(rescale=1. / 255)
#
# train_generator = train_datagen.flow_from_directory(
#     train_data_dir,
#     target_size=(img_height, img_width),
#     batch_size=batch_size,
#     class_mode=None,
#     shuffle=False)
#
# validation_generator = test_datagen.flow_from_directory(
#     validation_data_dir,
#     target_size=(img_height, img_width),
#     batch_size=batch_size,
#     class_mode=None,
#     shuffle=False)
#
# # # fine-tune the model
# # model.fit_generator(
# #     train_generator,
# #     samples_per_epoch=nb_train_samples,
# #     epochs=epochs,
# #     validation_data=validation_generator,
# #     nb_val_samples=nb_validation_samples)
#
#
# # print train_generator.shape
# # print validation_generator.shape
#
# # model.fit_generator(
# #     train_generator,
# #     steps_per_epoch=nb_train_samples // batch_size,
# #     epochs=epochs,
# #     validation_data=validation_generator,
# #     validation_steps=nb_validation_samples // batch_size,
# # )
# # train_data = np.load(open('bottleneck_features_train.npy'))
# train_labels = np.array(
#         [0] * 3000 + [1] * 3000 + [2] * 3000 + [3] * 3000 + [4] * 2992)
#
# # validation_data = np.load(open('bottleneck_features_validation.npy'))
# validation_labels = np.array(
#         [0] * 500 + [1] *500 + [2] * 500 + [3] * 500 + [4] * 496)
# train_labels = to_categorical(np.array(train_labels))  # 转numpy数组
# validation_labels = to_categorical(np.array(validation_labels))
#
# print train_data.shape
# print train_labels.shape
#
# print validation_data.shape
# print validation_labels.shape
# model.fit(train_data, train_labels,
#               epochs=epochs,
#               batch_size=batch_size,
#               validation_data=(validation_data, validation_labels))











train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
)

model.save('vgg_final.h5')
