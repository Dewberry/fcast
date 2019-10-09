# Installation

### Linux / Mac
You can install `fcast` by running:
```
pip install fcast
```

### Windows

To install `fcast` in a Windows environment, `shapely`, `fiona`, and `gdal` must first be installed manually from wheel files. The wheel files should be downloaded from Christoph Gohlke's [Unofficial Windows Binaries for Python Extension Packages website](https://www.lfd.uci.edu/~gohlke/pythonlibs/). These wheels can be downloaded then installed using `pip install <PATH TO WHEEL>`. The wheels should match the python version of the environment and Windows bit version (32 or 64), which can be deduced and verified from the name of the downloaded wheel file.

Once `shapely`, `fiona`, and `gdal` are installed from the wheel files, `fcast` can be installed by running: 
```
pip install fcast
```