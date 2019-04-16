import decision_tree as dt
import random_forest as rf
import pandas as pd

def main():
    '''Main program funcion'''
    data = pd.read_csv('sample_dataset.csv')
    #print(data.values[1])
    forest = rf.build_forest(data)
    #rf.print_forest(forest)
    row = data.values[15]
    print(row)
    print(forest.check_row(row))

if __name__ == '__main__':
    main()
