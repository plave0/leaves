import decision_tree as dt
import pandas as pd

def main():
    '''Main program funcion'''
    data = pd.read_csv('sample_dataset.csv')
    
    tree = dt.build_tree(data.values)
    #dt.print_tree(tree)
    #print(data.values)
    #print(data.values[15])
    #prediction = tree.check_row(data.values[15]).keys()
    
    #for key in prediction:
       # print(key)

if __name__ == '__main__':
    main()
