import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def usgs_descrip_to_dict(descrip: list, gage: str):
    d = {}
    for x in descrip:
        if 'Lat' in x:
            d['lat'] = deg_to_dec(x.split(',')[0].split(' ')[1])
            d['lon'] = deg_to_dec(x.split(', ')[1].split(' ')[1])
            d['horizontal datum'] = x.split(' ')[-1]
        elif 'Hydrologic' in x:
            d['HUC8'] = int(x.split(' ')[-1])
        elif 'Datum' in x:
            d['vertical datum'] = x.split('above ')[1].replace('.', '')
            d['feet above vertical datum'] = float(x.split(': ')[1].split(' feet')[0].replace(',', ''))
        elif 'Drainage area' in x:
            d['drainage area sqmi'] = float(x.split(': ')[1].split(' ')[0].replace(',', ''))
    d['gage'] = gage
    return d

def deg_to_dec(string):
    deg = float(string.split('°')[0])
    mn = float(string.split('\'')[0].split('°')[1])
    sec = float(string.split('\'')[1].replace('"', ''))
    dd = deg + mn/60 + sec/3600
    return dd

def get_gage_meta(gage: str):
    url = f'https://waterdata.usgs.gov/nwis/inventory/?site_no={gage}&agency_cd=USGS'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for i in soup.find('div', {"id": "stationTable"}).contents:
        if 'Datum' in str(i):
            break
    descrip = [j.text.replace('\xa0','').replace('  ', ' ') for j in i.find_all('dd')]
    return usgs_descrip_to_dict(descrip, gage)

def new_plot(figsize=(20,6), fontsize=18) -> plt.subplots:
    '''Return a created new plotframe.'''
    
    fig,  ax = plt.subplots(figsize=figsize)
    ax.set_xlabel('Discharge (cms)', fontsize=fontsize)
    ax.set_ylabel('Stage', fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.grid(which='major', color='lightgrey', linestyle='--', linewidth=2)
    return fig, ax

def get_USGS_ratingcurve(gage: str):
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