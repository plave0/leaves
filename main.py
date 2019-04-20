import classification.decision_tree as dt
import classification.random_forest as rf
import pandas as pd

def main():
    '''Main program funcion
    This is just a testing function'''
    
    data = pd.read_csv('sample_dataset.csv')
    #print(data.values[1])
    forest = rf.build_forest(data)
    #rf.print_forest(forest)
    row = data.values[15]
    print(row)
    print(forest.check_row(row))

if __name__ == '__main__':
    main()
