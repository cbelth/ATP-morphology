from utils import tolerance_principle
from case import Case

class TPSwitchStatement:
    '''
    A class that represents a Tolerance Principle (TP) switch (case) statement. 
    In linguistics, this is known as the Elsewhere Condition.
    Each leaf in an ATP decision tree contains a such a switch statement, which allows it to inflect words.
    If the leaf contains a productive suffix, it will be the default case and will apply to any lemma that reaches the leaf.
    '''
    def __init__(self, apply_phonology=False, pairs=None):
        '''
        :pairs: if provided, it trains automatically.
        '''
        self.vocab = set()
        self.productive = False
        self.apply_phonology = apply_phonology
        if apply_phonology:
            # treats the various alomorphs for English /-d/ and /-z/ as identical.
            # This was only used in the developmental experiment in Fig. 1 of the paper, to keep it from getting cluttered.
            from phon_engine import PhonEngine
            self.phon_engine = PhonEngine()

        self.cases = list()
        self.default_case = Case(condition=lambda lemma, inflection: True, # the default case applies to everything
                                 inflect=lambda lemma: lemma, # the default case just regurgitates the lemma
                                 name='default-default')

        if pairs:
            self.train(pairs)

    def train(self, pairs):
        '''
        :pairs: pairs to train on
        '''
        for lemma, inflected, feats in pairs:
            self.vocab.add((lemma, inflected, feats))
            self.train_on_pair(lemma, inflected, feats)

    def train_on_pair(self, lemma, inflected, feats):
        '''
        :lemma: the lemma to train on
        :inflected: the inflected form to train on
        :feats: the relevant features
        '''
        # no need to do anything if we already have this case
        cases = list(self.cases)
        if self.default_case.name != 'default-default':
            cases.append(self.default_case)
        for case in cases:
            res = case.apply(lemma, inflected, feats, train=True)
            if res:
                if case != self.default_case:
                    # bring the case to beginning of the switch statement
                    self.cases.insert(0, self.cases.pop(self.cases.index(case)))
                return
        # if no case applied, the default will, but we are training so that doesn't matter
        # instead, add a new case for this pair
        new_case = self.build_new_case(lemma, inflected)
        if new_case:
            new_case.apply(lemma, inflected, feats, train=True)
            self.cases.append(new_case)

    def apply_suffix(self, lemma, suffix):
        '''
        :return: the suffix concatenated to the lemma, but with the relevant phonology applied if self.apply_phonology == True
        '''
        return f'{lemma}{suffix}' if not self.apply_phonology else self.phon_engine.apply_suffix(lemma, suffix)

    def build_new_case(self, lemma, inflection):
        '''
        :return: a new Case for the switch statement to explain this particular :inflection:
        '''
        suffix = inflection[len(lemma):]
        if inflection.startswith(lemma) and inflection == self.apply_suffix(lemma, suffix):
            return Case(condition=lambda _lemma, _inflection: _inflection == self.apply_suffix(_lemma, suffix), # this case applies when the inflection starts with the lemma
                        inflect=lambda _lemma: self.apply_suffix(_lemma, suffix), # the case returns the lemma with this particular inflection's suffix
                        name=f'inflected = lemma + {suffix}')
        x, y = f'{lemma}', f'{inflection}'
        return Case(condition=lambda _lemma, _inflection: (_lemma, _inflection) == (x, y), # this case applies only for this exact (lemma, inflection pair)
                    inflect=lambda _lemma: inflection, # the case memorizes the inflection
                    name=f'inflected = {inflection}')

    def memorized(self, lemma, feats):
        '''
        :lemma: a lemma
        :feats: the lemma's features

        :return: True if the lemma has been memorized, False otherwise
        '''
        # search over cases in switch statement for the lemma's inflection
        for case in self.cases:
            if (lemma, feats) in case.lemmas:
                return True
        return False

    def inflect(self, lemma, feats):
        '''
        Inflect a lemma.

        Note: We assume that the inflection that we are searching for is unambiguous.

        :lemma: a lemma to inflect
        :feats: the features of the lemma to inflect
        '''
        # search over cases in switch statement for the lemma's inflection
        for case in self.cases:
            if (lemma, feats) in case.lemmas:
                return case.inflect(lemma)
        # if the lemma is not found in any case, then apply the default case
        return self.default_case.inflect(lemma)

    def get_case(self, lemma, feats):
        '''
        Get the case that inflects this lemma.

        :lemma: a lemma to inflect
        :feats: the features of the lemma to inflect
        '''
        # search over cases in switch statement for the lemma's inflection
        for case in self.cases:
            if (lemma, feats) in case.lemmas:
                return case
        # if the lemma is not found in any case, then return the default case
        return self.default_case

    def get_productive(self):
        '''
        Get the cases from the switch statement that pass the TP. 
        There should only be one, but if some odd edge case leads to more than one, return the best (highest c / n) 
        '''
        self.productive = False
        productive = list()
        n = len(self.vocab)
        cases = list(self.cases)
        if self.default_case.name != 'default-default': # the default-default case is a place-holder that just regurgitates the lemma, but is not productive
            cases.append(self.default_case)
        for case in cases:
            c = len(case.lemmas)
            if tolerance_principle(n=n, c=c):
                self.productive = True
                productive.append(case)
        if len(productive) == 0:
            return None
        if len(productive) == 1:
            return productive[0]
        return sorted(productive, key=lambda case: len(case.lemmas), reverse=True)[0]

    def get_closest_to_productive(self):
        '''
        Get the case that is the closest to pasing the TP.
        '''
        closest = None
        closest_val = 0
        for case in self.cases:
            c = len(case.lemmas)
            if not closest or c > closest_val:
                closest = case
                closest_val = c
        return closest

