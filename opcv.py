import cv2
import os
import numpy as np

PATH = 'img'
SAMPLE = os.path.join(PATH,'sample.tif')

img = cv2.imread(SAMPLE)

def pos(event, x, y, flags, param) :
    if event == cv2.EVENT_LBUTTONDBLCLK :
        print(x,y)

cv2.namedWindow('sample')
cv2.setMouseCallback('sample', pos)

while True :
    cv2.imshow('sample', img)
    if cv2.waitKey(0) & 0xFF == 27:
        break

cv2.destroyAllWindows()