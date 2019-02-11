import decision_tree as dt
import pandas as pd

def main():
    '''Main program funcion'''
    data = pd.read_csv('sample_dataset.csv')
    
    tree = dt.build_tree(data.values)
    dt.print_tree(tree)

if __name__ == '__main__':
    main()
