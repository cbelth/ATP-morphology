import unittest
import sys
sys.path.append('../src/')
from utils import most_freq

class TestUtils(unittest.TestCase):
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