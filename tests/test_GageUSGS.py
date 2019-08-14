import unittest
import pandas

import sys
sys.path.append('..')
from fcast import GageUSGS
print('imports succeeded')


class TestGageUSGS(unittest.TestCase):

    def setUp(self):
        """Sample data for test case"""
        self.id = '01651000'
        self.gage = GageUSGS(self.id)

    def test_avail_data(self):
        self.assertIsInstance(self.gage.available_data, pandas.DataFrame, 'Available data is not a pandas.DataFrame')

    def test_metadata(self):
        self.assertIsInstance(self.gage.metadata, dict, 'Metadata is not a dict')

    def test_rc(self):
        x = GageUSGS(self.id, get_rc=False)
        with self.assertRaises(TypeError):
            x.rating_curve
        with self.assertRaises(TypeError):
            x.rating_curve_metadata

    def test_notimplemented(self):
        with self.assertRaises(NotImplementedError):
            GageUSGS('01651750')


if __name__ == '__main__':
    unittest.main()
