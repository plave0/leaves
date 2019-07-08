import classification.decision_tree as dt
import classification.random_forest as rf
import image_processing.fex as f
import image_processing.calc as c
import data_processing.dataset as d
import pandas as pd
import cv2
from pathlib import Path
import os

def main():
    '''Main program funcion
    This is just a testing function'''
    path = str(Path('samples/2283.jpg'))
    img = cv2.imread(path, 1)

    #f.test_fex(img)
    c.calc_all(img)

    #rows = pd.read_csv(Path(os.path.pardir, 'petnica-leaves/samples/sample_dataset.csv').absolute())
    #forest = rf.build_forest(rows,2)
    #rf.print_forest(forest)
    #row = rows.values[0]
    #print(forest.calc_accu())
    #print(forest.check_row(row))
    #d.create_dataset()
    

if __name__ == '__main__':
    main()
