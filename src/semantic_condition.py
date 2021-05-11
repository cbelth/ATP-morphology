from condition import Condition

class SemanticCondition(Condition):
    '''
    A subclass of a branching Condition, which determines whether an ending has a particular semantic feature.
    '''
    def __init__(self, feature):
        self.feature = feature
        self.name = feature
        super().__init__('Semantic')

    def applies(self, lemma, features):
        return self.feature in features