import json 

def save_res(factor,number_of_trees, precision,forest_name, dataset_name):
    '''Saves the testing restults to a json file.'''

    #Loads results
    with open('res.json') as res_file:
        results = json.load(res_file)

    #Check if empty
    if results == {}:
        results = {'results':[]}

    #Appends new results and writes them to the file
    with open('res.json', 'w') as res_file:
        res = {'facotr':factor,
                'number of trees':number_of_trees,
                'precision': precision,
                'forest name':forest_name,
                'dataset name':dataset_name, 
                'comments':""}
        results['results'].append(res)
        json.dump(results, res_file)