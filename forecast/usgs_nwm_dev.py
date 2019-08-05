import requests
from bs4 import BeautifulSoup
import pandas as pd
# import matplotlib.pyplot as plt

class usgsGage:

    def __init__(self, gage: str):
        self._gage = gage
        self._metadata_url = f'https://waterdata.usgs.gov/nwis/inventory/?site_no={self._gage}&agency_cd=USGS'
        self._rc_url = f'https://waterdata.usgs.gov/nwisweb/get_ratings?site_no={self._gage}&file_type=exsa'
        self.__metadata_request = requests.get(self._metadata_url)
        self.__rc_request = requests.get(self._rc_url)

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
                if 'Lat' in x:
                    d['lat'] = deg_to_dec(x.split(',')[0].split(' ')[1])
                    d['lon'] = deg_to_dec(x.split(', ')[1].split(' ')[1])
                    d['horizontal datum'] = x.split(' ')[-1]
                elif 'Hydrologic' in x:
                    d['HUC8'] = x.split(' ')[-1]
                elif 'Datum' in x:
                    d['vertical datum'] = x.split('above ')[1].replace('.', '')
                    d['feet above vertical datum'] = float(x.split(': ')[1].split(' feet')[0].replace(',', ''))
                elif 'Drainage area' in x:
                    d['drainage area sqmi'] = float(x.split(': ')[1].split(' ')[0].replace(',', ''))
            d['gage'] = gage
            return d

        def get_gage_meta(self) -> dict:
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

        self._metadata = get_gage_meta(self)
        self._lat = self._metadata['lat']
        self._lon = self._metadata['lon']
        self._horizontal_datum = self._metadata['horizontal datum']
        self._HUC8 = self._metadata['HUC8']
        self._vertical_datum = self._metadata['vertical datum']
        self._feet_above_vertical_datum = self._metadata['feet above vertical datum']
        self._drainage_area_sqmi = self._metadata['drainage area sqmi']

        def get_gage_available_data(self) -> pd.DataFrame:
            """
            Scrape available data table from USGS website
            :param gage: usgs gage ID(e.g. '05418500')
            :return: html table as dataframe
            """
            soup = BeautifulSoup(self.__metadata_request.content, 'lxml')
            table = soup.find_all('table')[0]
            return pd.read_html(str(table))[0]

        self._available_data = get_gage_available_data(self)

        def get_rating_curve(self):
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

        def get_rating_curve_metadata(self):
            pass

    @property
    def gage(self):
        return self._gage
    
    @property
    def metadata_url(self):
        return self._metadata_url
    
    @property
    def metadata(self):
        return self._metadata

    @property
    def lat(self):
        return self._lat
    
    @property
    def lon(self):
        return self._lon
    
    @property
    def horizontal_datum(self):
        return self._horizontal_datum
    
    @property
    def HUC8(self):
        return self._HUC8
    
    @property
    def vertical_datum(self):
        return self._vertical_datum
    
    @property
    def feet_above_vertical_datum(self):
        return self._feet_above_vertical_datum
    
    @property
    def drainage_area_sqmi(self):
        return self._drainage_area_sqmi

    @property
    def available_data(self):
        return self._available_data
    
    