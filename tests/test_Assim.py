import unittest
import os
import gcsfs
import numpy
import scipy.interpolate
import pandas

import sys
sys.path.append('..')
from fcast import Assim
import warnings
print('imports succeeded')

RCFP='../notebooks/data/hydroprop-fulltable2D.nc'

class TestAssim(unittest.TestCase):

    def setUp(self):
        """Sample data for test case"""
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.fs = gcsfs.GCSFileSystem(project='national-water-model')
        self.date = '20190802'
        self.start_hr = 0
        self.comid = 4512772
        self.sim = Assim(self.fs, self.comid, self.date, self.start_hr)

    def test_flow(self):
        self.assertIsInstance(self.sim.assim_flow, float, 'assim_flow is not a float')

    def test_nfiles(self):
        self.assertEqual(self.sim.nfiles, 3)

    def test_time(self):
        self.assertIsInstance(self.sim.assim_time, numpy.datetime64, 'assim_time is not a numpy.datetime64')

    def test_offset(self):
        with self.assertRaises(AssertionError):
            Assim(self.fs, self.comid, self.date, self.start_hr, offset=4)

    def test_rc(self):
        f, df = self.sim.get_NWM_rc(rc_filepath=RCFP)[0], self.sim.get_NWM_rc(rc_filepath=RCFP)[1]
        self.assertIsInstance(f, scipy.interpolate.interpolate.interp1d, 'Rating curve function is not scipy interp1d')
        self.assertIsInstance(df, pandas.DataFrame, 'Rating curve df is not pandas.DataFrame')

    def test_copy_to_local(self):
        self.sim.copy_to_local('.')
        self.assertTrue(os.path.exists(os.path.basename(self.sim.filepath)))
        os.remove(os.path.basename(self.sim.filepath))

if __name__ == '__main__':
    unittest.main()
