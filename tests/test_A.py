import unittest
import os
import sys
PARENTDIR=os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PARENTDIR)
import definitive_screening_design as dsd

class TestA(unittest.TestCase):
    def test_primes(self):
        self.assertEqual( list(map(dsd._generalized_dsd.isprime,[2371, 2927, 6949, 6948, 1249, 3739, 9311])), [True, True, True, False, True, True, True])

    def test_example(self):
        self.assertEqual( dsd.design.generate(n_num=3,n_cat=2).shape,(14,5))
    
    def test_10(self):
        self.assertEqual( dsd.design.generate(10).shape[0], 21)


if __name__ == '__main__':
     unittest.main()

