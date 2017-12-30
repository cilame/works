import cv2
import numpy as np
import random as rd
import os

from GridLable import *

rd_outwin = False
w,h = 90,90
gridw,gridh = 3,3

def get_anchors(lens,grid):
    anchors = {}
    for i in range(grid):
        anchor = lens/grid
        anchors[i] = [i, int((i+0.25) * anchor),int((i+0.75) * anchor)]
    return anchors

def get_rdscal(lens,grid):
    return int((rd.random()*.7+.7)*lens/grid)
    

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

def to_xyxy(x,y,w,h):
    x1 = x - w/2
    x2 = x + w/2
    y1 = y - h/2
    y2 = y + h/2
    return x1,y1,x2,y2

def local_zero(x1,y1,x2,y2):
    if x1 < 0:
        x2 = x1 + x2
        x1 = 0
    if y1 < 0:
        y2 = y1 + y2
        y1 = 0
    return x1,y1,x2,y2

def create_sample(w,h,gridw,gridh,inx):
    pic = np.zeros((h,w,3))
    rdxywh = get_rdxywh(w,h,gridw,gridh)
    x1,y1,x2,y2 = local_zero(*to_xyxy(*rdxywh[:-2]))
    scax,scay = rdxywh[-2:]
    pic[x1:x2,y1:y2,inx]=255
    return pic,x1,y1,x2,y2,rdxywh



f = open('pic.txt','a')

if not os.path.isdir('pic'):
    os.mkdir('pic')

for i in range(20):
    color = rd.choice(['red','green','blue'])
    if color == 'red': inx = 2
    if color == 'green': inx = 1
    if color == 'blue': inx = 0
    picpath = 'pic/%05d.jpg'%i
    pic,x1,y1,x2,y2,rdxywh = create_sample(w,h,gridw,gridh,inx)
    cv2.imwrite(picpath,pic)
    print color,x1,y1,x2,y2,rdxywh

s = GridLable(twth = (448,448), gridwh = (3,3))
s.create_label(xywh = (50,40,3,3))

