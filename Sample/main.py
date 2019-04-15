import decision_tree as dt
import random_forest as rf
import pandas as pd

def main():
    '''Main program funcion'''
    data = pd.read_csv('sample_dataset.csv')
    rf.build_forest(data)

if __name__ == '__main__':
    main()
