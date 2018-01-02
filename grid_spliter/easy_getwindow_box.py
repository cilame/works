import cv2
import numpy as np
import easy_getscreen

def drawMouse(event,x,y,flags,param):
    color = (0,0,0)
    global xx,yy,nx,ny,ex,ey,tog,tog2
    if flags == cv2.EVENT_FLAG_LBUTTON:
        img[ny:y,nx:x] = 0
        tog = True
    else:
        if tog == True:
            tog2 = True
            ex,ey = x,y
        else:
            nx,ny = x,y
    xx,yy = x,y

img = easy_getscreen.get_window_abs_by_name('MineSweeper')
o_img = img.copy()
cv2.imshow('img',img)
cv2.setMouseCallback('img',drawMouse)
tog = False
tog2 = False

print 's means save, c means close, space means clear.'
while True:
    key = cv2.waitKey(10)
    cv2.imshow('img',img)
    if key == ord(' '):
        img = np.ones((300,300,3))*255
    if key == ord('s'):
        cv2.imwrite('output.jpg',img)
    if key == ord('c'):
        break
    if tog2:
        break

y,x = img.shape[:2]
ex = ex-x
ey = ey-y
print nx,ny,ex,ey
cv2.destroyAllWindows()
cv2.imshow('img', o_img[ny:ey,nx:ex])
cv2.waitKey()
cv2.destroyAllWindows()
