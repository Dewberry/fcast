import matplotlib.pyplot as plt

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
