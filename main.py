import classification.decision_tree as dt
import classification.random_forest as rf
import fex
import pandas as pd
import cv2

def main():
    '''Main program funcion
    This is just a testing function'''
    img = cv2.imread('samples\\sample.jpg', 1)
    fex.show_image(img, 'sample')

if __name__ == '__main__':
    main()
