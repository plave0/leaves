import classification.decision_tree as dt
import classification.random_forest as rf
import image_processing.fex as f
import image_processing.calc as c
import data_processing.dataset as d
import pandas as pd
import cv2
from pathlib import Path
import os
import cProfile, pstats, io

def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner

@profile
def main():
    '''Main program funcion
    This is just a testing function'''

    rows = pd.read_csv(Path(os.path.pardir, 'petnica-leaves/samples/sample_dataset.csv').absolute())
    forest = rf.build_forest(rows,2)
    #rf.print_forest(forest)
    #row = rows.values[0]
    print(forest.calc_accu())
    #print(forest.check_row(row))
    #d.create_dataset()


    

if __name__ == '__main__':
    main()
