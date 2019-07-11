import pandas as pd
import os.path
from pathlib import Path
import random
import numpy as np
import json
import fastnumbers as fn
import math

DATASET_HEADERS= ['color','diameter','wight','label']

class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, data):
        val = data[self.column]
        if isinstance(val, int) or isinstance(val,float):
            return val >= self.value
        else: 
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if fn.isfloat(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            DATASET_HEADERS[self.column], condition, str(self.value))


class Leaf:
    """A Leaf node classifies data.

    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """

    def __init__(self, rows):
        if isinstance(rows, dict):
            self.predictions = rows
        else:
            self.predictions = class_counts(rows)


class Decision_Node:
    """A Decision Node asks a question.

    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

    def check_row(self, row):
        res = self.question.match(row)

        if res:
            if not isinstance(self.true_branch, Leaf):
                return self.true_branch.check_row(row)
            else:
                return self.true_branch.predictions
        else:
            if not isinstance(self.false_branch, Leaf):
                return self.false_branch.check_row(row)
            else:
                return self.false_branch.predictions

def class_counts(data):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in data:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def partition(rows, question):
    """Partitions a dataset.

    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

def gini(data):
    '''Calculate the Gini Impurity for a list of rows.'''
    counts = class_counts(data)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(data))
        impurity -= math.pow(prob_of_lbl,2)
    return impurity


def info_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

def find_best_split(rows,factor,num_of_columns, used_columns):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = [i for i in range(0,num_of_columns) if i not in used_columns] # number of columns

    if len(n_features)>factor:
        n_features = random.sample(n_features, factor)

    for col in n_features:  # for each feature

        values = set([row[col] for row in rows])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the dataset
            true_rows, false_rows = partition(rows, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question
            
    
def build_tree(rows, factor ,used_columns=[]):
    """Builds the tree.
    Rules of recursion: 1) Believe that it works. 2) Start by checking
    for the base case (no further information gain). 3) Prepare for
    giant stack traces.
    """
    
    # Try partitioing the dataset on each of the unique attribute,
    # calculate the information gain,
    # and return the question that produces the highest gain.
    num_of_columns = len(rows[0])-1
    gain, question = find_best_split(rows,factor,num_of_columns,used_columns)

    if question != None:
        used_columns.append(question.column)

    # Base case: no further info gain
    # Since we can ask no further questions,
    # we'll return a leaf.
    if gain == 0:
        return Leaf(rows)

    # If we reach here, we have found a useful feature / value
    # to partition on.
    true_rows, false_rows = partition(rows, question)

    # Recursively build the true branch.
    true_branch = build_tree(true_rows,factor, used_columns)

    # Recursively build the false branch.
    false_branch = build_tree(false_rows,factor, used_columns)

    # Return a Question node.
    # This records the best feature / value to ask at this point,
    # as well as the branches to follow
    # dependingo on the answer.
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=" "):
    """World's most elegant tree printing function."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print (spacing + str(node.question))

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")
