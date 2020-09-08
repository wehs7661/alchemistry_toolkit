import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rc

def plot_style():
    rc('font', **{
       'family': 'sans-serif',
       'sans-serif': ['DejaVu Sans'],
       'size': 10
    })

    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

def plot_xy(x, y, xlabel=None, ylabel=None, title=None, png_name=None, style=True):
    """
    This function plot the dependent variable as a function of the independent 
    variable given a 2D data set.

    Parameters
    ----------
    x        (array-like): the data of the independent variable
    y        (array-like): the data of the dependent variable
    xlabel   (str): the name of the x-axis
    ylabel   (str): the name of the y-axis
    png_name (str): the name of the output figure
    style    (bool): whether the cutomized styling in this function should be used
    """
    
    if style:
        plot_style()
    
    plt.figure()
    if max(abs(x)) >= 10000:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    if max(abs(x)) >= 10000:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(png_name, dpi=600)
    plt.show()
