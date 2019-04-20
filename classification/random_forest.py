import classification.decision_tree as dt
import pandas as pd
import random as rnd
import itertools
from collections import Counter
import os.path

DATASET_HEADERS = pd.read_csv(os.path.abspath(os.path.join(os.path.pardir, 'petnica-leaves\\sample_dataset.csv'))).columns

class Forest:
    '''Class that represents the random forest. Contains an array of decision trees.'''
    def __init__(self):
        self.trees = []

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


def generate_combinations(len, set_range):
    ''' Generates all posible number combinations of a given length and a given range.

    The paramer len defines the length of the generated arrays, 
    and the parameter range defines the maximum posible number that can appear in the arrays.'''
    
    combinations = itertools.combinations(range(set_range+1), len) #Generate combinations
    return combinations #Retuns all combinations

def get_subset(rows, columns = []):
    '''Get a subset of columns from a dataset.

    Parameter columns represents an array of integers. 
    This ints are indexes of columns in the original dataset
    that will be put in the new subset.'''

    sub_columns = [] #Empty array of columns
    for col in columns: 
        sub_columns.append(rows[[DATASET_HEADERS[col]]]) #Append defined columns to the sub_columns array
    sub_columns.append(rows[[DATASET_HEADERS[-1]]]) #Append the label column to the sub_columns array
    subset = pd.concat(sub_columns, axis=1) #Form a datafreme from all the extracted columns

    return subset #Return the dataframe

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

def build_forest(rows):
    '''Builds the forest. 

    Creates deciosion node classes and appentds
    them into an array defined int Forest class.'''
    forest = Forest() #Create an instance of a Forest
    btset, out = buil_bootstrapped_dataset(rows) #Create a bs dataset and an ob dataset
    combinations = generate_combinations(2, 2) #Create all posible combinations of numbers(rows)
    for comb in combinations: #For each cobination of columns
        subset = get_subset(btset, comb) #Generate the subset of columns from bs dataset
        tree = dt.build_tree(subset.values) #Build a decision tree form the subset
        forest.trees.append(tree) #Append it to the Forest object

    return forest #Return the Forest object

def print_forest(forest:Forest):
    '''Forest display'''
    for tree in forest.trees:
        dt.print_tree(tree)

