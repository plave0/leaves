
class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, data):
        val = data[self.column]
        if is_numeric(val):
            return val >= self.value
        else: 
            return val == self.value

    def __repr__(self):
        return "Column: %s Value: %s" % (self.column, self.value)

def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)