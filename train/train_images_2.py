# -*- coding: utf-8 -*-

from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, Input
from keras.engine.training import Model
import numpy as np
from keras.utils import to_categorical #多分类
from PIL import ImageFile

# path to the model weights files.
# weights_path = '../keras/examples/vgg16_weights.h5'
# dimensions of our images.
ImageFile.LOAD_TRUNCATED_IMAGES = True
img_width, img_height = 150, 150

top_model_weights_path = './trained_vgg16/bottleneck_fc_model_weights.h5'
train_data_dir = '/home/ylj/tag_sys/GrapImage/new_data_train/train'
validation_data_dir = '/home/ylj/tag_sys/GrapImage/new_data_train/validation'
dic_num = 11

train_num   = 3200
test_num    = 160

nb_train_samples = train_num * dic_num
nb_validation_samples = test_num * dic_num

# nb_train_samples = 15000
# nb_validation_samples = 2500
epochs = 500
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
top_model.add(Dense(dic_num, activation='softmax'))

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

# for i,layer in enumerate(model.layers):
#     print i, layer.name
#
# # import os
# # os._exit(0)
#
# for layer in model.layers[:19]:
#     layer.trainable = False
# for layer in model.layers[19:]:
#     layer.trainable = True

# compile the model with a SGD/momentum optimizer
# and a very slow learning rate.
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])

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

model.save('./trained_vgg16/vgg_final_vgg19.h5')
