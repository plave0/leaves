import classification.random_forest as rf
import pandas as pd
from pathlib import Path
import os
import classification.serialization as s
import data_processing.recorder as r
import json

def main():
    '''Main program funcion
    This is just a testing function'''
    
    '''
    rows = pd.read_csv(Path(os.path.pardir, 'petnica-leaves/samples/dataset_3.csv').absolute())

    forest = rf.build_forest(rows,5)
    print(forest.calc_accu())

    json_forest = s.serialize_forest(forest)
    with open('forest.json', 'w') as f:
        json.dump(json_forest,f)
    '''
    r.save_res(4,50,78,"dataset_3")


if __name__ == '__main__':
    main()
