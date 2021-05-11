import ipapy

class PhonEngine:
    '''
    A class that mocks an English phonology so that the various alomorphs for English /-d/ and /-z/ and be treated as identical.

    This is only used in the developmental experiment in Fig. 1 of the paper, to keep it from getting cluttered.
    '''
    def __init__(self):
        pass

    def enforce_voicing(self, lemma, suffix):
        '''
        Make sure that the lemma and suffix match in voicing.
        '''
        if suffix == '':
            return lemma
        interfacing_letter = suffix[0]
        ipa_suffix = ipapy.UNICODE_TO_IPA[interfacing_letter]
        if ipa_suffix.is_vowel:
            return f'{lemma}{suffix}'

        assert(suffix in {'s', 'z', 'd', 't'})

        # ignore any diacritics
        last_char_index = -1
        last_char = lemma[-1]
        while not ipapy.UNICODE_TO_IPA[last_char].is_consonant and not ipapy.UNICODE_TO_IPA[last_char].is_vowel:
            last_char_index -= 1
            last_char = lemma[last_char_index]

        # get lemma voicing
        lemma_voicing = ipapy.UNICODE_TO_IPA[last_char].is_vowel or ipapy.UNICODE_TO_IPA[last_char].voicing == 'voiced'
        # get suffix voicing
        suffix_voicing = ipa_suffix.voicing == 'voiced'

        if lemma_voicing == suffix_voicing:
            return f'{lemma}{suffix}'
        
        if suffix == 's':
            new_suffix = 'z'
        elif suffix == 'z':
            new_suffix = 's'
        elif suffix == 't':
            new_suffix = 'd'
        elif suffix == 'd':
            new_suffix = 't'
        for i in range(1, len(suffix)):
            new_suffix += suffix[i] 
        return f'{lemma}{new_suffix}'

    def enforce_vowel(self, inflected):
        '''
        Insert [ɪ] where necessary.
        '''
        if len(inflected) < 2:
            return inflected
        second_to_last = ipapy.UNICODE_TO_IPA[inflected[-2]]
        last = ipapy.UNICODE_TO_IPA[inflected[-1]]
        if second_to_last.is_vowel or last.is_vowel:
            return inflected

        def is_sibilant(ipa_char):
            return ipa_char.is_consonant and 'sibilant' in ipa_char.manner

        if is_sibilant(second_to_last) and inflected[-1] in {'s', 'z'}:
            return f'{inflected[:-1]}ɪz'

        if inflected[-2] in {'t', 'd'} and inflected[-1] in {'t', 'd'}:
            return f'{inflected[:-1]}ɪd'
        return inflected

    def apply_suffix(self, lemma, suffix):
        '''
        Carries out a suffixation as the composition of morphological and phonological processes.
        '''
        res = self.enforce_voicing(lemma, suffix)
        res = self.enforce_vowel(res)
        return res