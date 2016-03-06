import numpy as np
import cv2

img = cv2.imgload("set1.png", cv2.IMREAD_GRAYSCALE) # load in grayscale
cv2.imwrite('set1-grayscale.png', img)
