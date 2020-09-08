import os 
import numpy as np
import pytest
from alchemistry_toolkit.visuals.plot_basics import *

@pytest.fixture
def plot_dict():
    input_dict = {}
    input_dict['xlabel'] = '$ x $'
    input_dict['ylabel'] = '$ y $'
    input_dict['title'] = 'x as a function of time'
    input_dict['png_name'] = 'test.png'

    return input_dict

def test_plot_xy(plot_dict):
    x = np.arange(0, 12000, 100)
    y = 2 * x
    assert os.path.isfile('test.png') is False
    plot_xy(x, y, plot_dict)
    assert os.path.isfile('test.png') is True
    os.system('rm test.png')

def test_plot_bar(plot_dict):
    x = np.arange(10)
    h = np.array([2, 3, 4, 2, 5, 6, 3, 6, 19, 8])
    plot_dict['title'] = 'The histogram of $ x $'
    assert os.path.isfile('test.png') is False
    plot_histogram(x, h, plot_dict)
    assert os.path.isfile('test.png') is True
    os.system('rm test.png')

    
