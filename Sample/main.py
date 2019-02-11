import decision_tree as dt
import pandas as pd

def main():
    '''Main program funcion'''
    data = pd.read_csv('sample_dataset.csv')
    
    tree = dt.build_tree(data.values)
    #dt.print_tree(tree)
    print(data.values[3])
    print(tree.check_row(data.values[3]))

if __name__ == '__main__':
    main()
