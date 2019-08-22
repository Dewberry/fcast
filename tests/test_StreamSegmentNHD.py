import unittest
import shapely.geometry
from collections import OrderedDict
import json
import fiona

import sys
sys.path.append('..')
from fcast import StreamSegmentNHD
print('imports succeeded')

with open('../notebooks/data/NHDPlusV21/comidDict_NHDPlusV21.json', 'r') as f:
    MAP = json.loads(f.read())
GDB = r'../notebooks/data/NHDPlusV21/NHDPlusV21_National_Seamless_Flattened_Lower48.gdb'
LYR = 'NHDFlowline_Network'
SRC = fiona.open(GDB, layer=LYR)


class TestStreamSegmentNHD(unittest.TestCase):

    def setUp(self):
        """Sample data for test case"""
        self.comid = 4512772  # some small segment on the Potomac near DC
        self.seg = StreamSegmentNHD(self.comid, MAP, SRC, warning=False)

    def test_geom(self):
        self.assertIsInstance(self.seg.geometry, shapely.geometry.multilinestring.MultiLineString,
                              'Geometry is not a shapely MultiLineString')

    def test_attrs(self):
        self.assertIsInstance(self.seg.attrs, OrderedDict, 'Attributes are not stored in an OrderedDict')
        self.assertEqual(len(self.seg.attrs), 137, 'Attributes are missing')

    def test_proj(self):
        self.assertEqual(self.seg.crs_proj4, '+init=epsg:4269', f'Expected +init=epsg:4269, got {self.seg.crs_proj4}')


if __name__ == '__main__':
    unittest.main()
