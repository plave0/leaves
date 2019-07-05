import classification.decision_tree as dt
import classification.random_forest as rf
import image_processing.fex as f
import image_processing.calc as c
import pandas as pd
import cv2
from pathlib import Path

def main():
    '''Main program funcion
    This is just a testing function'''
    path = str(Path('samples/sample_1.jpg'))
    img = cv2.imread(path, 1)
    #edge = fex.find_edge(img)

    c.calc_leaf_circumference(img)
    

if __name__ == '__main__':
    main()
