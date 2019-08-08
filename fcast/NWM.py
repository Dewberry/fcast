import gcsfs
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
from scipy.interpolate import interp1d

class NWM:

    def __init__(self, fs, date, start_hr, hr):

        self._fs = fs
        self._date = date
        self._start_hr = start_hr
        self._hr = hr

    def copy_to_local(filepath):
        pass


class Assim(NWM):

    def __init__(self, fs: gcsfs.core.GCSFileSystem, comid: int, date: str, start_hr: int, hr: int = 0):

        super().__init__(filename)

        self._fs = fs
        self._comid = comid
        self._date = date
        self._start_hr = str(start_hr).zfill(2)
        self._hr = hr
        self._filepath = f'national-water-model/nwm.{date}/analysis_assim/nwm.t{start_hr}z.analysis_assim.channel_rt.tm0{hr}.conus.nc'
        self.__file = self._fs.open(self._filepath, 'rb')
        self.__assim = xr.open_dataset(self.__file)
        self._assim_time = self.__assim.sel(feature_id=comid)['time'].values[0]
        self._assim_flow = self.__assim['streamflow'].to_dataframe().loc[comid].values[0]

        # super(NWMassim, self).__init__(date, start_hr, hr)

class NWM:
    def __init__(self, filename):
        self.filename = filename
        self.start_time = None
        self.valid_fcast_time = None      

        def get_fcast_hours():
            if 'assim' in self.filename:
                return 3
            elif 'short' in self.filename:
                return 18
            elif 'medium' in self.filename:
                return 284
            else:
                #raise DumbFile error
                pass

        self.fcast_hours = get_fcast_hours()


    def copy_to_local(self):
        """Add download option here"""
        pass


class Assim(NWM):

    def __init__(self, filename):
        
        super().__init__(filename)
        
        def number_of_files():
            return self.fcast_hours

        self.nfiles = number_of_files()

        
class ShortRange(NWM):

    def __init__(self, filename):
        
        super().__init__(filename)
        

class MidRange(NWM):

    def __init__(self, filename):
        
        super().__init__(filename)