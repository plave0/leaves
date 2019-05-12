import classification.decision_tree as dt
import classification.random_forest as rf
import image.fex as f
import pandas as pd
import cv2

def main():
    '''Main program funcion
    This is just a testing function'''
    img = cv2.imread('samples\\sample_1.jpg', 1)
    #edge = fex.find_edge(img)
    cntimage,_ = f.find_cnt(img)
    resized = f.resize_image(cntimage, 0.5)
    f.show_image(resized)

if __name__ == '__main__':
    main()
