import classification.decision_tree as dt

def serialize_forest(object):
    import classification.random_forest as rf
    if isinstance(object,rf.Forest):
        trees = []
        for tree in object.trees:
            trees.append(serialize_node(tree))
        
        return {'trees':trees,
        'error_estimates':object.oob_error_estimates,
        'factor':object.factor}

def serialize_question(object):
    if isinstance(object, dt.Question):
        return {'column': object.column, 'value': object.value}


def serialize_node(object):
    if isinstance(object, dt.Decision_Node):
        return {'question':serialize_question(object.question),
        'true_branch':serialize_node(object.true_branch),
        'false_branch':serialize_node(object.false_branch)}
    elif isinstance(object,dt.Leaf):
        return {'predictions': object.predictions}

def deserialize_forest(data):
    import classification.random_forest as rf
    forest = rf.Forest()
    forest.trees = []
    for tree in data['trees']:
        node = deserialize_node(tree)
        forest.trees.append(node)
    
    forest.oob_error_estimates=data['error_estimates']
    forest.factor = data['factor']
    return forest

        
def deserialize_node(tree):
    if next(iter(tree.keys()))=='question':
        node = dt.Decision_Node(deserialize_question(tree['question']),
        deserialize_node(tree['true_branch']),
        deserialize_node(tree['false_branch']))
        return node
    elif next(iter(tree.keys()))=='predictions':
        leaf = dt.Leaf(tree['predictions'])
        return leaf


def deserialize_question(question):
    question = dt.Question(question['column'],
    question['value'])
    return question