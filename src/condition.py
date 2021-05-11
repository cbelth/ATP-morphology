class Condition:
    '''
    A super class to represent a branch condition in a decision tree.
    '''
    def __init__(self, condition_type):
        self.condition_type = condition_type

    def __str__(self):
        return self.name