import json 
from pathlib import Path
import os.path

def save_res(factor,number_of_trees, precision,forest_name, dataset_name):
    '''Saves the testing restults to a json file.'''

    #Loads results
    path = Path('data/res.json')
    with open(path) as res_file:
        results = json.load(res_file)

    #Check if empty
    if results == {}:
        results = {'results':[]}

    #Appends new results and writes them to the file
    with open(path, 'w') as res_file:
        res = {'facotr':factor,
                'number of trees':number_of_trees,
                'precision': precision,
                'forest name':forest_name,
                'dataset name':dataset_name, 
                'comments':""}
        results['results'].append(res)
        json.dump(results, res_file, indent=4)

def load_res():
    path = Path('data/res.json')
    with open(path) as res_file:
        results = json.load(res_file)

    return results

def create_res_file():
    path = Path('data/res.json')
    if not os.path.isfile(path):
        with open(path, 'w+') as res_file:
            json_res = {'results':[]}
            json.dump(json_res,res_file,indent=4)
    else:
        print('Results file aready exits')
