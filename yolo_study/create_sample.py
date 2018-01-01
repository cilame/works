# -*- coding: utf-8 -*-
import cv2
import numpy as np
import random as rd
import os

from GridLable import *

rd_outwin = False
w,h = 448,448
gridw,gridh = 14,14

f = open('pic.txt','a')
if not os.path.isdir('pic'):
    os.mkdir('pic')

###################函数是“顶角坐标”与“中点长宽”数据转换函数，用以对边框进行限制
###################将其通常转换为左右角点的坐标进行最大边框约束
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

def limit_size(x1,y1,x2,y2,maxx,maxy):
    if x1 < 0:x1 = 0
    if y1 < 0:y1 = 0
    if x2 > maxx:x2 = maxx
    if y2 > maxy:y2 = maxy
    return x1,y1,x2,y2
###################


# 根据总长度和 grid 获取一个 grid 区域中心点以及其随机偏差为 0.25 的坐标
def get_anchors(lens,grid):
    anchors = {}
    for i in range(grid):
        anchor = lens/grid
        anchors[i] = [i, int((i+0.25) * anchor),int((i+0.75) * anchor)]
    return anchors

# 根据总长度和 grid 获取一个简单的随机边框（偏差为 0.9~1.7 倍化切块的长宽的）大小
def get_rdscal(lens,grid):
    return int((rd.random()*8+.9)*lens/grid)

# 就是前两个函数的综合利用，通过长宽以及长宽上的 grid 获取相应的随机边框及其坐标框
def get_rdxywh(w,h,gridw,gridh,num):
    y,x = np.mgrid[:gridh,:gridw]
    all_points = np.concatenate((x[...,None],y[...,None]),-1).reshape((-1,2))
    all_rdxywh = []
    for y,x in rd.sample(all_points,num):
        anchorsy = get_anchors(h,gridh)
        anchorsx = get_anchors(w,gridw)
        rdh = get_rdscal(h,gridh)
        rdw = get_rdscal(w,gridw)
        rdareax = anchorsx[x]
        rdareay = anchorsy[y]
        rdx = rd.randint(*rdareax[1:])
        rdy = rd.randint(*rdareay[1:])
        rdscalx = rdareax[0]
        rdscaly = rdareay[0]
        all_rdxywh.append([rdx,rdy,rdw,rdh,rdscalx,rdscaly])
    return all_rdxywh


def get_rdcolor(num):
    colorNinx = rd.sample([['red',2],['green',1],['blue',0]],num)
    return colorNinx

def create_samples(w,h,gridw,gridh,num=2):
    pic = np.zeros((h,w,3))
    rdcolor = get_rdcolor(num)
    rdxywh  = get_rdxywh(w,h,gridw,gridh,num)
    all_create = zip(rdcolor,rdxywh)
    all_created = []
    for (color,inx),(rdx,rdy,rdw,rdh,rdscalx,rdscaly) in all_create:
        x1,y1,x2,y2 = to_xyxy(rdx,rdy,rdw,rdh)
        x1,y1,x2,y2 = limit_size(x1,y1,x2,y2,w,h)
        pic[y1:y2,x1:x2,inx]=255
        xx,yy,ww,hh = to_xywh(x1,y1,x2,y2)
        all_created.append([xx,yy,ww,hh,color])
    return pic,all_created



s = GridLable(twth = (w,h), gridwh = (gridw,gridh))
for i in range(20):
    picpath = 'pic/%05d.jpg'%i
    pic,all_created = create_samples(w,h,gridw,gridh,num=3)
    # num 代表在一张图片里面添加的边框数
    # 因为颜色限制，最大只能选 3
    cv2.imwrite(picpath,pic)
    for xx,yy,ww,hh,color in all_created:
        print '{} {} {} {} {} {}'.format(picpath,xx,yy,ww,hh,color)
        print s.create_label((xx,yy,ww,hh))[1:]
    

