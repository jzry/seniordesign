import cv2 as cv
import numpy as np
import sys
sys.path.append('../')
import Common_Methods as cm

"""
Function Brief: extracts the image according to the input parameters 
Parameters: 
    image  : Source scoresheet 
    x(int) : x-coordinates of the field
    y(int) : y-coordinates of the field 
    w(int) : Pixel width of the field
    h(int) : Pixel height of the field
Returns:
    image  : Cropped image of the scorefield
"""
def crop_field(image, x, y, w, h) :
    cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

image = cv.imread('template-image.jpg')
image = cm.resizeImageToScreen(image, 2.5, 1.5)

recovery_score = crop_field(image, 500*2.5, 700*1.5, 100*2.5, 25*1.5)

cv.imshow('Recovery Score', recovery_score)
cv.waitKey(0)
cv.destroyAllWindows()