class Case:
    '''
    A case for a switch statement.
    '''

    def __init__(self, condition, inflect, name, default=False):
        '''
        :condition: a boolean lambda function that takes a (lemma, inflection) pair as parameters
        :inflect: a lambda function that takes a lemma as a parameter and returns the inflected form
        :name: a name that describes the case
        :default: True iff the case is the default case of a switch statement
        '''
        # the set of lemmas that have been encountered during training that can be inflected by this case
        self.lemmas = set()
        self.condition = condition
        self.inflect = inflect
        self.name = name
        self.default = default

    def __str__(self):
        return self.name

    def apply(self, lemma, inflection, feats, train=False):
        if self.condition(lemma, inflection):
            if train:
                self.lemmas.add((lemma, feats)) # the lemma is a hit
            return self.inflect(lemma)
        else:
            return False # return False if the case does not apply