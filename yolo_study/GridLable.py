import numpy as np

class GridLable:
    def __init__(self,*args,**kw):
        self._tw,self._th = map(float,kw.get('twth'))
        self._gridw,self._gridh = map(float,kw.get('gridwh'))
        self._gridkw = self._tw / self._gridw
        self._gridkh = self._th / self._gridh
        self._create_grid()
        
    def _create_grid(self):
        y, x = np.mgrid[:self._gridh,:self._gridw]
        self.indx = np.concatenate((y[...,None],x[...,None]),axis=-1)
        
    def _get_index(self,x,y):
        sh = np.arange(0,self._th,self._th/self._gridh)
        sw = np.arange(0,self._tw,self._tw/self._gridw)
        h = max(np.where(sh<y)[0])
        w = max(np.where(sw<x)[0])
        return h,w

    def create_label(self, xywh):
        x,y,w,h = map(float, xywh)
        locy,locx = self._get_index(x,y)
        sigx = x / self._gridkw - locx
        sigy = y / self._gridkh - locy
        return 'scah,scaw,sigx,sigy:',locx,locy,sigx,sigy

s = GridLable(twth = (90,90), gridwh = (3,3))
print s.create_label(xywh = (50,40,3,3))
