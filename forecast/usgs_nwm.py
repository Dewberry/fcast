import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


def get_gage_meta(gage: str) -> dict:
    """
    Scrape metadata from USGS website
    :nested functions:
        1. usgs_descrip_to_dict
    :param gage: usgs gage ID(e.g. '05418500')
    :return: selected metadata
    """
    url = f'https://waterdata.usgs.gov/nwis/inventory/?site_no={gage}&agency_cd=USGS'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for row in soup.find('div', {"id": "stationTable"}).contents:
        if 'Datum' in str(row):
            break
    descrip = [j.text.replace('\xa0','').replace('  ', ' ') for j in row.find_all('dd')]
    return usgs_descrip_to_dict(descrip, gage)

def get_gage_available_data(gage: str) -> pd.DataFrame:
    """
    Scrape available data table from USGS website
    :param gage: usgs gage ID(e.g. '05418500')
    :return: html table as dataframe
    """
    url = f'https://waterdata.usgs.gov/nwis/inventory/?site_no={gage}&agency_cd=USGS'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    table = soup.find_all('table')[0]
    return pd.read_html(str(table))[0]

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


def new_plot(figsize:tuple = (20, 6), fontsize: int = 18,
             xlabel:str = 'Discharge (cms)', ylabel:str = 'Stage') -> plt.subplots:
    """
    Generic plot setup
    :param figsize: recommeded 20,6 for notebooks
    :param fontsize: label fontsize
    :param xlabel: be careful, best to make a test to verify units are consistent
    :param ylabel: be careful, best to make a test to verify units are consistent
    :return: matplotlib fig, ax
    """
    fig,  ax = plt.subplots(figsize=figsize)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    # labelsize is the ticsize
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.grid(which='major', color='lightgrey', linestyle='--', linewidth=2)
    return fig, ax

def get_USGS_ratingcurve(gage: str):
    """
    Reads the table beginning after comment lines at url
    :param gage:
    :return:
    """
    url = f'https://waterdata.usgs.gov/nwisweb/get_ratings?site_no={gage}&file_type=exsa'
    r = requests.get(url)
    a = r.text.split('\n')
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