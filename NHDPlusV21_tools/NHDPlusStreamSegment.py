# StreamSegmentNHD is a class object that represents a stream segment
# in the NHDPlusV2.1. It is built for easy access to a single stream 
# segment represented by a ComID without overburdening memory. It is
# meant for the NHDPlusV21_National_Seamless_Flattened_Lower48.gdb. It
# also requires a ComID dictionary used as a map, which can be found at
# s3://nwm-datasets/Data/Vector/NHDPlusV21_CONUS_seamless/comidDict_NHDPlusV21.json
# or can be made using fiona like so:
# ```
# src = fiona.open(gdb, layer='NHDFlowline_Network')
# comidDict = {src[f]['properties']['COMID']: f for f in src.keys()}
# ```
#
# Author: Alec Brazeau (abrazeau@dewberry.com)
#
# Copyright: Dewberry
#
# ----------------------------------------------------------------------

import fiona
import fiona.crs
import shapely
from shapely.geometry import shape
from datetime import datetime
from collections import OrderedDict
import warnings

class StreamSegmentNHD:
    """A representation of one individual NHDPlusV2.1 ComID stream segment.

    For detailed information on the dataset, download the Release Notes from
    http://www.horizon-systems.com/NHDPlusData/NHDPlusV21/Data/NationalData/0Release_Notes_NationalData_Seamless_GeoDatabase.pdf
    
    All property docstrings have been pulled from these release notes.

    Parameters:
        comid (int): The comID that corresponds to the stream segment of interest.
        comidDict (dict): The dictionary used to map the ComIDs to the feature index in
                          the gdb. Generally loaded into memory using json.load(filepath)
        src (fiona.collection): The open fiona collection representing the gdb and the 
                                'NHDFlowline_Network' layer.
        warning (bool, optional): Defaults to true. Raises a warning to ensure the comidDict
                                  NHDPlus version matches that of the gdb.
    """

    def __init__(self, comid: int, comidDict: dict, src: fiona.collection, warning: bool = True):
        
        self.__warning = warning
        if self.__warning:
            warnings.warn('Make sure your comidDict json NHDPlus version matches your gdb NHDPlus version')
        
        self._comid = comid
        self._comidDict = comidDict
        self._src = src

        def get_attrs():
            """Pull the attributes of the feature from the fiona collection"""
            return self._src[self._comidDict[self._comid]]['properties']

        self._attrs = get_attrs()
        self._feat_currency_date = self._attrs['FDATE']
        self._resolution = self._attrs['RESOLUTION']
        self._GNIS_id = self._attrs['GNIS_ID']
        self._GNIS_name = self._attrs['GNIS_NAME']
        self._length_km = self._attrs['LENGTHKM']
        self._reach_code = self._attrs['REACHCODE']
        self._WB_area_comid = self._attrs['WBAREACOMI']
        self._stream_order = self._attrs['StreamOrde']
        self._from_node_id = self._attrs['FromNode']
        self._to_node_id = self._attrs['ToNode']
        self._tot_drainage_area_sqkm = self._attrs['TotDASqKM']
        self._tidal = self._attrs['Tidal']
        self._max_elev_raw = self._attrs['MAXELEVRAW']
        self._min_elev_raw = self._attrs['MINELEVRAW']
        self._max_elev_smoothed = self._attrs['MAXELEVSMO']
        self._min_elev_smoothed = self._attrs['MINELEVSMO']
        self._geometry = shape(self._src[self._comidDict[self._comid]]['geometry'])
        self._annual_mean_flow_QA = self._attrs['QA_MA']
        self._annual_mean_vel_QA = self._attrs['VA_MA']
        self._annual_mean_flow_QC = self._attrs['QC_MA']
        self._annual_mean_vel_QC = self._attrs['VC_MA']
        self._annual_mean_flow_QE = self._attrs['QE_MA']
        self._annual_mean_vel_QE = self._attrs['VE_MA']

        def get_current_month_QV():
            """Pull the current month using datetime.now() and get the matching Qs and Vs"""
            curr_month = str(datetime.now()).split('-')[1]
            data = OrderedDict()
            for k, v in self._attrs.items():
                if curr_month in k:
                    data[k] = v
            return data

        self._current_month_QV = get_current_month_QV()
        self._QV_meta = {
        'QA': 'Mean Annual Flow from runoff (cfs)',
        'VA': 'Mean Annual Velocity for QA (fps)',
        'QC': 'Mean Annual Flow with Reference Gage Regression applied to QB (cfs).'
        ' Best EROM estimate of “natural” mean flow.',
        'VC': 'Mean Annual Velocity for QC (fps).'
        ' Best EROM estimate of “natural” mean velocity.',
        'QE': 'Mean Annual Flow from gage adjustment (cfs).'
        ' Best EROM estimate of actual mean flow.',
        'VE': 'Mean Annual Velocity from gage adjustment (fps).'
        ' Best EROM estimate of actual mean velocity.'
        }
        self._crs_proj4 = fiona.crs.to_string(self._src.crs)
        self._crs_wkt = self._src.crs_wkt

    @property
    def comid(self):
        """Common identifier of the NHD feature"""
        return self._comid
    
    @property
    def comidDict(self):
        """Dictionary containing the ComID -> feature index map"""
        return self._comidDict
    
    @property
    def src(self):
        """The opened fiona collection of the gdb and the 'NHDFlowline_Network' layer"""
        return self._src
    
    @property
    def attrs(self):
        """An OrderedDict of all attributes for the stream segment"""
        return self._attrs

    @property
    def feat_currency_date(self):
        """Feature Currency Date"""
        return self._feat_currency_date
    
    @property
    def resolution(self):
        """NHD database resolution (i.e. “high”, “medium” or “local”)"""
        return self._resolution
    
    @property
    def GNIS_id(self):
        """Geographic Names Information System ID for the value in GNIS_Name"""
        return self._GNIS_ID
    
    @property
    def GNIS_name(self):
        """Feature Name from the Geographic Names Information System"""
        return self._GNIS_name
    
    @property
    def length_km(self):
        """Feature length in kilometers"""
        return self._length_km
    
    @property
    def reach_code(self):
        """Reach Code assigned to feature"""
        return self._reach_code

    @property
    def WB_area_comid(self):
        """ComID of the NHD polygonal water feature through which a NHD “Artificial Path” flowline flows"""
        return self._WB_area_comid
    
    @property
    def stream_order(self):
        """Modified Strahler Stream Order"""
        return self._stream_order

    @property
    def from_node_id(self):
        """Unique identifier for the point at the top of the NHDFlowline feature"""
        return self._from_node_id
    
    @property
    def to_node_id(self):
        """Unique identifier for the point at the end of the NHDFlowline feature"""
        return self._to_node_id
    
    @property
    def tot_drainage_area_sqkm(self):
        """Total upstream catchment area from downstream end of flowline."""
        return self._tot_drainage_area_sqkm
    
    @property
    def tidal(self):
        """Is Flowline Tidal? 1=yes, 0=no"""
        return self._tidal
    
    @property
    def max_elev_raw(self):
        """Maximum elevation (unsmoothed) in centimeters"""
        return self._max_elev_raw
    
    @property
    def min_elev_raw(self):
        """Minimum elevation (unsmoothed) in centimeters"""
        return self._min_elev_raw
    
    @property
    def max_elev_smoothed(self):
        """Maximum elevation (smoothed) in centimeters"""
        return self._max_elev_smoothed
    
    @property
    def min_elev_smoothed(self):
        """Minimum elevation (smoothed) in centimeters"""
        return self._min_elev_smoothed
    
    @property
    def geometry(self):
        """Shapely representation of the line segment"""
        return self._geometry
    
    @property
    def annual_mean_flow_QA(self):
        """Mean Annual Flow from runoff (cfs)"""
        return self._annual_mean_flow_QA
    
    @property
    def annual_mean_vel_QA(self):
        """Mean Annual Velocity for QA (fps)"""
        return self._annual_mean_vel_QA

    @property
    def annual_mean_flow_QC(self):
        """Mean Annual Flow with Reference Gage Regression applied to QB (cfs). Best EROM estimate of “natural” mean flow."""
        return self._annual_mean_flow_QC
    
    @property
    def annual_mean_vel_QC(self):
        """Mean Annual Velocity for QC (fps). Best EROM estimate of “natural” mean velocity."""
        return self._annual_mean_vel_QC

    @property
    def annual_mean_flow_QE(self):
        """Mean Annual Flow from gage adjustment (cfs). Best EROM estimate of actual mean flow."""
        return self._annual_mean_flow_QE
    
    @property
    def annual_mean_vel_QE(self):
        """Mean Annual Velocity from gage adjustment (fps). Best EROM estimate of actual mean velocity."""
        return self._annual_mean_vel_QE

    @property
    def current_month_QV(self):
        """
        'QA': 'Mean Annual Flow from runoff (cfs)',
        'VA': 'Mean Annual Velocity for QA (fps)',
        'QC': 'Mean Annual Flow with Reference Gage Regression applied to QB (cfs). Best EROM estimate of “natural” mean flow.',
        'VC': 'Mean Annual Velocity for QC (fps). Best EROM estimate of “natural” mean velocity.',
        'QE': 'Mean Annual Flow from gage adjustment (cfs). Best EROM estimate of actual mean flow.',
        'VE': 'Mean Annual Velocity from gage adjustment (fps). Best EROM estimate of actual mean velocity.
        """
        return self._current_month_QV
    
    @property
    def QV_meta(self):
        """Metadata describing the results of current_month_QV"""
        return self._QV_meta
    
    @property
    def crs_proj4(self):
        return self._crs_proj4
    
    @property
    def crs_wkt(self):
        return self._crs_wkt
    