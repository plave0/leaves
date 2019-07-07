import classification.decision_tree as dt
import pandas as pd
import random as rnd
import itertools
from collections import Counter
import os.path
from pathlib import Path
import numpy as np

DATASET_HEADERS = pd.read_csv(Path(os.path.pardir, 'petnica-leaves/samples/sample_dataset.csv').absolute()).columns

class Forest:
    '''Class that represents the random forest. Contains an array of decision trees.'''
    def __init__(self):
        self.trees = []
        self.oob_error_estimates = []

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

def generate_combinations(len, set_range):
    ''' Generates all posible number combinations of a given length and a given range.

    The paramer len defines the length of the generated arrays, 
    and the parameter range defines the maximum posible number that can appear in the arrays.'''
    
    combinations = itertools.combinations(range(set_range+1), len) #Generate combinations
    return combinations #Retuns all combinations

def buil_bootstrapped_dataset(rows):
    '''Builds a bootstrapped dataset out of dateset passed as the parameter.

    It is built by taking random row from the original dataset and placing them in the bootstrapped dataset.
    The bootstrapped data set has the same number of rows as the original dataset.'''

    orig_dataset = rows.to_dict('indexed') # Covner the dataframe into a dict
    bootdata = {} #Create empty dict to store the randomly selected row from the original dataset
    out_of_bag_samples = {}

    # Creating bootstrapped dateset
    for i in range(len(orig_dataset)):
        #Chose a random int from 0 to the number of rows in the original dataset
        rand_index = rnd.randint(0, len(rows.index)-1) 
        #Takes a random row from the original dataset and places it into do bootstraped datset
        bootdata[i] = orig_dataset[rand_index] 

    #Creating "out of bag dataset"
    index = 0 # Counts next dict key
    for value in orig_dataset.values(): #Interates all values form the original dataset
        if value not in bootdata.values(): # Cheks if the value is in the bootstrapped dataset
            out_of_bag_samples[index] = value # If it is not, then the value is placed in the "out of bag" dataset
            index += 1

    df_bootstrapped = pd.DataFrame.from_dict(bootdata, orient='index') # Converts dict to pd.DataFrame
    df_out_of_bag = pd.DataFrame.from_dict(out_of_bag_samples, orient='index') # Converts dict to pd.DataFrame

    return df_bootstrapped, df_out_of_bag # Return the new datasets

def calc_num_on_trees(factor, num_of_cols):
    '''Calculate the number of trees to generate.'''

    #Calc the number of combinations
    num_of_trees = 1
    while factor<=num_of_cols:
        num_of_trees*=factor
        num_of_cols-=1
    
    num_of_trees*=num_of_cols
    return num_of_trees

def build_forest(rows, factor):
    '''Builds the forest. 

    Creates deciosion node classes and appentds
    them into an array defined int Forest class.'''
    forest = Forest() #Create an instance of a Forest
    num_of_trees = calc_num_on_trees(factor,len(rows.values[0])-1)
    for i in range(num_of_trees*2):
        btset, out = buil_bootstrapped_dataset(rows) #Create a bs dataset and an ob dataset
        tree = dt.build_tree(np.array(btset.values),factor,[]) #Build a decision tree form the subset

        #Find all predictions
        predictions = {}
        for row in out.values:
            label = row[-1] #Label
            tree_prediction = tree.check_row(row).keys() #Generate prediction

            #Mergig the predictions
            if label not in predictions.keys():
                predictions[label]=list(tree_prediction)
            else:
                for pred in list(tree_prediction):
                    predictions[label].append(pred)
            
        #Calculating oob error prediction
        for key in predictions.keys():
            freq_counter=Counter(predictions[key])
            most_freq = freq_counter.most_common(1)[0][0]
            forest.oob_error_estimates.append(int(key==most_freq))

        forest.trees.append(tree) #Append it to the Forest object

    return forest #Return the Forest object

def print_forest(forest:Forest):
    '''Forest display'''
    for tree in forest.trees:
        dt.print_tree(tree)

