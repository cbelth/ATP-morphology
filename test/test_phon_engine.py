import unittest
import sys
sys.path.append('../src/')
from phon_engine import PhonEngine

class TestPhonEngine(unittest.TestCase):
    def test_init(self):
        phon_engine = PhonEngine()

    def test_suffixation_1(self):
        phon_engine = PhonEngine()
        assert(phon_engine.apply_suffix('wɔk', 't') == 'wɔkt')

    def test_suffixation_2(self):
        phon_engine = PhonEngine()
        assert(phon_engine.apply_suffix('wɔk', 'd') == 'wɔkt')

    def test_suffixation_3(self):
        phon_engine = PhonEngine()
        assert(phon_engine.apply_suffix('sprɪnt', 'ɪd') == 'sprɪntɪd')

    def test_suffixation_4(self):
        phon_engine = PhonEngine()
        assert(phon_engine.apply_suffix('sprɪnt', 'd') == 'sprɪntɪd')

    def test_suffixation_5(self):
        phon_engine = PhonEngine()
        assert(phon_engine.apply_suffix('pleɪ', 'd') == 'pleɪd')
        assert(phon_engine.apply_suffix('wɔk', 'd') == 'wɔkt')
        assert(phon_engine.apply_suffix('sprɪnt', 'd') == 'sprɪntɪd')

    def test_suffixation_6(self):
        phon_engine = PhonEngine()
        assert(phon_engine.apply_suffix('pleɪ', 't') == 'pleɪd')
        assert(phon_engine.apply_suffix('wɔk', 't') == 'wɔkt')
        assert(phon_engine.apply_suffix('sprɪnt', 't') == 'sprɪntɪd')

    def test_suffixation_7(self):
        phon_engine = PhonEngine()
        assert(phon_engine.apply_suffix('wɔk', 's') == 'wɔks')
        assert(phon_engine.apply_suffix('ʧæt', 's') == 'ʧæts')
        assert(phon_engine.apply_suffix('dɪmænd', 's') == 'dɪmændz')

if __name__ == "__main__":
    unittest.main()