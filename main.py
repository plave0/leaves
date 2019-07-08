import classification.decision_tree as dt
import classification.random_forest as rf
import image_processing.fex as f
import image_processing.calc as c
import pandas as pd
import cv2
from pathlib import Path
import os

def main():
    '''Main program funcion
    This is just a testing function'''
    path = str(Path('samples/sample_2.jpg'))
    img = cv2.imread(path, 1)

    rows = pd.read_csv(Path(os.path.pardir, 'petnica-leaves/samples/sample_dataset.csv').absolute())
    forest = rf.build_forest(rows,2)
    #rf.print_forest(forest)
    row = rows.values[0]
    print(forest.calc_accu())
    #print(forest.check_row(row))
    

if __name__ == '__main__':
    main()
