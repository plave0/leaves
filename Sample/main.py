import decision_tree as dt

DATA_SET = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]

def main():
    '''Main program funcion'''
    tree = dt.build_tree(DATA_SET)
    dt.print_tree(tree)

if __name__ == '__main__':
    main()
