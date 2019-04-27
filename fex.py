'''Feature extraxtion (fe-ex)'''
import cv2
import numpy as np

def find_edge(image):
    '''Returns the edge of a leaf.'''
    edge = cv2.Canny(image, 300, 480)
    return edge

def thresh(image):
    '''Returns thresholded image.'''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY_INV)
    return thresh

def calc_area(image):
    '''Returns the area of a leaf.'''
    bw = thresh(image)
    return cv2.countNonZero(bw)

def calc_ciric(image):
    '''Returns the circumference of the leaf.'''
    edge = find_edge(image)
    return cv2.countNonZero(edge)

def resize_image(image, factor):
    '''Returns the resized image.
    Parameter 'factor' represents the number with which the width and the height are multipied.'''
    height, width = image.shape[:2]
    resized = cv2.resize(image, (round(factor*width), round(factor*height)), interpolation = cv2.INTER_CUBIC)
    return resized

def show_image(image, title = "img"):
    '''Open window and show the image.'''
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()