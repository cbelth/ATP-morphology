import unittest
import sys
sys.path.append('../src/')
from utils import load_pairs, most_freq, load_word_to_ipa

class TestUtils(unittest.TestCase):
    def test_load_pairs_1(self):
        pairs, features = load_pairs('../data/german/quant/train60_0.txt')
        assert(len(pairs) == 60)
        assert(features == {'N', 'M', 'F'})
        assert(pairs[0] == ('Sache', 'Sachen', ('F',)))
        assert(pairs[-1] == ('Kegel', 'Kegel', ('M',)))

    def test_load_pairs_2(self):
        pairs, features = load_pairs('../data/german/growth/train100_0.txt')
        assert(len(pairs) == 100)
        assert(features == {'N', 'M', 'F'})
        assert(pairs[0] == ('Sache', 'Sachen', ('F',)))
        assert(pairs[-1] == ('Samen', 'Samen', ('M',)))

    def test_load_pairs_3(self):
        pairs, features = load_pairs('../data/english/quant/unimorph_celex0_train100_0.txt')
        assert(len(pairs) == 100)
        assert(features == {'V', 'PST'})
        assert(pairs[0] == ('hæv', 'hæd', ('V', 'PST')))
        assert(pairs[-1] == ('ʤɔɪn', 'ʤɔɪnd', ('V', 'PST')))

    def test_load_pairs_4(self):
        pairs, features = load_pairs('../data/english/growth/child-0/100.txt', sep=' ')
        assert(len(pairs) == 100)
        assert(features == {'V', 'PST', 'PL', 'V.PTCP', 'PRS'})
        assert(pairs[0] == ('pretend', 'pretending', ('V', 'V.PTCP', 'PRS'))) # conversion to IPA happens later
        assert(pairs[-1] == ('eat', 'ate', ('V', 'PST')))

    def test_load_pairs_5(self):
        pairs, features = load_pairs('../data/german/CHILDES-DE.txt', feat_sep=',', skip_header=True) 
        assert(features == {'C', 'N', 'F', 'M', 'RFS', 'Mono-N'}) # these features aren't actually used in the experiments
        assert(pairs[85] == ('Armel', 'Armel', ('C', 'M', 'RFS'))) # check that umlauts were removed

    def test_load_pairs_6(self):
        # convert to IPA
        word_to_ipa = load_word_to_ipa()
        pairs, features = load_pairs('../data/english/growth/child-0/100.txt', sep=' ', preprocessing=lambda s: word_to_ipa[s])
        assert(len(pairs) == 100)
        assert(features == {'V', 'PST', 'PL', 'V.PTCP', 'PRS'})
        assert(pairs[0] == ('pritɛnd', 'pritɛndɪŋ', ('V', 'V.PTCP', 'PRS')))
        assert(pairs[-1] == ('it', 'eɪt', ('V', 'PST')))

    def test_most_freq_1(self):
        assert(most_freq([1, 2, 1, 3, 4, 1, 1]) == 1)

    def test_most_freq_2(self):
        assert(most_freq([3, 2, 1, 3, 4, 1, 1]) == 1)

    def test_most_freq_3(self):
        assert(most_freq([3]) == 3)

    def test_most_freq_4(self):
        assert(most_freq([1, 2]) == 1)

    def test_most_freq_5(self):
        assert(most_freq(['a', 'b', 'b', 'c']) == 'b')

if __name__ == "__main__":
    unittest.main()