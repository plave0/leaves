'''Feature extraxtion (fe-ex)'''
import cv2
import numpy as np

def find_edge(image):
    edge = cv2.Canny(image, 300, 480)
    return edge

def thresh(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY_INV)
    return thresh

def calc_area(image):
    bw = thresh(image)
    return cv2.countNonZero(bw)

def calc_ciric(image):
    edge = find_edge(image)
    return cv2.countNonZero(edge)

def resize_image(image, factor):
    height, width = image.shape[:2]
    resized = cv2.resize(image, (round(factor*width), round(factor*height)), interpolation = cv2.INTER_CUBIC)
    return resized

def show_image(image, title = "img"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()