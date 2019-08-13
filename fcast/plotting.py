# plotting.py is a set of functions for easy plotting of fcast data.
# These are used in the jupyter notebooks in the fcast/notebooks dir.
# Please use cell magic: `%matplotlib inline` in your notebook.
#
# Author: Alec Brazeau (abrazeau@dewberry.com)
#
# Copyright: Dewberry
#
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import pandas as pd


def new_plot(
    figsize: tuple = (20, 6),
    fontsize: int = 18,
    xlabel: str = "Discharge (cms)",
    ylabel: str = "Stage",
) -> plt.subplots:
    """
    Generic plot setup
    :param figsize: recommeded 20,6 for notebooks
    :param fontsize: label fontsize
    :param xlabel: be careful, best to make a test to verify units are consistent
    :param ylabel: be careful, best to make a test to verify units are consistent
    :return: matplotlib fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    # labelsize is the ticsize
    ax.tick_params(axis="both", which="major", labelsize=18)
    ax.grid(which="major", color="lightgrey", linestyle="--", linewidth=2)
    return fig, ax


def plotShortRange(df: pd.DataFrame, comid: int, flow: bool = True):
    """Function for plotting short range forecasts"""
    ax = df.plot(
        figsize=(20, 6), title=f"Short-range 18-hour forecast for COMID: {comid}"
    )
    ax.grid(True, which="both")
    if flow:
        ax.set(xlabel="Date", ylabel="Streamflow (cms)")
    else:
        ax.set(xlabel="Date", ylabel="Depth (m)")


def plotMediumRange(df: pd.DataFrame, comid: int, flow: bool = True):
    """Function for plotting medium range forecasts"""
    ax = df.plot(
        figsize=(20, 6),
        title=f"Medium-range seven member ensemble forecast for COMID: {comid}",
    )
    ax.legend(title="Ensemble Members")
    ax.grid(True, which="both")
    if flow:
        ax.set(xlabel="Date", ylabel="Streamflow (cms)")
    else:
        ax.set(xlabel="Date", ylabel="Depth (m)")
