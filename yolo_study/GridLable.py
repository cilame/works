import numpy as np

class GridLable:
    def __init__(self,*args,**kw):
        '''
        **kw:
            twth:   a tuple(tw, th)
                true width and true height
            gridwh: a tuple(gridw, gridh)
                grid
        '''
        self._tw,self._th = map(float,kw.get('twth'))
        self._gridw,self._gridh = map(float,kw.get('gridwh'))
        self._gridkw = self._tw / self._gridw
        self._gridkh = self._th / self._gridh
        
    def _create_grid(self):
        y, x = np.mgrid[:self._gridh,:self._gridw]
        indx = np.concatenate((y[...,None],x[...,None]),axis=-1)
        return indx
        
    def _get_index(self,x,y):
        sh = np.arange(0,self._th,self._th/self._gridh)
        sw = np.arange(0,self._tw,self._tw/self._gridw)
        h = max(np.where(sh<y)[0])
        w = max(np.where(sw<x)[0])
        return h,w

    def _test_create_label(self, xywh):
        x,y,w,h = map(float, xywh)
        locy,locx = self._get_index(x,y)
        sigx = x / self._gridkw - locx
        sigy = y / self._gridkh - locy
        return 'scah,scaw,sigx,sigy:',locx,locy,sigx,sigy

    def _create_sig(self, xywh):
        x,y,w,h = map(float, xywh)
        locy,locx = self._get_index(x,y)
        sigx = x / self._gridkw - locx
        sigy = y / self._gridkh - locy
        return locx,locy,sigx,sigy

    # test other zero
    def create_label(self, xywh):
        locx,locy,sigx,sigy = self._create_sig(xywh)
        indx = self._create_grid()
        new_indx = indx + [sigy,sigx]
        mask = np.zeros(new_indx.shape)
        mask[locy,locx] = new_indx[locy,locx]
        return mask,locy,locx

        
if __name__ == "__main__":
    # cur test
    s = GridLable(twth = (90,90), gridwh = (3,3))
    print s.create_label((15, 59, 30, 30))#yxhw
    
