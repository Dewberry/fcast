import unittest
import os
import gcsfs
import scipy.interpolate
import pandas
import warnings

import sys
sys.path.append('..')
from fcast import Assim, MediumRange
print('imports succeeded')

RCFP = '../notebooks/data/hydroprop-fulltable2D.nc'


class TestMediumRange(unittest.TestCase):

    def setUp(self):
        """Sample data for test case"""
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.fs = gcsfs.GCSFileSystem(project='national-water-model')
        self.date = '20190802'
        self.start_hr = 0
        self.comid = 4512772
        self.mems = (1, 4, 6)
        sim = Assim(self.fs, self.comid, self.date, self.start_hr)
        self.mr = MediumRange(self.fs, self.comid, self.date, self.start_hr)
        self.mr_df = self.mr.get_streamflow(sim.assim_time, sim.assim_flow)
        self.mr_mems = MediumRange(self.fs, self.comid, self.date, self.start_hr, self.mems)
        self.mr_mems_df = self.mr_mems.get_streamflow(sim.assim_time, sim.assim_flow)

    def test_flow_df(self):
        self.assertIsInstance(self.mr_df, pandas.DataFrame, 'ShortRange flow is not a pandas.DataFrame')
        self.assertEqual(self.mr_df.shape, (69, 8),
                         f'All members df should be of shape (69, 8), instead was {self.mr_df.shape}')
        self.assertTrue(self.mr_df.all().values[0], 'Streamflow df has NaN, null, or 0 in it')
        self.assertEqual(self.mr_mems_df.shape, (69, len(self.mr_mems.members)+1),
                         f'MediumRange with less members df should of shape be (69, {len(self.mr_mems.members)+1}),'
                         f' instead was {self.mr_mems_df.shape}')
        self.assertTrue(self.mr_mems_df.all().values[0], 'Streamflow df has NaN, null, or 0 in it')

    def test_nfiles(self):
        self.assertEqual(self.mr.nfiles, int(len(self.mr.filepaths) * len(self.mr.filepaths[0])))

    def test_rc(self):
        f, df = self.mr.get_NWM_rc(rc_filepath=RCFP)[0], self.mr.get_NWM_rc(rc_filepath=RCFP)[1]
        self.assertIsInstance(f, scipy.interpolate.interpolate.interp1d, 'Rating curve function is not scipy interp1d')
        self.assertIsInstance(df, pandas.DataFrame, 'Rating curve df is not pandas.DataFrame')

    def test_copy_to_local(self):
        self.mr_mems.copy_to_local('.')
        for mem in self.mr_mems.filepaths:
            for f in mem:
                self.assertTrue(os.path.exists(os.path.basename(f)))
                os.remove(os.path.basename(f))


if __name__ == '__main__':
    unittest.main()
