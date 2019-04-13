import decision_tree as dt
import random_forest as rf
import pandas as pd

def main():
    '''Main program funcion'''
    data = pd.read_csv('sample_dataset.csv')
<<<<<<< HEAD
    tree = dt.build_tree(data)

=======
    
    tree = dt.build_tree(data.values)
    dt.print_tree(tree)
>>>>>>> parent of ff766b8... [edit] decision_tree.py

if __name__ == '__main__':
    main()
