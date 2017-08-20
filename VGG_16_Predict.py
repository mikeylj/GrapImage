# -*- coding: utf-8 -*-

from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os
from keras import applications

model = applications.VGG16(weights='imagenet')

pathName = '/home/ylj/tag_sys/GrapImage/baike_fl/baike_train/'

def get_top_predictions(preds, top=5):
    """Decodes the prediction of an ImageNet model.

    # Arguments
        preds: Numpy tensor encoding a batch of predictions.
        top: integer, how many top-guesses to return.

    # Returns
        A list of lists of top class prediction tuples
        `(class_name, class_description, score)`.
        One list of tuples per sample in batch input.

    # Raises
        ValueError: in case of invalid shape of the `pred` array
            (must be 2D).
    """
    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        # result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        # result.sort(key=lambda x: x[2], reverse=True)
        # results.append(result)
    return top_indices

def getClasses(path):
    image_paths = []
    for dir_path, dir_names, file_names in os.walk(path):
        if '.DS_Store' in file_names:
            file_names.remove('.DS_Store')
            p = os.path.join(dir_path, '.DS_Store')
            os.remove(p)
            print p
        if len(file_names) > 2:
            for f in file_names:
                # print dir_path + '/' + f
                image_paths.append(dir_path + '/' + f)
        # fileNums = len(file_names)
        # print dir_path, fileNums

    return image_paths;

images = getClasses(pathName)

for p in images:
    print p
    img = image.load_img(p, target_size=(150, 150))
    x = image.img_to_array(img).astype(np.float32) / 255
    # print(x.shape)
    x = np.expand_dims(x, axis=0)
    # print(x.shape)
    probs = model.predict(x)
    # print p, np.argmax(probs)
    print p, get_top_predictions(probs, 3)




# img_path = '/home/ylj/tag_sys/PIC_DATA/train/桉叶藤/c_816669_0_3813.jpeg'
# img = image.load_img(img_path, target_size=(224, 224))
# x = image.img_to_array(img)
# x = np.expand_dims(x, axis=0)
# x = preprocess_input(x)
#
# preds = model.predict(x)
# print('Predicted:', decode_predictions(preds, top=3)[0])