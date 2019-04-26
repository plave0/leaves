'''Feature extraxtion (fe-ex)'''
import cv2
import numpy as np

def find_edge(image):
    edge = cv2.Canny(image, 300, 480)
    return edge

def resize_image(image, factor):
    height, width = image.shape[:2]
    resized = cv2.resize(image, (round(factor*width), round(factor*height)), interpolation = cv2.INTER_CUBIC)
    return resized

def show_image(image, title = "img"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()