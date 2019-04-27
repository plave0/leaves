import classification.decision_tree as dt
import classification.random_forest as rf
import fex
import pandas as pd
import cv2

def main():
    '''Main program funcion
    This is just a testing function'''
    img = cv2.imread('samples\\sample.jpg', 1)
    #edge = fex.find_edge(img)
    thresh = fex.thresh(img)
    resized = fex.resize_image(thresh, 0.5)
    print(fex.calc_area(thresh))
    print(fex.calc_area(resized))
    fex.show_image(resized, 'sample')

if __name__ == '__main__':
    main()
