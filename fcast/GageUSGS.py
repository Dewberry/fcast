# GageUSGS is a class object used for webscraping metadata, current
# information, and rating curves from USGS stream flow gages. At the
# moment, tidal and estuary gages are not supported. This file only
# works on python version 3.6 or newer.
#
# Author: Alec Brazeau (abrazeau@dewberry.com)
#
# Copyright: Dewberry
#
# ----------------------------------------------------------------------

# import the required libs
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

# from IPython.display import IFrame

# Set global variables
LATITUDE = "Lat"
LONGITUDE = "Lon"
HDATUM = "horizontal datum"
VDATUM = "vertical datum"
RDATUM = "feet above vertical datum"  # Relative to vertical datum
HUC8 = "HUC8"
DA = "Drainage area"
DASQMILES = "drainage area sqmi"
DASQMETERS = "drainage area sq meters"


class GageUSGS:
    """USGS stream gage class containing data scraped from USGS websites.

    The class currently supports scraping of stream gage metadata 
    (i.e. vertical datum, lat/lon, etc.), currently available data
    at a gage, as well as rating curves and their metadata.

    Parameters:
        gage (str): A string representing a USGS gage id (e.g. '01400000').
        get_rc (bool, optional): Get the rating curve for the USGS gage. Defaults to True.
    """

    def __init__(self, gage: str, get_rc: bool = True):

        # assert that the user system is >= python version 3.6
        ver = sys.version_info
        assert ver[0] == 3 and ver[1] >= 6, "Must be using python version 3.6 or newer"

        self._gage = gage
        self._metadata_url = f"https://waterdata.usgs.gov/nwis/inventory/?site_no={self._gage}&agency_cd=USGS"
        self._rc_url = f"https://waterdata.usgs.gov/nwisweb/get_ratings?site_no={self._gage}&file_type=exsa"
        self.__metadata_request = requests.get(self._metadata_url)
        self.__get_rc = get_rc

        def check_implemented():
            """Ensure that the gage is not tidal/estuary"""
            soup = BeautifulSoup(self.__metadata_request.text, "html.parser")
            sitetype = soup.find("h3").text.strip()
            if "Estuary" in sitetype or "Tidal" in sitetype:
                raise NotImplementedError(f"Support for type: {sitetype} has not yet been implemented.")

        check_implemented()

        def deg_to_dec(string) -> float:
            """
            Converts a coordinate in degrees, converts to decimal degree
            param string: An unwieldy lat/lon string (e.g. 40°34'14")
            return: Lat/lon coordinate as a float
            """
            deg = float(string.split("°")[0])
            mn = float(string.split("'")[0].split("°")[1])
            sec = float(string.split("'")[1].replace('"', ""))
            dd = deg + mn / 60 + sec / 3600
            return dd

        def usgs_descrip_to_dict(descrip: list, gage: str) -> dict:
            """
            Takes a list of strings from the USGS Website, and turns it into a dictionary of metadata
            nested functions:
                1. deg_to_dec
            descrip: container for data from metadata ()
            gage: Gage ID (e.g. '05418500')
            Dictionary of metadata
            """
            # Initialize dictionary to be populated with data
            metadata = {}
            for x in descrip:
                # Go through each string and pull relative information
                if LATITUDE in x:
                    metadata[LATITUDE] = deg_to_dec(x.split(",")[0].split(" ")[1])
                    metadata[LONGITUDE] = deg_to_dec(x.split(", ")[1].split(" ")[1])
                    metadata[HDATUM] = x.split(" ")[-1]
                elif "Hydrologic" in x:
                    metadata[HUC8] = x.split(" ")[-1]
                elif "Datum" in x:
                    metadata[VDATUM] = x.split("above ")[1].replace(".", "")
                    metadata[RDATUM] = float(x.split(": ")[1].split(" feet")[0].replace(",", ""))
                elif DA in x:
                    metadata[DASQMILES] = float(x.split(": ")[1].split(" ")[0].replace(",", ""))
            metadata["gage"] = gage
            return metadata

        def get_gage_meta() -> dict:
            """
            Scrape metadata from USGS website
            nested functions:
                1. usgs_descrip_to_dict
            return: selected metadata
            """
            soup = BeautifulSoup(self.__metadata_request.text, "html.parser")
            for row in soup.find("div", {"id": "stationTable"}).contents:
                if "Latitude" in str(row):
                    break
            # Get a list of cleaned strings, each representing some metadata
            descrip = [j.text.replace("\xa0", "").replace("  ", " ") for j in row.find_all("dd")]
            return usgs_descrip_to_dict(descrip, self._gage)

        self._metadata = get_gage_meta()
        self._lat = self._metadata[LATITUDE]
        self._lon = self._metadata[LONGITUDE]
        self._horizontal_datum = self._metadata[HDATUM]
        self._HUC8 = self._metadata[HUC8]

        try:
            self._vertical_datum = self._metadata[VDATUM]
        except KeyError:
            self._vertical_datum = None

        try:
            self._feet_above_vertical_datum = self._metadata[RDATUM]
        except KeyError:
            self._feet_above_vertical_datum = None

        self._drainage_area_sqmi = self._metadata[DASQMILES]

        def get_gage_available_data() -> pd.DataFrame:
            """
            Scrape available data table from USGS website
            return: Html table as dataframe
            """
            soup = BeautifulSoup(self.__metadata_request.content, "lxml")
            table = soup.find_all("table")[0]
            return pd.read_html(str(table))[0]

        self._available_data = get_gage_available_data()

        def get_rating_curve() -> pd.DataFrame:
            """
            Reads the table beginning after comment lines at rc_url
            return: rating curve dataframe
            """
            assert ("INDEP" in self.__rc_request.text), "No rating curve available, please set `get_rc` = False"
            a = self.__rc_request.text.split("\n")
            b = [i for i in a if "#" not in i]
            c = [i.split("\t") for i in b]
            cols = c[0]
            del c[1], c[0]
            df = pd.DataFrame(c, columns=cols).drop(columns=["STOR"])
            df = df.apply(pd.to_numeric)
            df["INDEP_SHIFT"] = df.INDEP + df.SHIFT
            df["INDEP_m"] = df.INDEP * 0.3048
            df["SHIFT_m"] = df.SHIFT * 0.3048
            df["DEP_cms"] = df.DEP * 0.028316847
            df["INDEP_SHIFT_m"] = df.INDEP_m + df.SHIFT_m
            return df

        def get_rc_metadata() -> dict:
            """
            Scrapes metadata from the commented lines at top of the rc_url
            :return: Rating curve metadata dict
            """
            # Get a list of all commented lines, as well as all WARNING lines
            metalines = [line for line in self.__rc_request.text.split("\n") if "#" in line]
            warnings = [line for line in self.__rc_request.text.split("\n") if "# //WARNING" in line]
            # Initialize dictionary to contain metadata
            metadata = {"WARNING": "".join([line.replace("# //WARNING", "") for line in warnings]).strip()}
            for line in metalines:
                # Populate the dictionary with all the metadata provided
                if "RETRIEVED" in line:
                    metadata["RETRIEVED"] = line.split(": ")[-1]
                elif not "WARNING" in line and "=" in line:
                    line = line.replace("# //", "")
                    key = line.split(" ")[0]
                    vals = " ".join(line.split(" ")[1:])
                    metadata[key] = vals.strip()
            return metadata

        if self.__get_rc:
            # Only retrieve rating curve info if specified at init. Defaults to True.
            self.__rc_request = requests.get(self._rc_url)
            self._rating_curve = get_rating_curve().dropna()
            self._rating_curve_metadata = get_rc_metadata()
        else:
            # Use this attr as an error message if the rating curve properties are called
            self._rating_curve = "No rating curve retrieved. If rating curve desired, set get_rc = True"

    @property
    def rating_curve_metadata(self):
        """USGS Rating curve metadata at gage location"""
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
        """Feet above the vertical datum, for stage to elevation conversions"""
        return self._feet_above_vertical_datum

    @property
    def drainage_area_sqmi(self):
        """Drainage area upstream of the gage in sq miles"""
        return self._drainage_area_sqmi

    @property
    def available_data(self):
        """The data available from the metadata url"""
        return self._available_data

    @property
    def rating_curve_url(self):
        return self._rc_url

    # def open_main_site(self) -> IFrame:
    #     """Open the selected USGS station website. Users can use this website to prepare
    #     the required parameters for retrieving the desired records.
    #     """
    #     return IFrame(src=self._metadata_url, width='100%', height='500px')

    # def open_rating_curve_site(self) -> IFrame:
    #     """Open the selected USGS station website. Users can use this website to prepare
    #     the required parameters for retrieving the desired records.
    #     """
    #     return IFrame(src=self._rc_url, width='100%', height='500px')
