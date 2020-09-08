import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rc
from alchemistry_toolkit.visuals.plot_utils import *

def plot_xy(x, y, plot_dict=None, style=True):
    """
    This function plot the dependent variable as a function of the independent 
    variable given a 2D data set.

    Parameters
    ----------
    x         (array-like): the data of the independent variable
    y         (array-like): the data of the dependent variable
    plot_dict (dict): a dictionary of settings, including labels, title, and output name
    style     (bool): whether the customized font in plot_style should be used
    """
    if plot_dict is None:
        plot_dict = {'xlabel': None, 'ylabel': None, 'title': None, 'png_name': None}
    if style:
        customize_font()
    plt.figure()
    plot_sci(x, y)
    plt.plot(x, y)
    plt.xlabel(plot_dict['xlabel'])
    plt.ylabel(plot_dict['ylabel'])
    plt.title(plot_dict['title'])
    plt.grid()
    plt.savefig(plot_dict['png_name'], dpi=600)

def plot_histogram(x, h, plot_dict=None, style=True):
    """
    This function plot a histogram given the counts of a variable.

    Parameters
    ----------
    x          (array-like): the x coordinates of the bars
    h          (array-like): the height(s) of the bars
    plot_dict  (dict): a dictionary of settings, incluing labels, title and output name
    style      (bool): whether the customized fonts in plot_style should be used
    """
    if plot_dict is None:
        plot_dict = {'xlabel': None, 'ylabel': None, 'title': None, 'png_name': None}
    if style:
        customize_font()
    plt.figure()
    plot_sci(x, h)
    plt.bar(x, height=h)
    plt.xlabel(plot_dict['xlabel'])
    plt.ylabel(plot_dict['ylabel'])
    plt.title(plot_dict['title'])
    plt.minorticks_on()
    plt.grid()
    plt.savefig(plot_dict['png_name'], dpi=600)






