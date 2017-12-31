# -*- coding: utf-8 -*-
import cv2
import numpy as np
import random as rd
import os

from GridLable import *

rd_outwin = False
w,h = 90,90
gridw,gridh = 3,3



f = open('pic.txt','a')
if not os.path.isdir('pic'):
    os.mkdir('pic')




###################内部为数据转换函数，用以对边框进行限制
def to_xyxy(x,y,w,h):
    x1 = x - w/2
    x2 = x + w/2
    y1 = y - h/2
    y2 = y + h/2
    return x1,y1,x2,y2

def to_xywh(x1,y1,x2,y2):
    x = (x1 + x2)/2
    y = (y1 + y2)/2
    w = x2 - x1
    h = y2 - y1
    return x, y, w, h

def local_size(x1,y1,x2,y2,maxx,maxy):
    if x1 < 0:x1 = 0
    if y1 < 0:y1 = 0
    if x2 > maxx:x2 = maxx
    if y2 > maxy:y2 = maxy
    return x1,y1,x2,y2
###################


# 根据总长度和 grid 获取一个 grid 区域以及随机偏差为 .25 的坐标
def get_anchors(lens,grid):
    anchors = {}
    for i in range(grid):
        anchor = lens/grid
        anchors[i] = [i, int((i+0.25) * anchor),int((i+0.75) * anchor)]
    return anchors

# 根据总长度和 grid 获取一个简单的随机边框大小
def get_rdscal(lens,grid):
    return int((rd.random()*.8+.9)*lens/grid)

# 就是前两个函数的综合利用，通过长宽以及长宽上的 grid 获取相应的随机边框及其坐标框
def get_rdxywh(w,h,gridw,gridh):
    anchorsy = get_anchors(h,gridh)
    anchorsx = get_anchors(w,gridw)
    rdh = get_rdscal(h,gridh)
    rdw = get_rdscal(w,gridw)
    rdareax = rd.choice(anchorsx)
    rdareay = rd.choice(anchorsy)
    rdx = rd.randint(*rdareax[1:])
    rdy = rd.randint(*rdareay[1:])
    rdscalx = rdareax[0]
    rdscaly = rdareay[0]
    return rdx,rdy,rdw,rdh,rdscalx,rdscaly



def create_sample(w,h,gridw,gridh,inx):
    pic = np.zeros((h,w,3))
    rdxywh = get_rdxywh(w,h,gridw,gridh)
    x1,y1,x2,y2 = to_xyxy(*rdxywh[:-2])
    scax,scay = rdxywh[-2:]
    x1,y1,x2,y2 = local_size(x1,y1,x2,y2,w,h)
    pic[y1:y2,x1:x2,inx]=255
    xx,yy,ww,hh = to_xywh(x1,y1,x2,y2)
    return pic,xx,yy,ww,hh



for i in range(20):
    color = rd.choice(['red','green','blue'])
    if color == 'red': inx = 2
    if color == 'green': inx = 1
    if color == 'blue': inx = 0
    picpath = 'pic/%05d.jpg'%i
    pic,xx,yy,ww,hh = create_sample(w,h,gridw,gridh,inx)
    cv2.imwrite(picpath,pic)
    print '{} {} {} {} {} {}'.format(picpath,xx,yy,ww,hh,color)
    s = GridLable(twth = (w,h), gridwh = (3,3))
    print s.create_label((xx,yy,ww,hh))
    

