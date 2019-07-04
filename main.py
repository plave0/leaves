import classification.decision_tree as dt
import classification.random_forest as rf
import image.fex as f
import pandas as pd
import cv2
from pathlib import Path

def main():
    '''Main program funcion
    This is just a testing function'''
    path = str(Path('samples/sample_2.jpg'))
    img = cv2.imread(path, 1)
    #edge = fex.find_edge(img)
    cntimage, _ = f.find_encl(img)
    resized = f.resize_image(cntimage, 0.5)
    f.show_image(resized)

if __name__ == '__main__':
    main()
