#!/usr/bin/python
#-*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import shutil
import os
import uuid
import keras
from keras.models import load_model
from keras.models import Sequential
import cv2
import numpy as np
from keras.preprocessing import image
import sys

class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index_get.html",)

    def post(self):
        upload_path=os.path.join(os.path.dirname(__file__),'static/img')  #文件的暂存路径
        file_metas=self.request.files['file']    #提取表单中‘name’为‘file’的文件元数据
        flower_name = ''
        for meta in file_metas:
            filename=uuid.uuid1().__str__() + '_'  + meta['filename']
            filepath=os.path.join(upload_path,filename)
            with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            # self.write(filepath)
            img = image.load_img(filepath, target_size=(150, 150))
            x = image.img_to_array(img).astype(np.float32) / 255
            # print(x.shape)
            x = np.expand_dims(x, axis=0)
            # print(x.shape)
            probs = model.predict(x)
            # # print p, np.argmax(probs)
            # # self.write(filepath)
            # print type(np.argmax(probs))
            flower_type = int(np.argmax(probs))
            fTypes = self.getFlowerTypes()
            print flower_type
            print fTypes[flower_type]
            flower_name = fTypes[flower_type]
        self.render("index_post.html",
                    flower_name = flower_name,
                    flower_img = filename
                    )

    def getFlowerTypes(self):
        fTypes = []
        top_dir = './data/train'
        for i in sorted(os.listdir(top_dir)):
            if os.path.isdir(os.path.join(top_dir, i)):
                fTypes.append(i)

        return fTypes

model_path = os.path.join(os.path.dirname(__file__),'vgg_final.h5')
model = load_model(model_path)
print model_path




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/file', UploadFileHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)





















# app=tornado.web.Application([
#     (r'/file',UploadFileHandler),
# ])

if __name__ == '__main__':
    # app.listen(3000)
    # tornado.ioloop.IOLoop.instance().start()
    # tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(3000)
    tornado.ioloop.IOLoop.instance().start()