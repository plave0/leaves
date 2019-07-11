import classification.decision_tree as dt
import pandas as pd
import itertools
from collections import Counter
import os.path
from pathlib import Path
import numpy as np
from multiprocessing import Process,Manager,Queue
import data_processing.configuration as config
import data_processing.serialization as s
import json
import data_processing.recorder as r
import random

class Forest:
    '''Class that represents the random forest. Contains an array of decision trees.'''
    def __init__(self):
        self.trees = []
        self.oob_error_estimates = []
        self.factor = 0

    def check_row(self, row):
        '''Classifies the given row.
        Returns predictions'''

        predictions = [] #Emty array of predicions
        for tree in self.trees: #Iterate through evry tree in the forest
            tree_prediction = tree.check_row(row).keys() #Get predictions (return more thad one prediction)
            for prediction in tree_prediction:
                predictions.append(prediction) #Separate the predictions and add them to the array

        freq_counter=Counter(predictions)
        return predictions, freq_counter.most_common(1)[0][0] #Returns the array of all predictions and the most frequent prediction

    def calc_accu(self):
         return np.mean(np.array(self.oob_error_estimates))*100

def buil_bootstrapped_dataset(rows):
    '''Builds a bootstrapped dataset out of dateset passed as the parameter.

    It is built by taking random row from the original dataset and placing them in the bootstrapped dataset.
    The bootstrapped data set has the same number of rows as the original dataset.'''

    #Create bootstrapped dataset (type = pd.Dataframe)
    df_bootstrapped = rows.sample(n=len(rows.values),replace=True, random_state=random.randint(1,101))

    #Create out of bag dataset (tyep = pd.Dataframe)
    diff_df = pd.merge(rows, df_bootstrapped, how='outer', indicator='Exist')
    diff_df = diff_df.loc[diff_df['Exist'] != 'both']
    diff_df.drop(labels='Exist', axis=1,inplace=True)
    
    
    return df_bootstrapped, diff_df # Return the new datasets


def build_forest(forest_name):
    '''Starts the processes that create the trees of the forest.'''

    ######################################################################
    def build(outputt, rowss, factorr):
        '''Build a tree and calculates it's out of bag error estimate.
        It return the tree and the error estimate through the outputt parameter.'''
        
        #Creating the tree
        btset, out = buil_bootstrapped_dataset(rowss)
        tree = dt.build_tree(np.array(btset.values),factorr,[])

        #Find all predictions
        predictions = {}
        for row in out.values:
            label = row[-1] #Label
            tree_prediction = tree.check_row(row) #Generate prediction

            #Mergig the predictions
            if label not in predictions.keys():
                predictions[label]=[]
            for key,value in tree_prediction.items():
                for _ in range(value):
                    predictions[label].append(key)


        error_estimates = []
        #Calculating oob error estimate
        for key in predictions.keys():
            freq_counter=Counter(predictions[key])
            predictions[key] = freq_counter.most_common(1)[0][0]
            error_estimates.append(int(key==predictions[key]))

        outputt.put((tree,error_estimates))
    ######################################################################  

    configuration = config.load_config()
    rows = pd.read_csv(Path('data/datasets',configuration['dataset']))

    #Create the forest
    forest = Forest()
    forest.factor = configuration['factor']

    #Starting the processes
    output = Queue() #Queue that will be used to store the outputs of all the processes
    for i in range(int(configuration['number_of_trees']/configuration['cores_to_use'])): 
        threads = []
        for _ in range(int(configuration['cores_to_use'])):
            t = Process(target=build, args=(output,rows,forest.factor))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        #Geting the results and putting them in the forest object
        for _ in threads:
            result = output.get()
            forest.trees.append(result[0])
            for ee in result[1]:
                forest.oob_error_estimates.append(ee)

    save_forest(forest,forest_name,configuration['dataset'])    

def print_forest(forest:Forest):
    '''Forest display'''
    for tree in forest.trees:
        dt.print_tree(tree)

def save_forest(forest,forest_name,dataset):
    '''Saves the builts forest.'''
    json_tree = s.serialize_forest(forest)
    with open(Path('data/forests/'+forest_name+'.json'),'w+') as forest_file:
        json.dump(json_tree,forest_file,indent=4)

    r.save_res(forest.factor,
                len(forest.trees),
                forest.calc_accu(),
                forest_name,
                dataset)

