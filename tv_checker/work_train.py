# -*- coding: cp936 -*-
from keras.models import load_model
import cv2
import json, os
import numpy as np

from CreateCate import CreateCate


s = CreateCate()
cates2class = s.load_mapdict('my_mapdict.pickle')

model = load_model('my_model2.h5')

def get_name(l):
    return s.get_class_by_cate(cates2class, l)

def predict_name(picpath):
    s = cv2.imread(picpath).astype(np.float32)/255
    v = model.predict(s[None,])
    return get_name(v)

def save_pic(picpath):
    dirs = predict_name(picpath)
    name = picpath.split('/')[-1]
    if not dirs:
        print picpath,'not find'
        dirs = 'notfind'
    newdirs = os.path.join('pictt',dirs)
    newpath = os.path.join(newdirs,name)
    if not os.path.isdir(newdirs):
        os.makedirs(newdirs)
    s = cv2.imread(picpath)
    cv2.imwrite(newpath, s)
    

if __name__ == '__main__':
    for i in range(1,3001):
        picpath = 'pict/'+str(i)+'.png'
        print picpath
        save_pic(picpath)
