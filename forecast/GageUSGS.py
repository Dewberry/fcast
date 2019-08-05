import requests
from bs4 import BeautifulSoup
import pandas as pd

LATITUDE = 'Lat'
LONGITUDE ='Lon'
HDATUM = 'horizontal datum'
VDATUM = 'vertical datum'
RDATUM ='feet above vertical datum' # Relative to vertical datum
HUC8 = 'HUC8'
DA = 'Drainage area'
DASQMILES = 'drainage area sqmi'
DASQMETERS = 'drainage area sq meters'

class GageUSGS:

    def __init__(self, gage: str, get_rc: bool=True):
        self._gage = gage
        self._metadata_url = f'https://waterdata.usgs.gov/nwis/inventory/?site_no={self._gage}&agency_cd=USGS'
        self._rc_url = f'https://waterdata.usgs.gov/nwisweb/get_ratings?site_no={self._gage}&file_type=exsa'
        self.__metadata_request = requests.get(self._metadata_url)
        self.__get_rc = get_rc

        def check_implemented():
            soup = BeautifulSoup(self.__metadata_request.text, "html.parser")
            sitetype = soup.find("h3").text.strip()
            if 'Estuary' in sitetype or 'Tidal' in sitetype:
                raise NotImplementedError(f'Support for type: {sitetype} has not yet been implemented.')

        check_implemented()

        def deg_to_dec(string):
            """
            converts a coordinate in degrees, converts to decimal degree
            :param string:
            :return:
            """
            deg = float(string.split('°')[0])
            mn = float(string.split('\'')[0].split('°')[1])
            sec = float(string.split('\'')[1].replace('"', ''))
            dd = deg + mn/60 + sec/3600
            return dd

        def usgs_descrip_to_dict(descrip: list, gage: str) -> dict:
            """
            Takes a list of strings from the USGS Website, and turns it into a dictionary of metadata
            :nested functions:
                1. deg_to_dec
            :param descrip: container for data from metadata ()
            :param gage: Gauge ID (e.g. '05418500')
            :return:
            """
            d = {}
            for x in descrip:
                if LATITUDE in x:
                    d[LATITUDE] = deg_to_dec(x.split(',')[0].split(' ')[1])
                    d[LONGITUDE] = deg_to_dec(x.split(', ')[1].split(' ')[1])
                    d[HDATUM] = x.split(' ')[-1]
                elif 'Hydrologic' in x:
                    d[HUC8] = x.split(' ')[-1]
                elif 'Datum' in x:
                    d[VDATUM] = x.split('above ')[1].replace('.', '')
                    d[RDATUM] = float(x.split(': ')[1].split(' feet')[0].replace(',', ''))
                elif DA in x:
                    d[DASQMILES] = float(x.split(': ')[1].split(' ')[0].replace(',', ''))
            d['gage'] = gage
            return d

        def get_gage_meta() -> dict:
            """
            Scrape metadata from USGS website
            :nested functions:
                1. usgs_descrip_to_dict
            :param gage: usgs gage ID(e.g. '05418500')
            :return: selected metadata
            """
            soup = BeautifulSoup(self.__metadata_request.text, "html.parser")
            for row in soup.find('div', {"id": "stationTable"}).contents:
                if 'Datum' in str(row):
                    break
            descrip = [j.text.replace('\xa0','').replace('  ', ' ') for j in row.find_all('dd')]
            return usgs_descrip_to_dict(descrip, self._gage)

        self._metadata = get_gage_meta()
        self._lat = self._metadata[LATITUDE]
        self._lon = self._metadata[LONGITUDE]
        self._horizontal_datum = self._metadata[HDATUM]
        self._HUC8 = self._metadata[HUC8]
        self._vertical_datum = self._metadata[VDATUM]
        self._feet_above_vertical_datum = self._metadata[RDATUM]
        self._drainage_area_sqmi = self._metadata[DASQMILES]

        def get_gage_available_data() -> pd.DataFrame:
            """
            Scrape available data table from USGS website
            :param gage: usgs gage ID(e.g. '05418500')
            :return: html table as dataframe
            """
            soup = BeautifulSoup(self.__metadata_request.content, 'lxml')
            table = soup.find_all('table')[0]
            return pd.read_html(str(table))[0]

        self._available_data = get_gage_available_data()

        def get_rating_curve() -> pd.DataFrame:
            """
            Reads the table beginning after comment lines at rc_url
            :param gage:
            :return: rating curve dataframe
            """
            a = self.__rc_request.text.split('\n')
            b = [i for i in a if '#' not in i]
            c = [i.split('\t') for i in b]
            cols = c[0]
            del c[1], c[0]
            df = pd.DataFrame(c, columns=cols).drop(columns=['STOR'])
            df = df.apply(pd.to_numeric)
            df['INDEP_SHIFT'] = df.INDEP + df.SHIFT
            df['INDEP_m'] = df.INDEP * 0.3048
            df['SHIFT_m'] = df.SHIFT * 0.3048
            df['DEP_cms'] = df.DEP * 0.028316847
            df['INDEP_SHIFT_m'] = df.INDEP_m + df.SHIFT_m
            return df

        def get_rc_metadata() -> dict:
            metalines = [line for line in self.__rc_request.text.split('\n') if '#' in line]
            warnings = [line for line in self.__rc_request.text.split('\n') if '# //WARNING' in line]
            d = {}
            d['WARNING'] = ''.join([line.replace('# //WARNING', '') for line in warnings]).strip()
            for line in metalines:
                if 'RETRIEVED' in line:
                    d['RETRIEVED'] = line.split(': ')[-1]
                elif not 'WARNING' in line and '=' in line:
                    line = line.replace('# //', '')
                    key = line.split(' ')[0]
                    vals = ' '.join(line.split(' ')[1:])
                    d[key] = vals.strip()
            return d


        if self.__get_rc:
            self.__rc_request = requests.get(self._rc_url)
            self._rating_curve = get_rating_curve()
            self._rating_curve_metadata = get_rc_metadata()
        else:
            self._rating_curve = 'No rating curve retrieved. If rating curve desired, set get_rc = True'

        def get_rating_curve_metadata(self):
            pass

    @property
    def rating_curve_metadata(self):
        """USGS Rating curve at gage location"""
        if self.__get_rc:
            return self._rating_curve_metadata
        else:
            raise TypeError(self._rating_curve)

    @property
    def rating_curve(self):
        """USGS Rating curve at gage location"""
        if self.__get_rc:
            return self._rating_curve
        else:
            raise TypeError(self._rating_curve)
    
    @property
    def gage(self):
        """Gage id string"""
        return self._gage
    
    @property
    def metadata_url(self):
        """Url that the gage metadata is gathered from"""
        return self._metadata_url
    
    @property
    def metadata(self):
        """Dictionary of general gage metadata"""
        return self._metadata

    @property
    def lat(self):
        """Latitude of the gage"""
        return self._lat
    
    @property
    def lon(self):
        """Longitude of the gage"""
        return self._lon
    
    @property
    def horizontal_datum(self):
        """Horizontal Datum of the gage"""
        return self._horizontal_datum
    
    @property
    def HUC8(self):
        """HUC8 that the gage is within"""
        return self._HUC8
    
    @property
    def vertical_datum(self):
        """Vertical datum of the gage"""
        return self._vertical_datum
    
    @property
    def feet_above_vertical_datum(self):
        """Feet aboe the vertical datum, for stage to elevation conversions"""
        return self._feet_above_vertical_datum
    
    @property
    def drainage_area_sqmi(self):
        """Drainage area upstream of the gage in sq miles"""
        return self._drainage_area_sqmi

    @property
    def available_data(self):
        """The data available from the metadata url"""
        return self._available_data
     
# a = 1

# try:
#     a + bool

# except NameError as e:
#     print(f'Fail due to {e}')

# except TypeError as e:
#     print(f'Fail due to {e}')

# except:
#     print('Last resort....didnt see this coming')
