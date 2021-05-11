import unittest
import sys
sys.path.append('../src/')
from tp_switch_statement import TPSwitchStatement

class TestTPSwitchStatement(unittest.TestCase):
    def test_init(self):
        tp = TPSwitchStatement()

    def test_default_case_1(self):
        tp = TPSwitchStatement()
        assert(tp.default_case.inflect('hit') == 'hit')

    def test_train_on_pair_1(self):
        tp = TPSwitchStatement(apply_phonology=True)
        assert(len(tp.cases) == 0)
        tp.train_on_pair('wɔk', 'wɔkt', 'tense=PST')
        assert(len(tp.cases) == 1)
        assert(tp.cases[0].lemmas == {('wɔk', 'tense=PST')})
        assert(tp.inflect('wɔk', 'tense=PST') == 'wɔkt')
        tp.train_on_pair('sprɪnt', 'sprɪntɪd', 'tense=PST')
        assert(len(tp.cases) == 1)
        assert(tp.inflect('sprɪnt', 'tense=PST') == 'sprɪntɪd')

    def test_train_on_pair_2(self):
        tp = TPSwitchStatement(apply_phonology=True)
        assert(len(tp.cases) == 0)
        tp.train_on_pair('pleɪ', 'pleɪd', 'tense=PST')
        assert(len(tp.cases) == 1)
        assert(tp.inflect('pleɪ', 'tense=PST') == 'pleɪd')
        tp.train_on_pair('wɔk', 'wɔkt', 'tense=PST')
        assert(len(tp.cases) == 1)
        assert(tp.inflect('wɔk', 'tense=PST') == 'wɔkt')

    def test_train_on_pair_3(self):
        '''
        Getting unlucky with an /ɪd/ before a /t/ or /d/
        '''
        tp = TPSwitchStatement()
        assert(len(tp.cases) == 0)
        tp.train_on_pair('peɪnt', 'peɪntɪd', 'tense=PST')
        assert(len(tp.cases) == 1)
        assert(tp.cases[0].lemmas == {('peɪnt', 'tense=PST')})
        assert(tp.inflect('peɪnt', 'tense=PST') == 'peɪntɪd')
        tp.train_on_pair('oʊpən', 'oʊpənd', 'tense=PST')
        assert(len(tp.cases) == 2)
        assert(tp.inflect('oʊpən', 'tense=PST') == 'oʊpənd')

    def test_train_on_pair_4(self):
        '''
        Getting unlucky with an /ɪd/ before a /t/ or /d/
        '''
        tp = TPSwitchStatement()
        assert(len(tp.cases) == 0)
        tp.train_on_pair('baby', 'babys', 'gender=F')
        assert(len(tp.cases) == 1)
        tp.train_on_pair('tunnel', 'tunnels', 'gender=F')
        assert(len(tp.cases) == 1)

    def test_build_new_case_1(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'lay', 'laid'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'tidy', 'tidied'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'qualify', 'qualified'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'hurry', 'hurried'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'dry', 'dried'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'dirty', 'dirtied'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'try', 'tried'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'bury', 'buried'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'spy', 'spied'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'fry', 'fried'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'petrify', 'petrified'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'cry', 'cried'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'fancy', 'fancied'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'carry', 'carried'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'marry', 'married'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'pay', 'paid'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'satisfy', 'satisfied'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)

    def test_build_new_case_2(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'bend', 'bent'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'lose', 'lost'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'spell', 'spelt'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'spend', 'spent'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'build', 'built'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'send', 'sent'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)

    def test_build_new_case_3(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'swing', 'swang'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'spit', 'spat'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'sit', 'sat'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)

    def test_build_new_case_4(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'sting', 'stung'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'fling', 'flung'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'stick', 'stuck'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)

    def test_build_new_case_5(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'shoot', 'shot'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'meet', 'met'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'feed', 'fed'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)

    def test_build_new_case_6(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'hide', 'hid'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'bite', 'bit'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        lemma, inflection = 'slide', 'slid'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)

    def test_build_new_case_7(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'lemma_nonword', 'inflected_nonword'
        case = tp.build_new_case(lemma, inflection)
        assert(case.inflect(lemma) == inflection)
        assert(case.inflect('diff_lemma_nonword') == inflection)

    def test_build_new_case_8(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'walk', 'walked'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        lemma, inflection = 'lay', 'laid'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        lemma, inflection = 'shoot', 'shot'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        assert(len(tp.cases) == 3)

    def test_build_new_case_9(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'lay', 'laid'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        lemma, inflection = 'crunch', 'crunched'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        assert(len(tp.cases) == 2)
        assert(tp.inflect('lay', 'tense=PST') == 'laid')
        assert(tp.inflect('crunch', 'tense=PST') == 'crunched')

    def test_build_new_case_10(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'lay', 'laid'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        lemma, inflection = 'tidy', 'tidied'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        assert(len(tp.cases) == 2)
        assert(tp.inflect('lay', 'tense=PST') == 'laid')
        assert(tp.inflect('tidy', 'tense=PST') == 'tidied')

    def test_build_new_case_11(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'crunch', 'crunched'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        lemma, inflection = 'nudge', 'nudged'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        assert(len(tp.cases) == 2)
        assert(tp.inflect('crunch', 'tense=PST') == 'crunched')
        assert(tp.inflect('nudge', 'tense=PST') == 'nudged')

    def test_build_new_case_12(self):
        tp = TPSwitchStatement()
        lemma, inflection = 'do', 'did'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        lemma, inflection = 'nudge', 'nudged'
        tp.train_on_pair(lemma, inflection, 'tense=PST')
        assert(len(tp.cases) == 2)
        assert(tp.inflect('do', 'tense=PST') == 'did')
        assert(tp.inflect('nudge', 'tense=PST') == 'nudged')

if __name__ == "__main__":
    unittest.main()