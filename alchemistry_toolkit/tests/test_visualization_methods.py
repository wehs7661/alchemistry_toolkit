import os
import numpy as np
import pytest
from alchemistry_toolkit.analysis.visualization_methods import *

@pytest.fixture
def initialize_test():
    input_dict = {}
    input_dict['xlabel'] = '$ x $'
    input_dict['ylabel'] = '$ y $'
    input_dict['title'] = 'x as a function of time'
    input_dict['png_name'] = 'test.png'

    visuals = Visualization()

    return (input_dict, visuals)

def test_plot_xy(initialize_test):
    plot_dict, visuals = initialize_test
    x = np.arange(0, 12000, 100)
    y = 2 * x
    plot_dict['png_name'] = 'sample_outputs/test_xy.png'
    assert os.path.isfile('sample_outputs/test_xy.png') is False
    visuals.plot_xy(x, y, plot_dict)
    assert os.path.isfile('sample_outputs/test_xy.png') is True
    os.system('rm sample_outputs/test_xy.png')

def test_plot_bar(initialize_test):
    plot_dict, visuals = initialize_test
    x = np.arange(10)
    h = np.array([2, 3, 4, 2, 5, 6, 3, 6, 19, 8])
    plot_dict['title'] = 'The histogram of $ x $'
    plot_dict['png_name'] = 'sample_outputs/test_bar.png'
    assert os.path.isfile('sample_outputs/test_bar.png') is False        
    visuals.plot_histogram(x, h, plot_dict)
    assert os.path.isfile('sample_outputs/test_bar.png') is True
    os.system('rm sample_outputs/test_bar.png')

def test_plot_matrix(initialize_test):
    _, visuals = initialize_test
    rng = np.random.RandomState(1)  # a separate random number generator (RNG)
    matrix = rng.rand(15, 15) * 0.1   # min: 0.00273 < default threshold
    plot_dict = {'title': 'Test matrix', 'var_name': 'n', 'png_name': 'sample_outputs/test_matrix.png'}
    assert os.path.isfile('sample_outputs/test_matrix.png') is False
    visuals.plot_matrix(matrix, plot_dict=plot_dict)
    assert os.path.isfile('sample_outputs/test_matrix.png') is True
    os.system('rm sample_outputs/test_matrix.png')

