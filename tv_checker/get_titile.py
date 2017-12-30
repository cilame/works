import cv2
import os

if not os.path.isdir('pict'):
    os.mkdir('pict')

for i in range(1,3001):
    p = 'pic/'+str(i)+'.png'
    t = 'pict/'+str(i)+'.png'
    s = cv2.imread(p)
    cv2.imwrite(t,s[200:360,430:640])
    print(i)
    

