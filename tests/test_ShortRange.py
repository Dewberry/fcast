import unittest
import os
import gcsfs
import scipy.interpolate
import pandas
import warnings

import sys
sys.path.append('..')
from fcast import Assim, ShortRange
print('imports succeeded')

RCFP = '../notebooks/data/hydroprop-fulltable2D.nc'


class TestShortRange(unittest.TestCase):

    def setUp(self):
        """Sample data for test case"""
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.fs = gcsfs.GCSFileSystem(project='national-water-model')
        self.date = '20190802'
        self.start_hr = 0
        self.comid = 4512772
        sim = Assim(self.fs, self.comid, self.date, self.start_hr)
        self.sr = ShortRange(self.fs, self.comid, self.date, self.start_hr)
        self.sr_df = self.sr.get_streamflow(sim.assim_time, sim.assim_flow)

    def test_flow_df(self):
        self.assertIsInstance(self.sr_df, pandas.DataFrame, 'ShortRange flow is not a pandas.DataFrame')
        self.assertEqual(self.sr_df.shape, (19, 1), f'Streamflow df should be (19, 1), instead was {self.sr_df.shape}')
        self.assertTrue(self.sr_df.all().values[0], 'Streamflow df has NaN, null, or 0 in it')

    def test_nfiles(self):
        self.assertEqual(self.sr.nfiles, 18)

    def test_rc(self):
        f, df = self.sr.get_NWM_rc(rc_filepath=RCFP)[0], self.sr.get_NWM_rc(rc_filepath=RCFP)[1]
        self.assertIsInstance(f, scipy.interpolate.interpolate.interp1d, 'Rating curve function is not scipy interp1d')
        self.assertIsInstance(df, pandas.DataFrame, 'Rating curve df is not pandas.DataFrame')

    def test_copy_to_local(self):
        self.sr.copy_to_local('.')
        for f in self.sr.filepaths:
            self.assertTrue(os.path.exists(os.path.basename(f)))
            os.remove(os.path.basename(f))


if __name__ == '__main__':
    unittest.main()
