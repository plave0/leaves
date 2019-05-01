import classification.decision_tree as dt
import classification.random_forest as rf
import fex
import pandas as pd
import cv2

def main():
    '''Main program funcion
    This is just a testing function'''
    img = cv2.imread('samples\\sample_3.jpg', 1)
    #edge = fex.find_edge(img)
    thresh = fex.find_thresh(img)
    rect = fex.find_rect(img)
    hull,_ = fex.find_hull(img)
    resized_thr = fex.resize_image(thresh, 0.5)
    resized_rect = fex.resize_image(rect, 0.5)
    resized_hull = fex.resize_image(hull, 0.5)
    fex.show_image(resized_thr, 'sample')
    fex.show_image(resized_hull, 'sample')
    fex.show_image(resized_rect, 'sample')

if __name__ == '__main__':
    main()
