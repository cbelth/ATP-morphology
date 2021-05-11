from condition import Condition

class PhonologicalCondition(Condition):
    '''
    A subclass of a branching Condition, which determines whether an ending has one of a set of endings.
    '''
    def __init__(self, ending):
        self.ending = ending
        self.singleton = type(ending) is str
        if self.singleton:
            self.name = f'{ending}#'
        else:
            self.name = f"[{'|'.join(ending)}]#"
        super().__init__('Phonological')

    def applies(self, lemma, features):
        if self.singleton:
            return lemma.endswith(self.ending)
        else:
            return any(lemma.endswith(e) for e in self.ending)